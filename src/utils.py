import argparse
import json
from argparse import ArgumentParser
from pathlib import Path


def get_data(file_path: str | Path) -> dict:
    with open(file_path) as file:
        input_data = json.load(file)
    return input_data


def create_args() -> argparse.Namespace:
    argument_parser = ArgumentParser()
    argument_parser.add_argument('--file', '-f')
    args = argument_parser.parse_args()
    if not args.file:
        raise FileNotFoundError('Input file can`t be empty!')
    return args
