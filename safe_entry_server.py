import asyncio
import logging
from sqlite3 import Date

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
        }
        inserted_record = records.insert_one(record)
        print(inserted_record.inserted_id)
        print(request)
        return safe_entry_pb2.CheckInIndividualReply(status="complete!")

    async def CheckInGroup(self, request: safe_entry_pb2.CheckInGroupRequest, context: grpc.aio.ServicerContext) -> safe_entry_pb2.CheckInGroupReply:
        time = datetime.now()
        for i in range(0, request.nric.length):
            record = {
                "name": request.name[i],
                "nric": request.nric[i],
                "location": request.location,
                "checkInTime": time,
                "checkOutTime": None,
            }
            print(record)
        return safe_entry_pb2.CheckInGroupReply(status="complete!")

    async def CheckInHistory(self, request: safe_entry_pb2.CheckInHistoryRequest, context: grpc.aio.ServicerContext) -> safe_entry_pb2.CheckInHistoryReply:
        formatted_results = []
        db = self.mongoDB.connect_database('safe-entry')
        records = db['records']
        results = records.find({"nric": request.nric}, {"id": 0})
        for i in results:
            formatted_results.append(i)
        # formatted_results = json.dumps(formatted_results, default = lambda x: x.__dict__)
        print(formatted_results)
        return safe_entry_pb2.CheckInHistoryReply(results=formatted_results)


async def serve() -> None:
    server = grpc.aio.server()
    safe_entry_pb2_grpc.add_SafeEntryServicer_to_server(SafeEntry(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    asyncio.run(serve())
