from safe_entry_client import *
from special_access_client import *
import unittest
from unittest import IsolatedAsyncioTestCase
import asyncio


class CheckIns(IsolatedAsyncioTestCase):
    async def test_single_checkin(self):

        name = "Chee Cheong Fan"
        nric = "S9876543O"
        location = "East Coast Park"

        await asyncio.create_task(checkInIndividual(name=name, nric=nric, location=location))

    async def test_group_checkin(self):
        group_names = ["Dim Sum", "Har Gao"]
        group_nrics = ["S9876543I", "S9876543U"]
        location = "East Coast Park"

        await asyncio.create_task(checkInGroup(names=group_names, nrics=group_nrics, location=location))

    async def test_single_checkout(self):

        name = "Chee Cheong Fan"
        nric = "S9876543O"
        location = "East Coast Park"

        await asyncio.create_task(checkOutIndividual(name=name, nric=nric, location=location))

    async def test_group_checkout(self):
        group_names = ["Dim Sum", "Har Gao"]
        group_nrics = ["S9876543I", "S9876543U"]
        location = "East Coast Park"

        await asyncio.create_task(checkOutGroup(names=group_names, nrics=group_nrics, location=location))


class History(IsolatedAsyncioTestCase):
    async def test_checkin_history(self):
        nric = "S9876543O"

        await asyncio.create_task(checkInHistory(nric=nric))

    async def test_exposure_history(self):
        nric = "S9876543O"

        await asyncio.create_task(checkExposureHistory(nric=nric))


class MarkCluster(IsolatedAsyncioTestCase):
    async def test_mark_cluster(self):
        location = "East Coast Park"
        date = "06/06/2022"
        time = "12:34"
        await asyncio.create_task(markCluster(location=location, date=date, time=time))

    async def test_show_clusters(self):
        await asyncio.create_task(showClusters())


if __name__ == '__main__':
    unittest.main()
