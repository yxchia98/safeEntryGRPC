import asyncio
import logging

import grpc
import safe_entry_pb2
import safe_entry_pb2_grpc

import threading


menu_loop = True

menu_options = {
    1: 'Check In - Single',
    2: 'Check Out - Single',
    3: 'Check In - Group',
    4: 'Check Out - Group',
    5: 'Check History',
    6: 'Exit',
}

def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key]) 

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
            empty_string = ""
            hyphen = " to "
            
            for results in collectedresponse.results:
                print(f"\nAlert! You, {results.name} ({results.nric}), visited {results.location} on {results.checkInTime} { hyphen if results.checkOutTime else empty_string} {results.checkOutTime if results.checkOutTime else empty_string} which has been marked as a COVID Cluser. Please quarantine for 14 days.\n")

        # async for i in response:
        #     # closeContact wont show if false, only shows if true
        #     print(i)

async def subscriptionThreadFunction(name: str, nric: str):
    notificationTask = asyncio.create_task(subscribeNotification(name=name, nric=nric))
    await notificationTask

async def main():

    logging.getLogger("asyncio").setLevel(logging.WARNING)

    name = input("Enter your name: ")
    nric = input("Enter your NRIC: ")

    # asyncio.create_task(checkInIndividual(name=name, nric=nric,
    #             location=location))
    # asyncio.create_task(checkOutIndividual(name=name, nric=nric,
    #             location=location))
    # asyncio.create_task(checkInGroup(names=groupnames,
    #             nrics=groupnrics, location=location))
    # asyncio.create_task(checkOutGroup(names=groupnames,
    #             nrics=groupnrics, location=location))

    subscription_thread = threading.Thread(target=asyncio.run, args=(subscriptionThreadFunction(name, nric),), daemon=True)
    subscription_thread.start()

    while menu_loop:
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        if option == 1:
            print(1)
        elif option == 2:
            print(2)
        elif option == 3:
            print(3)
        elif option == 4:
            print(4)
        elif option == 5:
            print(5)
        elif option == 6:
            print('Exiting')
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 4.')

if __name__ == "__main__":
    asyncio.run(main())
