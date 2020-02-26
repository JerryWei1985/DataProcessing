#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import re, argparse, sys

class PostProcessor:

    def __init__(self, lex = None, mapping = None):
        self.lexiconPath = lex
        self.mappingPath = mapping
        self.lexicon = set()
        self.isMatch = None
        self.englishRegex = re.compile('[0-9a-zA-Z\']+')
        self.whiteCharRegex = re.compile('\\s{2,}')
        self.quotRegex = re.compile("'")
        self.numberEnglishRegex = re.compile('[2345678][ADGMPS]')
        self.CCTVRegex = re.compile('CCTV1?[0-9]')
        self.voc = {}
        if lex:
            self.LoadLexicon()
        if mapping:
            self.LoadMapping()

    def LexiconPath(self):
        return self.lexiconPath

    def Lexicon(self):
        return self.lexicon

    def SetLexiconPath(self, lex):
        self.lexiconPath = lex
        self.LoadLexicon()

    def SetMappingPath(self, mapping):
        self.mappingPath = mapping
        self.LoadMapping()

    def LoadMapping(self):
        if not self.mappingPath:
            self.isMatch = None
            return
        with open(self.mappingPath) as inf:
            regexStr = ''
            self.mappingDic = {}
            for line in inf:
                line = line.strip().split('\t')
                self.mappingDic[line[0]] = (line[2], re.compile(line[1]))
                regexStr += '|' + line[1]
            self.isMatch = re.compile(regexStr.strip('|'))

    def ProcessCCTVMatch(self, matchObj):
        return matchObj.group(0) + ' '

    def ProcessNumEnMatch(self, matchObj):
        pass

    def ProcessEngMatch(self, matchObj):
        if matchObj.group(0) in self.lexicon:
            return matchObj.group(0)
        tmpStr = self.quotRegex.sub(' ', matchObj.group(0)).strip()
        if len(tmpStr) == 0:
            return ''
        tmpStr = self.CCTVRegex.sub(self.ProcessCCTVMatch, tmpStr)
        return tmpStr

    def ProcessMappingMatch(self, matchObj):
        if len(matchObj.groups()) <= 0:
            return self.mappingDic[matchObj.re.pattern]
        else:
            tmp = self.mappingDic[matchObj.re.pattern]
            for i in range(len(matchObj.groups())):
                i += 1
                tmp = tmp.replace('\\%d' % i, matchObj.group(i))
            return tmp

    def ProcessMapping(self, string):
        tmp = string
        while True:
            repMatch = self.isMatch.search(tmp)
            if repMatch:
                matchStr = repMatch.group(0)
                replaceDic = self.mappingDic[matchStr]
                tmp = replaceDic[1].sub(replaceDic[0], tmp)
            else:
                break
        return tmp

    def LoadLexicon(self):
        if not self.lexiconPath:
            sys.stderr.write('Missing lexicon, please set lexicon.\n')
            sys.exit(-1)
        with open(self.lexiconPath) as lex:
            for line in lex:
                tmp = line.strip().split()
                self.lexicon.add(tmp[0])

    def ProcessData(self, dataPath, outputPath):
        with open(dataPath) as data:
            with open(outputPath, 'w') as output:
                if not self.isMatch:
                    for line in data:
                        output.write(
                            self.whiteCharRegex.sub(
                                ' ', self.englishRegex.sub(
                                    self.ProcessEngMatch, line
                                )
                            )
                        )
                else:
                    for line in data:
                        output.write(
                            self.whiteCharRegex.sub(
                                ' ', self.englishRegex.sub(
                                    self.ProcessEngMatch, self.ProcessMapping(line)
                                )
                            )
                        )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--lexicon', '-l')
    parser.add_argument('--input', '-i')
    parser.add_argument('--mapping', '-m', default='')
    parser.add_argument('--output', '-o')
    argvs = parser.parse_args()

    processor = PostProcessor(argvs.lexicon, argvs.mapping)
    processor.ProcessData(argvs.input, argvs.output)
