#!/usr/bin/env python3

# This program will create text files from the raw xml files in Europarl.
# It requires the files created by the find_fragments program.

import glob
import argparse
import gzip
import os
import xml.etree.ElementTree as ET
from collections import defaultdict


def main():
    # Languages of interest
    languages = ['EN', 'DE', 'FR', 'NL', 'IT', 'ES']
    report_id_language_dict = defaultdict(dict)
    # Create a directory for each language of interest (when necessary)
    for language in languages:
        if not os.path.exists('{}/{}'.format(args.metadata, language)):
            os.mkdir('{}/{}'.format(args.metadata, language))
        with open('{}/{}.txt'.format(args.metadata, language)) as file_handle:
            for line in file_handle:
                report_code, speaker_id = line.strip().split(',')
                report_id_language_dict[report_code][speaker_id] = language
    # Read the gzipped xml files, and put every sentence spoken on a new line in a text file.
    # This will create one text file for every FileID,SpeakerID pair.
    for report_code in report_id_language_dict:
        with gzip.open('{}/en/{}.xml.gz'.format(args.path, report_code)) as file_handle:
            tree = ET.fromstring(file_handle.read())
            for speaker_id in report_id_language_dict[report_code]:
                fragment = tree.find('.//SPEAKER[@ID=\'{}\']'.format(speaker_id))
                with open('{}/{}/{}.{}.txt'.format(args.metadata,
                                                   report_id_language_dict[report_code][speaker_id],
                                                   report_code, speaker_id), 'w') as file_handle:
                    for sentence in fragment.findall('.//s'):
                        print(sentence.text, file=file_handle)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='The path where the \'raw\' folder of Europarl can be found.')
    parser.add_argument('metadata', type=str, help='The path where the fragment_data folder can be found.')
    args = parser.parse_args()
    # Remove the slash at the end of the path, if it is present
    if args.path[-1] == '/':
        args.path = args.path[:-1]
    if args.metadata[-1] == '/':
        args.metadata = args.metadata[:-1]
    main()
