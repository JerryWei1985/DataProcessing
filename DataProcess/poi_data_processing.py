#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import argparse
import os
import sys

from DataProcessing.DataProcess.pylib.POIAreas import ChineseAreas

class POI(object):
    def __init__(self, inputs, separator=['\t']):
        self._separator = separator
        self._inputs = inputs
        self._outputRoot = ''
        self._chineseAreas = ChineseAreas()

    def _setOutput(self, root, nameHead=''):
        nameHead = nameHead.strip()
        self._outputRoot = root
        if not os.path.exists(self._outputRoot):
            os.makedirs(self._outputRoot)
        paths = {}
        if nameHead and '_' != nameHead:
            nameHead += '_'
        for key in self._chineseAreas.GetAreasCode():
            if not key:
                continue
            paths[key] = open(os.path.join(self._outputRoot, '{}{}.txt'.format(nameHead, key)), 'w')
        return paths

    def _cleanOutput(self, streams):
        for key in streams:
            streams[key].close()

    def _splitDataByAreas(self, outStreams, col):
        for inFile in self._inputs:
            with open(inFile, 'r') as inf:
                print('Reading "{}" ...'.format(inFile))
                lineNum = 0
                tmpNum = 0
                for line in inf:
                    lineNum += 1
                    tmpNum += 1
                    if tmpNum >= 65000:
                        print('\r', lineNum, end='')
                        tmpNum = 0
                    tmp = line.strip().split(self._separator)
                    province = tmp[col]
                    areaCode = self._chineseAreas.GetAreaCode(province)
                    if areaCode:
                        outStreams[areaCode].write(line)
                    else:
                        print('\r"{}" is not support.'.format(province), file=sys.stderr)
                print('\r', lineNum)

    def SplitArea(self, outRoot, col=0, nameHead=''):
        try:
            streams = self._setOutput(outRoot, nameHead)
            self._splitDataByAreas(streams, col)
        finally:
            self._cleanOutput(streams)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', nargs='+', required=True, help='input list')
    parser.add_argument('--output', '-o', required=True, help='output folder path')
    parser.add_argument('--filename', '-f', required=False, default='', help='a head in file name')
    parser.add_argument('--separator', '-s', required=False, default='\t', help='separator in file')
    parser.add_argument('--column', '-c', type=int, required=False, default=0, help='column index in file.')
    args = parser.parse_args()

    poiFile = POI(args.input, args.separator)
    poiFile.SplitArea(args.output, args.column, args.filename)