#!/usr/bin/env python3

# This script will create versions of text files where all tokens have been replaced by
# parse rules representing the relationship between tokens. The format of these rules is
# MAIN_DEPENDENCY DEPENDENCY_IN_SUBTREE [DEPENDENCY_IN_SUBTREE] ...

import argparse
import glob
import spacy


def main():
    nlp = spacy.load('en_core_web_md')
    # Get a list of files to create parse rules for
    filenames = glob.glob('{}/*/*.txt'.format(args.path))
    total = len(filenames)
    # Convert every file to parse rules
    # Every parse rule has the following format:
    # Dependency A B C
    # Where A B C are the dependencies of all tokens in the subtree of the token that has
    # its dependency as the first token of a line.
    # Please note that one should edit the classify_sk program in order to actually use
    # these rules, as the current configuration does NOT consider the order of the
    # features. This can be done by replacing the tokenizer by a function that returns a
    # list of lines instead of a list of tokens/POS-tags.
    for i, path in enumerate(filenames):
        with open(path, 'r') as file_handle:
            with open(path+'.parse', 'w') as file_handle2:
                for line in file_handle:
                    parse = nlp(line)
                    for token in parse:
                        subtree = [t for t in token.subtree]
                        if len(subtree) > 1:
                            print(token.pos_, ' '.join([sub.pos_ for sub in subtree if sub != token]), file=file_handle2)
        # Print progress every 100 files
        if i % 100 == 0:
            print('{}/{} files processed'.format(i, total))
    # Show that the program is finished
    print('All files processed')

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='The location of the training data', type=str)
    args = parser.parse_args()
    # Format paths as required
    if args.path and args.path[-1] == '/':
        args.path = args.path[:-1]
    # Run the main function
    main()
