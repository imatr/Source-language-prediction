#!/usr/bin/env python3

# This script analyses the language tags in the Europarl corpus. It will only select
# speeches that are available in English, and if they are originally in English,
# it will check that the text is produced by a MEP from the UK.

import argparse
import glob
import gzip
import os
import xml.etree.ElementTree as ET
from collections import defaultdict
from whoswho import who


def get_available():
    '''
    Creates a set that contains information on whether a speech can be found in the English part of Europarl.
    The information represented by a tuple in the format (file-ID, speaker-ID).
    '''
    available = set()
    for path in glob.glob('./en/*.xml.gz'):
        report_code = path.split('/')[-1][:-7]
        with gzip.open(path, 'rb') as file_handle:
            tree = ET.fromstring(file_handle.read())
        for fragment in tree.findall('.//SPEAKER[@ID]'):
            available.add((report_code, fragment.get('ID')))
    return available


def is_british(name):
    '''Returns whether a speaker is likely to be an MEP from the United Kingdom'''
    for possible_name in en_meps:
        if who.match(name, possible_name):
            return True
    return False


def main():
    id_to_lang = defaultdict(set)
    available = get_available()
    # Search through the corpus and put all speeches that were said by UK MEPS in English,
    # and all speeches that were not said in English, but do have a language tag in a dictionary.
    for path in glob.glob('{}*/*.xml.gz'.format(args.path)):
        report_code = path.split('/')[-1][:-7]
        with gzip.open(path, 'rb') as file_handle:
            tree = ET.fromstring(file_handle.read())
        for fragment in tree.findall('.//SPEAKER[@LANGUAGE]'):
            if fragment.get('LANGUAGE') != 'EN' or (
                            fragment.get('LANGUAGE') == 'EN' and is_british(fragment.get('NAME'))):
                id_to_lang[(report_code, fragment.get('ID'))].add(fragment.get('LANGUAGE'))
    file_handles = dict()
    # Create a folder where all information can be stored
    if not os.path.exists('./fragment_data'):
        os.mkdir('./fragment_data')
    # Go through the collected data, and write the file-IDs and speaker-IDs to files:
    # If the speech is not available in English, ignore it.
    # If there are multiple language tags for a single fragment, ignore it.
    # The filenames are based on the spoken language.
    # The information is written as "FileID,SpeakerID" (without quotes, one tuple per line).
    for key in id_to_lang:
        if len(id_to_lang[key]) == 1:
            language = id_to_lang[key].pop()
            if language not in file_handles:
                file_handles[language] = open('./fragment_data/{}.txt'.format(language), 'w')
            if key in available:
                print('{},{}'.format(*key), file=file_handles[language])
            for language in file_handles:
                file_handles[language].close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='The path where the \'raw\' folder of Europarl can be found.')
    parser.add_argument('meps', type=str, help='The path where a list of MEPs can be found.')
    args = parser.parse_args()
    # Add a slash at the end of the path, if it is missing
    if args.path[-1] != '/':
        args.path += '/'
    en_meps = set()
    with open(args.meps, 'r') as fh:
        for line in fh:
            en_meps.add(line)
    main()
