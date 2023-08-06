import os
import sys
import re
import argparse
from witter.chain_generator import ChainGenerator
from typing import TextIO


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate texts based on an input text."
    )

    parser.add_argument(
        "-c",
        "--chain-length",
        type=int,
        default=10,
        help="The number of characters used to chain together and forecast the next character.",
    )

    parser.add_argument(
        "-t",
        "--text-length",
        type=int,
        default=200,
        help="The length of text sample to generate. Note: may be approximate.",
    )

    parser.add_argument(
        "-s",
        "--sample-count",
        type=int,
        default=1,
        help="The number of samples to generate",
    )

    parser.add_argument(
        "input_file",
        metavar="FILE",
        nargs="?",
        default="-",
        help="The file to use as a source of text for for witter, or - for stdin.",
    )

    return parser.parse_args()


def read_source(input_stream: TextIO) -> str:
    source = input_stream.read()

    pattern = re.compile("[^\\w\\s,\\.']+")
    source = pattern.sub(" ", source)

    unwanted_pattern = re.compile("[0-9]+")
    source = unwanted_pattern.sub(" ", source)

    multiple_spaces_pattern = re.compile("[\\s\\n\\r]+")
    source = multiple_spaces_pattern.sub(" ", source)

    return source


def main():
    arguments = parse_arguments()

    if not arguments.input_file or arguments.input_file == "-":
        source = read_source(sys.stdin)
    else:
        absolute_path = os.path.abspath(arguments.input_file)

        if not os.path.isfile(absolute_path):
            print(f"Not a file: {absolute_path}")
            sys.exit(1)
        with open(arguments.input_file, mode="r") as source:
            source = read_source(source)

    output_limit = arguments.text_length
    chain_length = arguments.chain_length

    generator = ChainGenerator(source)

    print(f"Chain Length: {chain_length}")
    for attempt in range(0, 3):
        print(f"Version: {attempt + 1}")
        print(f"{generator.generate_chain(chain_length, output_limit)}")
        print("")


if __name__ == "__main__":
    main()
