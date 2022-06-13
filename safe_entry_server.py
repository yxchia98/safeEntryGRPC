import asyncio
import logging

import grpc
import safe_entry_pb2
import safe_entry_pb2_grpc
from database import MongoDatabase
import json


class SafeEntry(safe_entry_pb2_grpc.SafeEntryServicer):
    mongoDB = MongoDatabase()
    mongoDB.connect()

    async def CheckInIndividual(self, request: safe_entry_pb2.CheckInIndividualRequest, context: grpc.aio.ServicerContext) -> safe_entry_pb2.CheckInIndividualReply:
        db = self.mongoDB.connect_database('safe-entry')
        records = db['records']
        record = {
            "name": request.name,
            "nric": request.nric,
            "location": request.location,
            "time": request.time
        }
        inserted_record = records.insert_one(record)
        print(inserted_record.inserted_id)
        print(request)
        return safe_entry_pb2.CheckInIndividualReply(status="complete!")

    async def CheckInGroup(self, request: safe_entry_pb2.CheckInGroupRequest, context: grpc.aio.ServicerContext) -> safe_entry_pb2.CheckInGroupReply:
        for i in request.name:
            print(i)
        print(request.name)
        return safe_entry_pb2.CheckInGroupReply(status="complete!")

    async def CheckInHistory(self, request: safe_entry_pb2.CheckInHistoryRequest, context: grpc.aio.ServicerContext) -> safe_entry_pb2.CheckInHistoryReply:
        formatted_results = []
        db = self.mongoDB.connect_database('safe-entry')
        records = db['records']
        results = records.find({"nric": request.nric})
        for i in results:
            del i['_id']
            formatted_results.append(i)
        # formatted_results = json.dumps(formatted_results, default = lambda x: x.__dict__)
        print(formatted_results)
        return safe_entry_pb2.CheckInHistoryReply(results=formatted_results)

    # async def SayHello(
    #     self, request: helloworld_pb2.HelloRequest, context: grpc.aio.ServicerContext
    # ) -> helloworld_pb2.HelloReply:
    #     return helloworld_pb2.HelloReply(message="Hello, %s!" % request.name)


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
