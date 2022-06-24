import asyncio
import logging
from sqlite3 import Date
from tokenize import Special

import grpc
import safe_entry_pb2
import safe_entry_pb2_grpc
from database import MongoDatabase
from datetime import datetime


class SafeEntry(safe_entry_pb2_grpc.SafeEntryServicer):
    mongoDB = MongoDatabase()
    mongoDB.connect()

    async def CheckInIndividual(self, request: safe_entry_pb2.CheckInIndividualRequest, context: grpc.aio.ServicerContext) -> safe_entry_pb2.CheckInIndividualReply:
        time = datetime.now()
        db = self.mongoDB.connect_database('safe-entry')
        records = db['records']
        record = {
            "name": request.name,
            "nric": request.nric,
            "location": request.location,
            "checkInTime": time,
            "checkOutTime": None,
            'closeContact': False,
        }
        inserted_record = records.insert_one(record)
        print('Check-in acknowledgement for', request.name, request.nric,
              'at', request.location, time, '=', inserted_record.acknowledged)
        if not inserted_record.acknowledged:
            return safe_entry_pb2.CheckInIndividualReply(status="Individual check-in failure")
        return safe_entry_pb2.CheckInIndividualReply(status="Individual check-in success")

    async def CheckOutIndividual(self, request: safe_entry_pb2.CheckOutIndividualRequest, context: grpc.aio.ServicerContext) -> safe_entry_pb2.CheckOutIndividualReply:
        time = datetime.now()
        db = self.mongoDB.connect_database('safe-entry')
        records = db['records']
        query = {'name': request.name,
                 'nric': request.nric,
                 'location': request.location,
                 'checkOutTime': None}
        updateQuery = {'$set': {'checkOutTime': time}}
        updated_records = records.update_many(query, updateQuery)
        print('Check-out acknowledgement for', request.name, request.nric,
              'at', request.location, time, '=', updated_records.acknowledged)
        if not updated_records.acknowledged:
            return safe_entry_pb2.CheckOutIndividualReply(status="Individual check-out failure")

        return safe_entry_pb2.CheckOutIndividualReply(status="Individual check-out success")

    async def CheckInGroup(self, request: safe_entry_pb2.CheckInGroupRequest, context: grpc.aio.ServicerContext) -> safe_entry_pb2.CheckInGroupReply:
        time = datetime.now()
        names = list(request.names)
        nrics = list(request.nrics)
        db = self.mongoDB.connect_database('safe-entry')
        records = db['records']
        checkInList = []
        for i in range(0, len(nrics)):
            record = {
                "name": names[i],
                "nric": nrics[i],
                "location": request.location,
                "checkInTime": time,
                "checkOutTime": None,
                'closeContact': False,
            }
            checkInList.append(record)
        inserted_records = records.insert_many(checkInList)
        print('Check-in acknowledgement for', names, nrics,
              'at', request.location, time, '=', inserted_records.acknowledged)
        if not inserted_records.acknowledged:
            return safe_entry_pb2.CheckInGroupReply(status="Group check-in failure")
        return safe_entry_pb2.CheckInGroupReply(status="Group check-in success")

    async def CheckOutGroup(self, request: safe_entry_pb2.CheckOutGroupRequest, context: grpc.aio.ServicerContext) -> safe_entry_pb2.CheckOutGroupReply:
        time = datetime.now()
        names = list(request.names)
        nrics = list(request.nrics)
        db = self.mongoDB.connect_database('safe-entry')
        records = db['records']
        query = {
            'name': {'$in': names},
            'nric': {'$in': nrics},
            'location': request.location,
            'checkOutTime': None
        }
        updateQuery = {'$set': {'checkOutTime': time}}
        updated_records = records.update_many(query, updateQuery)
        print('Check-out acknowledgement for', names, nrics,
              'at', request.location, time, '=', updated_records.acknowledged)
        if not updated_records.acknowledged:
            return safe_entry_pb2.CheckOutGroupReply(status="Group check-out failure")
        return safe_entry_pb2.CheckOutGroupReply(status="Group check-out success")

    async def CheckInHistory(self, request: safe_entry_pb2.CheckInHistoryRequest, context: grpc.aio.ServicerContext) -> safe_entry_pb2.CheckInHistoryReply:
        formatted_results = []
        db = self.mongoDB.connect_database('safe-entry')
        records = db['records']
        results = records.find({"nric": request.nric}, {"_id": 0})
        for i in results:
            i['checkInTime'] = i['checkInTime'].isoformat()
            
            if i['checkOutTime']:
                i['checkOutTime'] = i['checkOutTime'].isoformat()
            formatted_results.append(i)
        print(formatted_results)
        return safe_entry_pb2.CheckInHistoryReply(results=formatted_results)


class SpecialAccess(safe_entry_pb2_grpc.SpecialAccessServicer):
    mongoDB = MongoDatabase()
    mongoDB.connect()

    async def MarkCluster(self, request: safe_entry_pb2.MarkClusterRequest, context: grpc.aio.ServicerContext) -> safe_entry_pb2.MarkClusterReply:
        time = datetime.strptime(
            ' '.join([request.date, request.time]), '%d/%m/%Y %H:%M')
        db = self.mongoDB.connect_database('safe-entry')
        records = db['clusters']
        record = {
            "location": request.location,
            "time": time
        }
        inserted_record = records.insert_one(record)
        print('New cluster acknowledgement at', request.location, time,
              '=', inserted_record.acknowledged)
        return safe_entry_pb2.MarkClusterReply(status="complete!")


async def serve() -> None:
    server = grpc.aio.server()
    safe_entry_pb2_grpc.add_SafeEntryServicer_to_server(SafeEntry(), server)
    safe_entry_pb2_grpc.add_SpecialAccessServicer_to_server(
        SpecialAccess(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    asyncio.run(serve())
