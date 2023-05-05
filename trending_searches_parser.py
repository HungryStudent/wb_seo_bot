import csv
import datetime
import re
import sys

import requests

import asyncio
import base64

from utils import wb_api, db


async def main(period):
    await db.start()
    await db.delete_first_search_frequency()
    await db.delete_search_priorities()

    regex = "[a-zA-Z]"
    pattern = re.compile(regex)

    response = requests.get(f"https://trending-searches.wb.ru/file?period={period}")
    decoded_content = base64.b64decode(response.json()["data"]["file"]).decode('utf-8')

    searches = decoded_content.splitlines()
    # f = open('requests.csv', newline='', encoding="utf-8")
    # searches = csv.reader(f, delimiter=";")
    today_day = int(datetime.date.today().strftime("%j"))
    for index, search in enumerate(searches):
        try:
            search = search[0]
            query, query_count = search.split(",")
            query = query.replace("﻿", "")
            query_count = int(query_count)

            search_data = await wb_api.get_search_info(query)
            if search_data == {} or search_data["data"]["total"] == 0 or search_data["metadata"][
                "catalog_type"] == "brand":
                continue

            ads_data = await wb_api.get_ads(query)
            if ads_data["prioritySubjects"] is None:
                continue

            search_id = await db.add_search(query, search_data["data"]["total"], bool(pattern.search(query)))
            await db.add_search_frequency(search_id, query_count, period, today_day)

            priority_subjects = ads_data["prioritySubjects"]
            search_priorities = []
            for i, priority_subject in enumerate(priority_subjects):
                search_priorities.append([search_id, i + 1, priority_subject])
            await db.add_search_priorities(search_priorities)
        except Exception as e:
            print(e)

        # merger


if __name__ == '__main__':
    asyncio.run(main(sys.argv[0]))
