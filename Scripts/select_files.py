#!/usr/bin/env python3

# This script will copy files that have a length between 380 and 2500 tokens from
# the input directory to the output directory.

import argparse
import glob
from nltk.tokenize import wordpunct_tokenize
from os import makedirs, mkdir
from shutil import copyfile


def process_data(language):
    """Check the number of tokens for each .txt file in the dataset. Copy those that have between 380 and 2500 tokens
    to the output directory. """
    x = []
    for path in glob.glob('{}{}/*.txt'.format(args.input, language)):
        with open(path, 'r') as file_handle:
            tokens = 0
            for line in file_handle:
                tokens += len(wordpunct_tokenize(line))
            if 380 < tokens < 2500:
                x.append(path)
    for path in x:
        copyfile(path, path.replace(args.input, args.output))


def main():
    try:
        makedirs(args.output, exist_ok=True)
    except FileExistsError:
        pass
    for lang in ['DE', 'EN', 'ES', 'FR', 'IT', 'NL']:
        try:
            mkdir(args.output + lang)
        except FileExistsError:
            pass
        print('Processing data for {}'.format(lang))
        process_data(lang)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='The location of the full dataset')
    parser.add_argument('output', type=str,
                        help='The location where selected files should be placed. (Will be created when necessary)')
    args = parser.parse_args()
    if args.input[-1] != '/':
        args.input += '/'
    if args.output[-1] != '/':
        args.output += '/'
    main()
