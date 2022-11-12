#!/usr/bin/env python3

import csv
import hashlib
import os
import os.path as path
import random
import glob
import pandas as pd
import sys
import argparse

DIR = path.abspath(path.dirname(__file__))
FILES = {
    'clothing.csv': ('Blouses', 'Shirts', 'Tanks', 'Cardigans', 'Pants', 'Capris', '"Gingham" Shorts',),
    'accessories.csv': ('Watches', 'Wallets', 'Purses', 'Satchels',),
    'household_cleaners.csv': ('Kitchen Cleaner', 'Bathroom Cleaner',),
}


def write_file(writer, length, categories):
    writer.writerow(['email_hash', 'category'])
    for i in range(0, length):
        writer.writerow([
            hashlib.sha256('tech+test{}@pmg.com'.format(i).encode('utf-8')).hexdigest(),
            random.choice(categories),
        ])

# takes all the csv files in the fixtures folder and converts all the information to a pandas data frame, with the addition of the
# filename column
def read_files_to_data_frame():
    files = parse_cmd_line()
    data_frame = pd.DataFrame()
    for file in files:
        df = pd.read_csv(file, index_col=None)
        df['filename'] = pd.Series([os.path.basename(file) for x in range(len(df.index))])

        data_frame = data_frame.append(df)
    return data_frame

def csv_combiner():
    data_frame = read_files_to_data_frame()
    data_frame.to_csv('combined.csv', index = False)

def parse_cmd_line():
    n = len(sys.argv)
    file_inputs = []
    for i in range(1, n):
        file_inputs.append(sys.argv[i])
    return file_inputs
    # parser = argparse.ArgumentParser()
    # args = parser.parse_args()
    # if args.Output:

def main():
    for fn, categories in FILES.items():
        with open(path.join(DIR, 'fixtures', fn), 'w', encoding='utf-8') as fh:
            write_file(
                csv.writer(fh, doublequote=False, escapechar='\\', quoting=csv.QUOTE_ALL),
                random.randint(100, 1000),
                categories
            )
    csv_combiner()
    parse_cmd_line()


if __name__ == '__main__':
    main()
