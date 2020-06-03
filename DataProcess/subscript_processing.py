#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import argparse
import os
import re
import sys
import chardet
from enum import Enum, unique


@unique
class ScriptStyle(Enum):
    SRT = 0
    ASS = 1
    SSA = 2
    OTHER = 3
    SUB = 4
    

class ParseError(Exception):
    pass


class SubscriptProcesser(object):

    def __init__(self, data_path, style=ScriptStyle.SRT):
        self.number_re = re.compile(r'^[0-9]+$')
        self.time_duration_re = re.compile(
            r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}')
        self.eng_re = re.compile(
            r'^[a-zA-Z♪\s,.!?，！？<>\\//:\-+=_(){}\[\];；~～*&%@\'"0-9]+$')
        self.noise_re = re.compile(r'{[^}]+}')
        self.script_style = style
        self.data_path = data_path
        tmp_style = SubscriptProcesser.get_script_style(self.data_path)
        if tmp_style == ScriptStyle.SUB:
            print("Don't support *.sub.", file=sys.stderr)
            sys.exit(1)
        if tmp_style != ScriptStyle.OTHER:
            self.script_style = tmp_style

    @classmethod
    def get_script_style(cls, data_path):
        ext = os.path.splitext(data_path)[-1][1:].lower()
        if ext == 'srt':
            return ScriptStyle.SRT
        elif ext == 'ass':
            return ScriptStyle.ASS
        elif ext == 'ssa':
            return ScriptStyle.SSA
        elif ext == 'sub':
            return ScriptStyle.SUB
        else:
            return ScriptStyle.OTHER

    @classmethod
    def is_support_format(cls, data_path):
        input_sub_style = SubscriptProcesser.get_script_style(data_path)
        if (input_sub_style == ScriptStyle.OTHER or
            input_sub_style == ScriptStyle.SUB):
            return False
        return True

    @classmethod
    def read_text(cls, data_path):
        bom = b'\xef\xbb\xbf'
        exist_bom = lambda s: True if s == bom else False
        f = open(data_path, 'rb')
        f_body = f.read()
        f.close()
        if exist_bom(f_body[:3]):
            return f_body[3:]
        else:
            return f_body

    @classmethod
    def decode_bytes(cls, bytes_data):
        pass

    def extract_srt(self):
        chs_list = []
        eng_list = []
        byte_data = SubscriptProcesser.read_text(self.data_path)
        dicts = chardet.detect(byte_data)
        encoding = dicts['encoding']
        if dicts['confidence'] < 0.7:
            encoding = 'utf-8'
        try:
            str_data = byte_data.decode(encoding)
        except UnicodeDecodeError:
            str_data = byte_data.decode('gb18030')
        is_start = True
        is_empty = True
        for line in str_data.split('\n'):
            tmp_line = line.strip()
            if not tmp_line:
                is_empty = True
                continue
            elif (self.number_re.match(tmp_line) and
                  (is_start or is_empty)):
                is_empty = False
                continue
            elif (self.time_duration_re.match(tmp_line)):
                is_empty = False
                continue
            elif self.eng_re.match(tmp_line):
                is_empty = False
                eng_list.append(tmp_line)
            else:
                is_empty = False
                chs_list.append(tmp_line)
            is_start = False
        return chs_list, eng_list

    def extract_ass(self):
        chs_list = []
        eng_list = []
        byte_data = SubscriptProcesser.read_text(self.data_path)
        dicts = chardet.detect(byte_data)
        encoding = dicts['encoding']
        if dicts['confidence'] < 0.7:
            encoding = 'utf-8'
        try:
            str_data = byte_data.decode(encoding)
        except UnicodeDecodeError:
            str_data = byte_data.decode('gb18030')
        for line in str_data.split('\n'):
            tmp_line = line.strip()
            if not tmp_line:
                continue
            elif tmp_line.startswith('Dialogue'):
                cols = tmp_line.split(':')[1].strip().split(',')
                text = ','.join(cols[9:])
                text = self.noise_re.sub('', text)
                tmp_text = text.split(r'\N')
                for item in tmp_text:
                    if self.eng_re.match(item):
                        eng_list.append(item)
                    else:
                        chs_list.append(item)
        return chs_list, eng_list

    def extract_content(self):
        if self.script_style == ScriptStyle.SRT:
            return self.extract_srt()
        elif (self.script_style == ScriptStyle.ASS or
              self.script_style == ScriptStyle.SSA):
            return self.extract_ass()
        else:
            raise ParseError() from None

    def output(self, output_path):
        chs_list, _ = self.extract_content()
        if chs_list:
            with open(output_path, 'w') as output_os:
                for item in chs_list:
                    output_os.write(item)


