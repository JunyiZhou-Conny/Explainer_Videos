"""
Command-line translation app.
"""

import argparse
import asyncio

from art import text2art
from googletrans import Translator


async def main(args):
    print("\n")
    print(text2art("AC215"))
    print("\nArguments:", args)

    text = args.text

    if args.file:
        with open(args.file, encoding="utf-8") as file:
            text = file.read()

    print("\nInput:", text)

    async with Translator(raise_exception=True) as translator:
        try:
            result = await translator.translate(
                text,
                src=args.src,
                dest=args.dest,
            )
        except Exception as error:
            raise RuntimeError(
                "Translation request to Google Translate failed "
                "(the server's network/IP may be rate-limited or blocked "
                "by Google's unofficial translate endpoint)."
            ) from error

    print("Output:", result.text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple translation app")

    parser.add_argument(
        "-t",
        "--text",
        type=str,
        default="I love cheese",
        help="Text to translate",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default="",
        help="File to translate",
    )
    parser.add_argument(
        "-s",
        "--src",
        default="en",
        help="Source language",
    )
    parser.add_argument(
        "-d",
        "--dest",
        default="it",
        help="Destination language",
    )

    asyncio.run(main(parser.parse_args()))