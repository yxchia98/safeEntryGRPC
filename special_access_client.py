import asyncio
import logging

import grpc
import safe_entry_pb2
import safe_entry_pb2_grpc

menu_loop = True
menu_options = {
    1: 'Mark Cluster',
    2: 'Exit'
}

def print_menu():
    for key in menu_options.keys():
        print(key, '--', menu_options[key])

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

    while (menu_loop):
        print_menu()
        option = ''

        try:
            option = int(input("Enter your choice: "))
        except:
            print('Wrong input. Please enter a number...')

        if option == 1:
            location = input('Enter location of cluster: ')
            date = input('Enter date of cluster (DD/MM/YYYY): ')
            time = input('Enter time of cluster (00:00 - 23:59):')
            asyncio.run(markCluster(location=location, date=date, time=time))
        elif option == 2:
            print('Exiting')
            exit()
