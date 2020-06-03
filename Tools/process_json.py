#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os
import json
import argparse

def parse_json(input_file, output_file):
    input_s = open(input_file)
    data = json.load(input_s)
    with open(output_file, 'w') as of:
        for item in data:
            item_data = item['map']
            if 'content' in item_data:
                content = item_data['content']
                of.write(content + '\n')
            if 'comments' in item_data:
                comments = item_data['comments']
                if 'list' in comments:
                    of.write('\n'.join(comments['list']) + '\n')
    input_s.close()

def parse_list(input_list, output_folder):
    if not os.path.exists(output_folder) and output_dir:
        os.makedirs(output_folder)
    with open(input_list, 'r') as inf:
        for line in inf:
            line = line.strip()
            file_name = os.path.basename(line) + '.txt'
            output_file = os.path.join(output_folder, file_name)
            parse_json(line, output_file)

def parse_folder(input_folder, output_folder):
    if not os.path.exists(output_folder) and output_dir:
        os.makedirs(output_folder)
    for _, _, files in os.walk(input_folder):
        for f in files:
            output_file = os.path.join(output_folder, f + '.txt')
            input_file = os.path.join(input_folder, f)
            parse_json(input_file, output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--text', '-t', default=None)
    parser.add_argument('--output-file', '-f', default=None)
    parser.add_argument('--input-list', '-fl', default=None)
    parser.add_argument('--input-folder', '-if', default=None)
    parser.add_argument('--output-folder', '-of', default=None,)
    args = parser.parse_args()

    if not args.text and not args.input_list and not args.input_folder:
        parser.error('No input.')
    if not args.output_file and not args.output_folder:
        parser.error('No output.')
    if (args.input_folder or args.input_list) and not args.output_folder:
        parser.error('Folder or list input need folder output: "--output-folder".')

    if args.text and args.output_file:
        output_dir = os.path.dirname(args.output_file)
        if not os.path.exists(output_dir) and output_dir:
            os.makedirs(output_dir)
        parse_json(args.text, args.output_file)
    if args.text and not args.output_file:
        if not os.path.exists(args.output_folder):
            os.makedirs(args.output_folder)
        file_name = os.path.basename(args.text) + '.txt'
        output_file = os.path.join(args.output_folder, file_name)
        parse_json(args.text, output_file)
    if args.input_list:
        parse_list(args.input_list, args.output_folder)
    if args.input_folder:
        parse_folder(args.input_folder, args.output_folder)
