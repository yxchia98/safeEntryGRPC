import asyncio
import logging
from time import strftime
from datetime import datetime

import grpc
import safe_entry_pb2
import safe_entry_pb2_grpc

import threading


menu_loop = True
stop_threads = False
menu_options = {
    1: 'Check In - Single',
    2: 'Check Out - Single',
    3: 'Check In - Group',
    4: 'Check Out - Group',
    5: 'History',
    6: 'Exposure History',
    7: 'Exit',
}


def print_menu():
    print("\n================")
    print("SafeEntry Client")
    print("================")
    for key in menu_options.keys():
        print(key, '--', menu_options[key])


async def checkInIndividual(name: str, nric: str, location: str):
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = safe_entry_pb2_grpc.SafeEntryStub(channel)
        response = await stub.CheckInIndividual(
            safe_entry_pb2.CheckInIndividualRequest(
                name=name,
                nric=nric,
                location=location)
        )
        print(response.status)


async def checkOutIndividual(name: str, nric: str, location: str):
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = safe_entry_pb2_grpc.SafeEntryStub(channel)
        response = await stub.CheckOutIndividual(
            safe_entry_pb2.CheckOutIndividualRequest(
                name=name,
                nric=nric,
                location=location)
        )
        print(response.status)


async def checkInGroup(names: list[str], nrics: list[str], location: str):
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = safe_entry_pb2_grpc.SafeEntryStub(channel)
        response = await stub.CheckInGroup(
            safe_entry_pb2.CheckInGroupRequest(
                names=names,
                nrics=nrics,
                location=location)
        )
        print(response.status)


async def checkOutGroup(names: list[str], nrics: list[str], location: str):
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = safe_entry_pb2_grpc.SafeEntryStub(channel)
        response = await stub.CheckOutGroup(
            safe_entry_pb2.CheckOutGroupRequest(
                names=names,
                nrics=nrics,
                location=location)
        )
        print(response.status)


async def checkInHistory(nric):
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = safe_entry_pb2_grpc.SafeEntryStub(channel)
        response = await stub.CheckInHistory(
            safe_entry_pb2.CheckInHistoryRequest(
                nric=nric)
        )
        for i in response.results:
            # closeContact wont show if false, only shows if true
            inTime = (datetime.fromisoformat(i.checkInTime)
                      ).strftime('%d %b %Y, %H:%M')
            outTime = (datetime.fromisoformat(i.checkOutTime)
                       ).strftime('%d %b %Y, %H:%M') if i.checkOutTime != '' else 'No check-out recorded'
            closeContact = 'True' if i.closeContact else 'False'
            print(
                f"Check-in time: {inTime}\nCheck-out time: {outTime}\nLocation: {i.location}\nClose contact: {closeContact}\n")


async def checkExposureHistory(nric):
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = safe_entry_pb2_grpc.SafeEntryStub(channel)
        response = await stub.CheckExposureHistory(
            safe_entry_pb2.CheckExposureHistoryRequest(
                nric=nric)
        )
        for i in response.results:
            # closeContact wont show if false, only shows if true
            inTime = (datetime.fromisoformat(i.checkInTime)
                      ).strftime('%d %b %Y, %H:%M')
            outTime = (datetime.fromisoformat(i.checkOutTime)
                       ).strftime('%d %b %Y, %H:%M') if i.checkOutTime is not None else 'No check-out recorded'
            closeContact = 'True' if i.closeContact else 'False'
            print(
                f"Check-in time: {inTime}\nCheck-out time: {outTime}\nLocation: {i.location}\nClose contact: {closeContact}\n")


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
            global stop_threads
            if stop_threads:
                channel.close()
                break
            collectedresponse = await response.read()
            empty_string = ""
            hyphen = " to "

            for results in collectedresponse.results:
                print(f"\nAlert! You, {results.name} ({results.nric}), visited {results.location} on {results.checkInTime} { hyphen if results.checkOutTime else empty_string} {results.checkOutTime if results.checkOutTime else empty_string} which has been marked as a COVID Cluser. Please quarantine for 14 days from the date of visit.\n")
        response.cancel()
        # async for i in response:
        #     # closeContact wont show if false, only shows if true
        #     print(i)


# async def unsubscribeNotification(nric: str):
#     async with grpc.aio.insecure_channel("localhost:50051") as channel:
#         stub = safe_entry_pb2_grpc.NotificationStub(channel)
#         response = await stub.UnsubscribeNotification(
#             safe_entry_pb2.UnsubscribeRequest(
#                 nric=nric
#             )
#         )
#         print(response)


async def subscriptionThreadFunction(name: str, nric: str):
    notificationTask = asyncio.create_task(
        subscribeNotification(name=name, nric=nric))
    await notificationTask


async def main():

    logging.getLogger("asyncio").setLevel(logging.WARNING)

    name = input("Enter your name: ")
    nric = input("Enter your NRIC: ")

    subscription_thread = threading.Thread(target=asyncio.run, args=(
        subscriptionThreadFunction(name, nric),), daemon=True)
    subscription_thread.start()

    while menu_loop:
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        if option == 1:
            location = input('Enter your location: ')
            print(f"Checking in...")
            await asyncio.create_task(checkInIndividual(name=name, nric=nric,
                                                        location=location))
        elif option == 2:
            location = input('Enter your location: ')
            print(f"Checking out...")
            await asyncio.create_task(checkOutIndividual(name=name, nric=nric,
                                                         location=location))

        elif option == 3:
            groupnames = [name]
            groupnrics = [nric]
            location = input('Enter your location: ')
            n = int(
                input('Enter number of people to check in (yourself not included):'))

            for i in range(0, n):
                temp_name = input(f"Enter no. {i+1} name: ")
                temp_nric = input(f"Enter no. {i+1} NRIC: ")
                groupnames.append(temp_name)
                groupnrics.append(temp_nric)

            print(f"Checking in...")

            await asyncio.create_task(checkInGroup(names=groupnames,
                                                   nrics=groupnrics, location=location))

        elif option == 4:
            groupnames = [name]
            groupnrics = [nric]
            location = input('Enter your location: ')
            n = int(
                input('Enter number of people to check out (yourself not included):'))

            for i in range(0, n):
                temp_name = input(f"Enter no. {i+1} name: ")
                temp_nric = input(f"Enter no. {i+1} NRIC: ")
                groupnames.append(temp_name)
                groupnrics.append(temp_nric)

            print(f"Checking out...")
            await asyncio.create_task(checkOutGroup(names=groupnames,
                                                    nrics=groupnrics, location=location))

        elif option == 5:
            print("\n================")
            print("Check In History")
            print(f"================\nName: {name}\nNRIC: {nric}\n")
            await asyncio.create_task(checkInHistory(nric=nric))
        elif option == 6:
            print("\n================")
            print("Exposure History")
            print(f"================\nName: {name}\nNRIC: {nric}\n")
            await asyncio.create_task(checkExposureHistory(nric=nric))
        elif option == 7:
            print('Exiting')
            # await asyncio.create_task(unsubscribeNotification(nric=nric))
            stop_threads = True
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 4.')

if __name__ == "__main__":
    asyncio.run(main())
