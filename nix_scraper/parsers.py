import asyncio
import random
import typing
from concurrent.futures import ThreadPoolExecutor

import bs4
import curl_cffi

from nix_scraper import schemas
from nix_scraper.log import logger
from nix_scraper.serializers import Serializer

REQUEST_HEADERS = {
    'authority': 'github.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
              'image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8,uk;q=0.7',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'referer': 'https://github.com/',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}


class GitScraper:
    def __init__(self, session: curl_cffi.AsyncSession):
        self.session = session

    async def get_searching_page(self, query: str, searching_type: str) -> curl_cffi.Response:
        params = {
            'q': query, 'type': searching_type
        }
        response = await self.session.get('https://github.com/search', params=params, headers=REQUEST_HEADERS)
        return response

    async def check_extras(self, url: str) -> curl_cffi.Response:
        response = await self.session.get(url, headers=REQUEST_HEADERS)
        return response

def simple_format_urls(urls: typing.Sequence) -> list[dict]:
    return [
        {'url': url} for url in urls
    ]



def extras_format_urls(results: list[curl_cffi.Response]) -> list[dict]:
    data = []

    for response in results:
        language_stats = {}
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        side_bar = soup.find('div', {'class': 'Layout-sidebar'})
        lis = side_bar.find_all('div')[0].find_all('li', {'class': 'd-inline'})
        spans_list = [li.find_all('span') for li in lis]
        for span_list in spans_list:
            language_stats[span_list[0].text] = float(span_list[1].text[:-1])

        repo_url = str(response.url)
        result = {
            'url': repo_url,
            "extra": {
                "owner": Serializer.extract_owner(repo_url),
                "language_stats": language_stats
            }
        }

        data.append(result)

    return data

async def retrieve_info(input_data: dict) -> list[dict]:
    input_data = schemas.InputDataWithProxyCheck(**input_data)
    logger.info(f'{input_data = }')

    proxy: str = random.choice(input_data.proxies)
    session = curl_cffi.AsyncSession(proxy=proxy)
    parser = GitScraper(session)

    searching_page_response: curl_cffi.Response = await parser.get_searching_page(
        input_data.type, ' '.join(input_data.keywords)
    )
    logger.info(f'{searching_page_response = }')
    urls: list[str] = Serializer.extract_urls(searching_page_response.text)
    if input_data.type.lower() == 'repositories':
        tasks = [parser.check_extras(url) for url in urls]
        results: list[curl_cffi.Response] = await asyncio.gather(*tasks)
        if not results:
            raise Exception(f'check_extras method can`t give empty results with given {input_data = }')
        return extras_format_urls(results=results)
    return simple_format_urls(urls)
