import bs4



class Serializer:

    @staticmethod
    def extract_urls(html: str) -> list[str]:
        soup = bs4.BeautifulSoup(html, 'lxml')
        rows = soup.find_all('div', {'class': 'search-title'})
        return [f'https://github.com{i.find("a")["href"]}' for i in rows]

    @staticmethod
    def extract_owner(url) -> str:
        return url.removeprefix('https://github.com/').split('/')[0]
