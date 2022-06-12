import asyncio
import logging

import grpc
import safe_entry_pb2
import safe_entry_pb2_grpc


async def run() -> None:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = safe_entry_pb2_grpc.SafeEntryStub(channel)
        response = await stub.CheckInGroup(
            safe_entry_pb2.CheckInGroupRequest(name=["this", "is", "a", "test"])
        )
    print("received: " + response.status)


if __name__ == "__main__":
    logging.basicConfig()
    asyncio.run(run())
