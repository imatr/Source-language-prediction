#!/usr/bin/env python3

# This script will put the sentences of the English books in the books dataset into text files.

import glob
import argparse
import gzip
import xml.etree.ElementTree as ET
from collections import defaultdict
import os


def main():
    for path in glob.glob('{}/raw/en/*.xml.gz'.format(args.input)):
        name = path.split('/')[-1][:-7]
        with gzip.open(path, 'rb') as file_handle:
            with open('{}/{}.txt'.format(args.output, name), 'w') as out:
                tree = ET.fromstring(file_handle.read())
                for i, sentence in enumerate(tree.findall('.//s')):
                    if i == 0:
                        continue
                    print(sentence.text, file=out)


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='The path to the Books dataset')
    parser.add_argument('output', type=str, help='The location where to put the text files')
    args = parser.parse_args()
    # Format path as required
    if args.input[-1] == '/':
        args.input = args.input[:-1]
    if args.output[-1] == '/':
        args.output = args.output[:-1]
    # Create output folder if needed
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    main()
