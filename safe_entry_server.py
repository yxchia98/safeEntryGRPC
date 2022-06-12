import asyncio
import logging

import grpc
import safe_entry_pb2
import safe_entry_pb2_grpc


class SafeEntry(safe_entry_pb2_grpc.SafeEntryServicer):
    async def CheckInIndividual(
        self,
        request: safe_entry_pb2.CheckInIndividualRequest,
        context: grpc.aio.ServicerContext,
    ) -> safe_entry_pb2.CheckInIndividualReply:
        print(request.name)
        return safe_entry_pb2.CheckInIndividualReply(status="complete!")

    async def CheckInGroup(
        self,
        request: safe_entry_pb2.CheckInGroupRequest,
        context: grpc.aio.ServicerContext,
    ) -> safe_entry_pb2.CheckInGroupReply:
        print(request.name)
        return safe_entry_pb2.CheckInGroupReply(status="complete!")

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
