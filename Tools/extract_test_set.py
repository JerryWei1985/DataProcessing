#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import argparse, os, sys

class TestSet():
    def __init__(self, trans, wav, wer = ''):
        self.trans = trans
        self.wav = wav
        self.wer = wer

class TestSetParser(object):
    def pathValidate(self, p):
        if not os.path.exists(p):
            raise IOError("%s doesn't exit" % p)
        return p

    def __init__(self, trans, scp):
        self.trans = self.pathValidate(trans)
        self.scp = self.pathValidate(scp)
        self.testSet = self.loadTest()

    def loadTest(self):
        textSet = {}
        testSet = {}
        with open(self.trans, 'r') as intrans:
            for line in intrans:
                tmp = line.strip().split()
                textSet[tmp[0]] = tmp[1:]
        with open(self.scp, 'r') as inscp:
            for line in inscp:
                tmp = line.strip().split()
                if tmp[0] in textSet:
                    testSet[tmp[0]] = TestSet(textSet[tmp[0]], tmp[1:])
        return testSet

    def parseEvaResult(self, eva):
        with open(eva, 'r') as ineva:
            isUtt = False
            uttID = ''
            for line in ineva:
                tmp = line.strip()
                if len(tmp) <= 0:
                    continue
                if tmp.startswith('utt:'):
                    uttID = tmp.split()[1]
                    if uttID in self.testSet:
                        isUtt = True
                elif isUtt and tmp.startswith('WER:'):
                    WER = tmp.split()[1]
                    self.testSet[uttID].wer = WER
                elif isUtt and tmp.startswith('lab:'):
                    lab = ' '.join(tmp.split()[1:])
                elif isUtt and tmp.startswith('rec:'):
                    rec = ' '.join(tmp.split()[1:])
                    uttID = ''
                    isUtt = False

    def checkScp(self, scp=''):
        tmpScp = self.scp
        if scp:
            tmpScp = scp
        if os.path.exists(tmpScp):
            raise IOError("%s doesn't exit." % tmpScp)
        with open(tmpScp, 'r') as inscp:
            print("Begin to check %s" % tmpScp, file=sys.stderr)
            for line in inscp:
                tmp = line.strip().split()
                if not os.path.exists(tmp[1]):
                    print("%s doesn't exit." % tmp[1], file=sys.stderr)
            print("Finish checking %s" % tmpScp, file=sys.stderr)

    def output(self, out):
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--eva', help='')
    parser.add_argument('--trans', help='')
    parser.add_argument('--scp', help='')
    parser.add_argument('--output', '-o', help='')
    argvs = parser.parse_args()

    testSetParser = TestSetParser(argvs.trans, argvs.scp)
    testSetParser.parseEvaResult(argvs.eva)
    testSetParser.output(argvs.output)