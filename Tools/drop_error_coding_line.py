#!/usr/bin/env python2
#-*- coding:utf-8 -*-

import os
import argparse
import multiprocessing

def filter_data(input_file, output_file):
    print('Process %s' % input_file)
    with open(input_file, 'r') as inf:
        with open(output_file, 'w') as of:
            for line in inf:
                try:
                    line.decode('utf-8')
                    of.write(line)
                except:
                    continue

def filter_data_list(input_list, output_folder, process_count=2):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    pool = multiprocessing.Pool(process_count)
    with open(input_list) as inf:
        for line in inf:
            line = line.strip()
            if line.startswith('#'):
                continue
            output_file_name = os.path.basename(line)
            output_file_path = os.path.join(output_folder, output_file_name)
            pool.apply_async(filter_data, (line, output_file_path))
    pool.close()
    pool.join()

def filter_data_folder(input_folder, output_folder, process_count=2):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    pool = multiprocessing.Pool(process_count)
    for root, _, files in os.walk(input_folder):
        for f in files:
            input_path = os.path.join(root, f)
            output_path = os.path.join(output_folder, f)
            pool.apply_async(filter_data, (input_path, output_path))
    pool.close()
    pool.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', '-i', nargs='+', default=[])
    parser.add_argument('--output-file', '-o', default=[])
    parser.add_argument('--input-list', '-il', nargs='+', default=[])
    parser.add_argument('--input-folder', '-if', nargs='+', default=[])
    parser.add_argument('--output-folder', '-of', default='')
    parser.add_argument('--process-count', default=0)
    args = parser.parse_args()

    if not args.input_file and not args.input_list and not args.input_folder:
        parser.error('No input data.')
    if not args.output_file and not args.output_folder:
        parser.error('No output path.')
    if (args.input_list or args.input_folder) and not args.output_folder:
        parser.error('"--input-list" or "--input-folder" is set, '
                     'but missing "--output-folder".')
    if len(args.input_file) > 1 and not args.output_folder:
        parser.error('input files are more than one, '
                     'but missing "--output-folder".')

    cpu_core = multiprocessing.cpu_count() if not args.process_count else args.process_count

    if args.input_list:
        for input_list in args.input_list:
            filter_data_list(input_list, args.output_folder, cpu_core)
    if args.input_folder:
        for folder in args.input_folder:
            filter_data_folder(folder, args.output_folder, cpu_core)
    if len(args.input_file) == 1:
        if not os.path.exists(args.output_folder):
            os.makedirs(args.output_folder)
        filter_data(args.input_file[0], args.output_file)
    elif len(args.input_file) > 1:
        if not os.path.exists(args.output_folder):
            os.makedirs(args.output_folder)
        for f in args.input_file:
            file_name = os.path.basename(f)
            output_file_path = os.path.join(args.output_folder, file_name)
            filter_data(f, output_file_path)
