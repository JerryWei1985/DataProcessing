#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import re
import os
import argparse

duration_re_str = r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}'
duration_start_num_re = re.compile(r'^\d+$')
duration_line_re = re.compile(duration_re_str)

def extract_title(file_path):
    tmp_title = os.path.basename(file_path)
    index = tmp_title.strip('.zh-tw.srt').rfind('-')
    tmp_title = tmp_title[0: index]
    return tmp_title

def load_file(file_path):
    print('process {}'.format(file_path))
    text = []
    with open(file_path) as inf:
        title = extract_title(file_path)
        text.append(title)
        for line in inf:
            tmp = line.strip()
            if (len(tmp) <= 0 or
                duration_start_num_re.match(tmp) or
                duration_line_re.match(tmp)):
                continue
            else:
                text.append(tmp)
    return ' '.join(text)

def output(content, output_path):
    output_folder = os.path.dirname(output_path)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    with open(output_path, 'a') as of:
        of.write(content + '\n')

def scan_folder(input_folder, output_file):
    for root, _, files in os.walk(input_folder):
        for file in files:
            file_path = os.path.join(root, file)
            content = load_file(file_path)
            output(content, output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-folder', '-i')
    parser.add_argument('--output-file', '-o')
    args = parser.parse_args()
    scan_folder(args.input_folder, args.output_file)
