from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, urlunparse

import httpx
from pydantic import BaseModel, field_validator

from nix_scraper.log import logger

PROXY_PROTOCOLS = ("http://", "https://", "socks5://", "socks4://")
SEARCHING_TYPES = ("Repositories", "Issues", "Wikis")
PROXY_CHECK_URL = "http://ip-api.com/json/?fields=8217"


class InputData(BaseModel):
    keywords: list[str]
    proxies: list[str]
    type: str

    @field_validator("type")
    @classmethod
    def check_request_type(cls, value: str) -> str:
        if value.lower() not in [s.lower() for s in SEARCHING_TYPES]:
            raise ValueError(f"Unavailable searching type: {value}")
        return value.lower()

    @classmethod
    def normalize_proxies(cls, proxies: list[str]) -> list[str]:
        if not proxies:
            raise ValueError("Proxies can't be empty")
        normalized = []
        for proxy in proxies:
            parsed = urlparse(proxy)
            if not parsed.scheme:
                proxy = urlunparse(("http", proxy, "", "", "", ""))
            normalized.append(proxy)
        return normalized

    @field_validator("proxies")
    @classmethod
    def validate_proxies(cls, proxies: list[str]) -> list[str]:
        return cls.normalize_proxies(proxies)


class InputDataWithProxyCheck(InputData):
    @classmethod
    def __check_proxy(cls, proxy: str) -> str | None:
        try:
            resp = httpx.get(PROXY_CHECK_URL, proxy=proxy, timeout=10)
            if resp.status_code == 200 and resp.json().get("query"):
                return proxy
        except Exception as error:
            logger.error(f"Can't use this proxy: {proxy} ({error})")
        return None

    @classmethod
    def __check_multiple_proxies(cls, proxies: list[str]) -> list[str]:
        with ThreadPoolExecutor(len(proxies)) as pool:
            checked_proxies = [
                proxy for proxy in pool.map(cls.__check_proxy, proxies) if proxy
            ]
        logger.info(f"Working proxies: {checked_proxies}")
        return checked_proxies

    @field_validator("proxies")
    @classmethod
    def validate_proxies(cls, proxies: list[str]) -> list[str]:
        logger.info(f"Checking proxies: {proxies}")
        proxies = cls.normalize_proxies(proxies)
        return cls.__check_multiple_proxies(proxies)
