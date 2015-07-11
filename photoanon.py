#!/usr/bin/env python3
# -*- Mode: Python; py-indent-offset: 4 -*-

# (c) Copyright Cameron Conn 2015
# This file is licensed GPLv3 or Later
# See LICENSE for details


from gi.repository import GExiv2

import argparse
from time import time


def main():
    '''
    Interprets command-line arguments and act accordingly
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('image', help='Image to anonymize')

    args = parser.parse_args()


if __name__ == '__main__':
    main()
