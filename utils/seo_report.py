import io

import aiohttp
import pymorphy2
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from tempfile import NamedTemporaryFile

from config import searches_server_host

morph = pymorphy2.MorphAnalyzer()


async def create_report(user_id, category_id):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                    f'{searches_server_host}/report?user_id={user_id}&category_id={category_id}') as resp:
                data = await resp.json()
                return data["filename"]
        except Exception:
            return "Error"
