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


async def checkOutIndividual(name: str, nric: str, location: str):
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = safe_entry_pb2_grpc.SafeEntryStub(channel)
        response = await stub.CheckOutIndividual(
            safe_entry_pb2.CheckOutIndividualRequest(
                name=name,
                nric=nric,
                location=location)
        )
        print(response)


async def checkInGroup(names: list[str], nrics: list[str], location: str):
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = safe_entry_pb2_grpc.SafeEntryStub(channel)
        response = await stub.CheckInGroup(
            safe_entry_pb2.CheckInGroupRequest(
                names=names,
                nrics=nrics,
                location=location)
        )
        print(response)


async def checkOutGroup(names: list[str], nrics: list[str], location: str):
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = safe_entry_pb2_grpc.SafeEntryStub(channel)
        response = await stub.CheckOutGroup(
            safe_entry_pb2.CheckOutGroupRequest(
                names=names,
                nrics=nrics,
                location=location)
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
            # closeContact wont show if false, only shows if true
            print(i)

if __name__ == "__main__":
    logging.basicConfig()
    groupnames = ['name1', 'name2', 'name3', 'name4']
    groupnrics = ['nric1', 'nric2', 'nric3', 'nric4']
    location = 'AMK Hub'
    name = 'name3'
    nric = 'nric3'
    # asyncio.run(run())
    # asyncio.run(checkInIndividual(name=name, nric=nric,
    #             location=location))
    # asyncio.run(checkOutIndividual(name=name, nric=nric,
    #             location=location))
    asyncio.run(checkInGroup(names=groupnames,
                nrics=groupnrics, location=location))
    # asyncio.run(checkOutGroup(names=groupnames,
    #             nrics=groupnrics, location=location))
    asyncio.run(checkInHistory(nric=nric))
