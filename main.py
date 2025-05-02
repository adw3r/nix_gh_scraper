import argparse
import asyncio

from src import utils
from src.log import logger
from src.parsers import retrieve_info
from src.utils import create_args


async def main():
    args: argparse.Namespace = create_args()
    input_data: dict = utils.get_data(args.file)
    repo_hrefs: list[dict] = await retrieve_info(input_data)
    logger.info(f'{repo_hrefs = }')


if __name__ == '__main__':
    asyncio.run(main())
