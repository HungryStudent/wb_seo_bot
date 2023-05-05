import aiohttp


async def get_search_info(search_query):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&curr=rub&dest=123585704&filters=xsubject&query={search_query}&resultset=filters') as resp:
            text = await resp.text()
            if text == "{}":
                return
            if resp.status == 404:
                return
            try:
                response = await resp.json(content_type="text/plain")
            except aiohttp.client_exceptions.ContentTypeError:
                return
            print(search_query, response)
            if response is None:
                return
            return response


async def get_ads(query):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'https://catalog-ads.wildberries.ru/api/v5/search?keyword={query}') as resp:
            response = await resp.json()
            return response


async def get_card_details(article_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'https://card.wb.ru/cards/detail?curr=rub&dest=-1257786&regions=80,64,38,4,115,83,33,68,70,69,30,86,75,40,1,66,48,110,22,31,71,114,111&spp=0&nm={article_id}') as resp:
            if resp.status == 404:
                return
            response = await resp.json(content_type="text/plain")

            if not response["data"]["products"]:
                return
            return response["data"]["products"][0]
