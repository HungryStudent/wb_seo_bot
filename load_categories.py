import asyncio
import requests

from utils import db


async def main():
    req = requests.get("https://static-basket-01.wb.ru/vol0/data/subject-base.json")
    data = req.json()
    print("Loading...")
    categories = []
    for parent in data:
        for category in parent["childs"]:
            categories.append([category["id"], category["name"]])
    await db.add_categories(categories)


# merger
if __name__ == '__main__':
    asyncio.run(main())
