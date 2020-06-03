#!/usr/bin/env python3
#-*- coding:utf-8 -*-

"""
Merge 36kr crawled data.
"""

import os
import argparse

def scan_root(root_folder, output_folder):
    dirs = os.listdir(root_folder)
    for d in dirs:
        folder = os.path.join(root_folder, d)
        scan_folder(folder, output_folder)

def scan_folder(input_folder, output_folder):
    dirs_date = os.listdir(input_folder)
    for dir_date in dirs_date:
        year = os.path.basename(input_folder)
        date = '{}-{}'.format(year, dir_date)
        folder = os.path.join(input_folder, dir_date)
        scan_files(folder, output_folder, date)

def scan_files(input_folder, output_folder, date_str):
    print('Process {}.'.format(input_folder))
    year = date_str.split('-')[0]
    date = '-'.join(date_str.split('-')[1:])
    dirs_cat = os.listdir(input_folder)
    if os.path.isfile(os.path.join(input_folder, dirs_cat[0])):
        output_f = os.path.join(output_folder, year)
        if not os.path.exists(output_f):
            os.makedirs(output_f)
        output_file_name = date_str + '.txt'
        output_file = os.path.join(output_f, output_file_name)
        with open(output_file, 'w') as of:
            for f in dirs_cat:
                with open(os.path.join(input_folder, f), 'r') as inf:
                    for line in inf:
                        of.write(line)
    else:
        output_f = os.path.join(output_folder, year, date)
        if not os.path.exists(output_f):
            os.makedirs(output_f)
        for dir_cat in dirs_cat:
            output_file_name = '{}_{}.txt'.format(dir_cat, date_str)
            output_file = os.path.join(output_f, output_file_name)
            if os.path.exists(output_file):
                continue
            with open(output_file, 'w') as of:
                folder = os.path.join(input_folder, dir_cat)
                for r, _, files in os.walk(folder):
                    for f in files:
                        with open(os.path.join(r, f), 'r') as inf:
                            for line in inf:
                                of.write(line)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-folder', '-i')
    parser.add_argument('--output-folder', '-o')
    args = parser.parse_args()

    scan_root(args.input_folder, args.output_folder)
