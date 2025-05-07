import argparse
import asyncio

from nix_scraper import utils
from nix_scraper.log import logger
from nix_scraper.scrapers import retrieve_info
from nix_scraper.utils import create_args


async def main():
    args: argparse.Namespace = create_args()
    input_data: dict = utils.get_data(args.file)
    repo_hrefs: list[dict] = await retrieve_info(input_data)
    logger.info(f"{repo_hrefs = }")


if __name__ == "__main__":
    asyncio.run(main())