def normalize_name(file_path):
    re_str = r'(?:[简繁]体|[英中]文|[ce]n|chs|eng|zh-hans|zh-hant|cht|chn)'
    file_ext_re = re.compile(
        '[._-]{0}(?:[_&\\-]{0})?\\.(?:ass|srt|ssa)$'.format(re_str))
    file_name = os.path.basename(file_path).lower()
    file_name = file_ext_re.sub('', file_name)
    return file_name


def parse_folder(input_folder):
    for root, dirs, files in os.walk(input_folder):
        for f in files:
            file_path = os.path.join(root, f)
            if not SubscriptProcesser.is_support_format(file_path):
                continue
            else:
                yield file_path
        for d in dirs:
            folder_path = os.path.join(root, d)
            parse_folder(folder_path)

def parse_sub_file(input_path, output_folder, file_name_set):
    input_file_name = normalize_name(input_path) + '.txt'
    if input_file_name not in file_name_set:
        output_path = os.path.join(output_folder, input_file_name)
        file_name_set.add(input_file_name)
        processer = SubscriptProcesser(input_path)
        processer.output(output_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='',
                        help='Subscript file path.')
    parser.add_argument('--input-folder', default='',
                        help="Subscript files' folder path.")
    parser.add_argument('--input-list', default='',
                        help="Subscript files' list path.")
    parser.add_argument('--output-text', default='',
                        help='Output file path.')
    parser.add_argument('--output-folder', default='',
                        help="Output files' folder path.")
    args = parser.parse_args()
    output_path = args.output_text
    output_folder = args.output_folder
    file_name_set = set()
    if args.input:
        if not SubscriptProcesser.is_support_format(args.input):
            print('Not support input file.')
            raise ParseError()
        if not args.output_text and not args.output_folder:
            parser.error('Missing output path. '
                         'Need --output-text or --output-folder.')
        elif args.output_text and args.output_folder:
            parser.error('Just need one of "--output-text"/"--output-folder".')
        elif not output_path:
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            input_file_name = normalize_name(args.input) + '.txt'
            output_path = os.path.join(output_folder, input_file_name)
            file_name_set.add(input_file_name)
        processer = SubscriptProcesser(args.input)
        processer.output(output_path)
    if args.input_folder or args.input_list:
        if not args.output_folder:
            parser.error('Missing --output-folder.')
        elif not os.path.exists(output_folder):
            os.makedirs(output_folder)
    eng_sub_re = re.compile(
        '\\.?(?:eng|en|enu|en-us|en_us|英文|英)\\.(?:ass|srt|ssa)$')
    tmp = set()
    if args.input_folder:
        for f in parse_folder(args.input_folder):
            if eng_sub_re.search(f):
                tmp.add(f)
            else:
                print('parse {}'.format(f))
                parse_sub_file(f, output_folder, file_name_set)
    if args.input_list:
        with open(args.input_list) as in_list:
            for line in in_list:
                line = line.strip()
                if eng_sub_re.search(f):
                    tmp.add(line)
                else:
                    print('parse {}'.format(line))
                    parse_sub_file(line, output_folder, file_name_set)
    for f in tmp:
        print('parse {}'.format(f))
        parse_sub_file(f, output_folder, file_name_set)
