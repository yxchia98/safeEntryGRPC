import asyncio
import logging

import grpc
import safe_entry_pb2
import safe_entry_pb2_grpc


async def markCluster(location: str, date: str, time: str):
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = safe_entry_pb2_grpc.SpecialAccessStub(channel)
        response = await stub.MarkCluster(
            safe_entry_pb2.MarkClusterRequest(
                location=location,
                date=date,
                time=time)
        )
        print(response)

if __name__ == "__main__":
    logging.basicConfig()
    location = 'ION Orchard'
    date = '20/06/2021'
    time = '15:30'
    asyncio.run(markCluster(location=location, date=date, time=time))
