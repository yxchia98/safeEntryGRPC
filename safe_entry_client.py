import asyncio
import logging

import grpc
import safe_entry_pb2
import safe_entry_pb2_grpc


async def run() -> None:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = safe_entry_pb2_grpc.SafeEntryStub(channel)

        response = await stub.CheckInGroup(
            safe_entry_pb2.CheckInGroupRequest(
                name=["name1", "name2", "name3", "name4"])
        )

        response = await stub.CheckInIndividual(
            safe_entry_pb2.CheckInIndividualRequest(
                name='Yi Xuan',
                nric='S9273612E',
                location='northpoint',)
        )
    print("received: " + response.status)


async def checkInIndividual(name: str, nric: str, location: str):
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = safe_entry_pb2_grpc.SafeEntryStub(channel)
        response = await stub.CheckInIndividual(
            safe_entry_pb2.CheckInIndividualRequest(
                name=name,
                nric=nric,
                location=location)
        )
        print(response)


async def checkInGroup(name: list[str], nric: list[str], location: str, time: str):
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = safe_entry_pb2_grpc.SafeEntryStub(channel)
        response = await stub.CheckInGroup(
            safe_entry_pb2.CheckInGroupRequest(
                name=name,
                nric=nric,
                location=location,
                time=time
            )
        )
        print(response)


async def checkInHistory(nric):
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = safe_entry_pb2_grpc.SafeEntryStub(channel)
        response = await stub.CheckInHistory(
            safe_entry_pb2.CheckInHistoryRequest(
                nric=nric)
        )
        for i in response.results:
            print(i)

if __name__ == "__main__":
    logging.basicConfig()
    # asyncio.run(run())
    asyncio.run(checkInIndividual(name='Yi Xuan', nric='S9273612E',
                location='northpoint'))
    # asyncio.run(checkInGroup(name=['brandon', 'yixuan', 'justin', 'jinming'], nric=[
    #             'S82746718D', 'S9283710H', 'S82716222C', 'S9125829A'], location='tampines', time='timestring'))
    # asyncio.run(checkInHistory(nric='S9273612E'))
