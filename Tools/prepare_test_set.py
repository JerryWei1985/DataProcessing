#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os, re, argparse
from enum import Enum

TestSetMode = Enum('TestSetMode', ('jv', 'log', 'mapping'))

class TestSetGenerator(object):
    def __init__(self, inputPath, outputFolder, normalizePath = True,
                 categoryMapping = None, mode = TestSetMode.jv):
        self.mode = mode
        self.input = inputPath
        self.output = outputFolder
        self.isNormalizePath = normalizePath
        self.catMapping = self.loadCatMapping(categoryMapping)
        self.IDRe = re.compile('[^a-zA-Z0-9_\\-]')
        self.normalizeIDRe = re.compile('[-_]{2,}')
        if not os.path.exists(self.input):
            raise IOError("%s dosen't exit." % self.input)

    def loadCatMapping(self, categoryMapping):
        if not categoryMapping:
            return None
        categoryDic = {}
        with open(categoryMapping) as catIn:
            for line in catIn:
                tmp = line.strip().split()
                if len(tmp) <= 0:
                    continue
                catID = os.path.basename(' '.join(tmp[1:])).rstrip('.wav')
                categoryDic[catID] = tmp[0].lower()
        return categoryDic
    
    def normalizePath(self, path):
        if self.isNormalizePath:
            path = path[:path.rfind('_')] + '.wav'
        path = path.replace(' ', '_')
        return path

    def normalizeID(self, id):
        id = self.IDRe.sub('', id)
        id = self.normalizeIDRe.sub('_', id).strip('_')
        return id

    def getJVTrans(self, path):
        path = path[path.rfind('_') + 1:].rstrip('.wav')
        return path

    def generateJVTestSet(self, transMap = None, rootPath = None):
        wavs = {}
        for root, _, files in os.walk(self.input):
            if not rootPath:
                rootPath = root
            for wav in files:
                if wav.endswith('.wav'):
                    path = os.path.join(rootPath, wav)
                    normalizedPath = self.normalizePath(path)
                    os.rename(path, normalizedPath)
                    wavs[wav.rstrip('.wav')] = normalizedPath

        correctedTransDic = {}
        if transMap:
            with open(transMap) as inMap:
                for line in inMap:
                    tmp = line.strip().split()
                    if len(tmp) == 0:
                        continue
                    tmpName = os.path.basename(tmp[0]).rstrip('.wav')
                    correctedTransDic[tmpName] = ' '.join(tmp[1:])
        
        if not os.path.exists(self.output):
            os.makedirs(self.output)

        if self.catMapping:
            tmpCat = {}
            for key in wavs:
                wavid = self.normalizeID(key)
                trans = self.getJVTrans(key)
                if key in self.catMapping:
                    if self.catMapping[key] not in tmpCat:
                        tmpCat[self.catMapping[key]] = [(wavid, trans, wavs[key])]
                        continue
                    tmpCat[self.catMapping[key]].append((wavid, trans, wavs[key]))
            for key in tmpCat:
                print('%s: %d' % (key, len(tmpCat[key])))
                transCatPath = os.path.join(self.output, '%s_trans' % key)
                wavscpCatPath = os.path.join(self.output, '%s_wav.scp' % key)
                with open(transCatPath, 'w') as transOut:
                    with open(wavscpCatPath, 'w') as wavOut:
                        for items in tmpCat[key]:
                            transOut.write('%s %s\n' % (items[0], items[1]))
                            wavOut.write('%s %s\n' % (items[0], items[2]))

        transPath = os.path.join(self.output, 'trans')
        wavscpPath = os.path.join(self.output, 'wav.scp')
        with open(transPath, 'w') as transOut:
            with open(wavscpPath, 'w') as wavOut:
                for key in wavs:
                    wavid = self.normalizeID(key)
                    trans = self.getJVTrans(key)
                    wavOut.write('%s %s\n' % (wavid, wavs[key]))
                    if key in correctedTransDic:
                        transOut.write('%s %s\n' % (wavid, correctedTransDic[key]))
                    else:
                        transOut.write('%s %s\n' % (wavid, trans))

    def generateMappingTestSet(self, rootPath = None):
        pass


def _main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--input', '-i')
    argparser.add_argument('--output', '-o')
    argparser.add_argument('--catlist', '-c', default='')
    argparser.add_argument('--modifylist', '-m', default='')
    args = argparser.parse_args()

    generator = TestSetGenerator(args.input, args.output, True, args.catlist)
    generator.generateJVTestSet(args.modifylist)

if __name__ == '__main__':
    _main()