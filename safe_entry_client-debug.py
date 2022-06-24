import asyncio
import logging

import grpc
import safe_entry_pb2
import safe_entry_pb2_grpc


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


async def subscribeNotification(name: str, nric: str):
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = safe_entry_pb2_grpc.NotificationStub(channel)
        response = stub.SubscribeNotification(
            safe_entry_pb2.NotificationRequest(
                name=name,
                nric=nric
            )
        )
        while True:
            collectedresponse = await response.read()
            print(collectedresponse)

        # async for i in response:
        #     # closeContact wont show if false, only shows if true
        #     print(i)


async def main():
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    groupnames = ['name1', 'name2', 'name3', 'name4']
    groupnrics = ['nric1', 'nric2', 'nric3', 'nric4']
    location = 'AMK Hub'
    name = 'name5'
    nric = 'nric5'
    notificationTask = asyncio.create_task(
        subscribeNotification(name=name, nric=nric))
    # asyncio.create_task(checkInIndividual(name=name, nric=nric,
    #             location=location))
    # asyncio.create_task(checkOutIndividual(name=name, nric=nric,
    #             location=location))
    # asyncio.create_task(checkInGroup(names=groupnames,
    #             nrics=groupnrics, location=location))
    # asyncio.create_task(checkOutGroup(names=groupnames,
    #             nrics=groupnrics, location=location))
    task = asyncio.create_task(checkInHistory(nric=nric))
    await notificationTask
    await task


if __name__ == "__main__":
    asyncio.run(main())
