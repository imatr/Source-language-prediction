#!/usr/bin/env python3

# This script will create versions of text files where all tokens have been replaced by their
# part-of-speech tag.

import argparse
import glob
from nltk import pos_tag
from nltk.tokenize import wordpunct_tokenize


def main():
    # Get a list of files to create tagged versions of
    filenames = glob.glob('{}/*/*.txt'.format(args.path))
    total = len(filenames)
    # Convert every file to its tagged version
    for i, path in enumerate(filenames):
        with open(path, 'r') as file_handle:
            with open(path+args.extension, 'w') as file_handle2:
                for line in file_handle:
                    if args.features == 'POS':
                        print(' '.join([pos for _, pos in pos_tag(wordpunct_tokenize(line))]), file=file_handle2)
                    elif args.features == 'POS-universal':
                        print(' '.join([pos for _, pos in pos_tag(wordpunct_tokenize(line), tagset='universal')]), file=file_handle2)
        # Print progress every 100 files
        if i % 100 == 0:
            print('{}/{} files tagged'.format(i, total))
    # Show that the program is finished
    print('All files tagged')

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='The location of the training data', type=str)
    parser.add_argument('-f', '--features', default='POS', help='The type of features to use (default: %(default)s)', choices=['POS', 'POS-universal'])
    args = parser.parse_args()
    # Format paths as required
    if args.path and args.path[-1] == '/':
        args.path = args.path[:-1]
    if args.features:
        extensions = {'POS': '.pos', 'POS-universal': '.uni'}
        args.extension = extensions[args.features]
    # Run the main function
    main()
