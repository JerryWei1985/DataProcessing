#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import argparse, os, sys, re
import Tools.compute_wer

def errorPrint(string):
    print(string, file=sys.stderr)

class Summarizer:
    def __init__(self, transPath, resultPath,
                 wavPath, domainPath, useID=False):
        self.transPath = self._checkPath(transPath)
        self.resultPath = self._checkPath(resultPath)
        self.wavPath = self._checkPath(wavPath) if useID else wavPath
        self.domainPath = self._checkPath(domainPath)
        self.useID = useID
        self.idMap = {}
        self.LoadDomainList()
        self.ParseTestSet()
        self.domainRegx = None

    def _checkPath(self, path):
        if os.path.exists(path):
            return path
        errorPrint("%s doesn't exit." % path)
        sys.exit(-1)

    def LoadDomainList(self):
        errorPrint('load domain list: %s' % self.domainPath)
        regexStr = ''
        with open(self.domainPath) as inf:
            for line in inf:
                line = line.strip()
                if line.startswith('#') or len(line) == 0:
                    continue
                regexStr = '%s%s%s' %(regexStr, '|' if len(regexStr) > 0 else '', line)
        if len(regexStr) == 0:
            errorPrint('domain list is empty.')
            sys.exit(-1)
        self.domainRegx = re.compile('(%s)' % regexStr)
        errorPrint('finish loading.')

    def LoadTestSet(self, filePath, idMap, col=1):
        with open(filePath) as inf:
            for line in inf:
                line = line.strip().split()
                if len(line) < col:
                    continue
                domain = self.domainRegx.search(line[col - 1])
                if domain:
                    if line[0] not in idMap:
                        idMap[line[0]] = domain.group(1)

    def ParseTestSet(self):
        if self.useID:
            self.LoadTestSet(self.resultPath, self.idMap)
        else:
            self.LoadTestSet(self.wavPath, self.idMap, 2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--trans', '-t', required=True, help='transcription path')
    parser.add_argument('--wav', '-w', help='wav scp path')
    parser.add_argument('--result', '-r', required=True, help='asr test result path')
    parser.add_argument('--domain', '-d', required=True, help='domain name list path')
    parser.add_argument('--match', choices=['id', 'path'], default='id', help='')
    args = parser.parse_args()

if __name__ == '__main__':
    main