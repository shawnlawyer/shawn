#!/usr/bin/python

import click

from .consts import *
from .Scanner import Scanner


@click.command()
@click.option('--targets','-t', 'addresses', required=True, help=OPTION_TARGETS_HELP)
def main(addresses):
    scanner = Scanner(addresses)


if __name__ == '__main__':
    # python src/__main__.py --targets=172.253.124.102,98.137.11.164
    main()
