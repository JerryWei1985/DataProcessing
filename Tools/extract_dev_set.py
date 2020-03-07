#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os
import sys
import random
import argparse

def generateRandomList(count, max):
    print('Random numbers.')
    numSet = set()
    maxNum = -1
    while len(numSet) < count:
        tmpNum = random.randint(1, max)
        numSet.add(tmpNum)
        if tmpNum > maxNum:
            maxNum = tmpNum
    return numSet, maxNum


def countLines(inputFile):
    count = -1
    print('Counting file: %s' % inputFile)
    with open(inputFile, 'r', errors='ignore') as inf:
        for count, _ in enumerate(inf):
            pass
    count += 1
    return count


def extractDevSet(inputList, outputFolder, outputDevSet, count):
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)
    if not os.path.exists(os.path.dirname(outputDevSet)):
        os.makedirs(os.path.dirname(outputDevSet))
    with open(outputDevSet, 'w') as outDevSet:
        isDuplicate = False
        devSet = set()
        totalCount = 0
        for filePath in inputList:
            totalCount += countLines(filePath)
        print('total count: %d' % totalCount)
        lineNums, _ = generateRandomList(count, totalCount)
        lineNum = 0
        duplicateCount = 0
        for filePath in inputList:
            fileName = os.path.basename(filePath)
            outputPath = os.path.join(outputFolder, fileName)
            with open(outputPath, 'w') as outFile:
                with open(filePath, 'r') as inf:
                    for line in inf:
                        lineNum += 1
                        if lineNum in lineNums and not isDuplicate:
                            if line in devSet:
                                outFile.write(line)
                                duplicateCount += 1
                                isDuplicate = True
                                continue
                            outDevSet.write(line)
                            devSet.add(line)
                        else:
                            if not isDuplicate or line in devSet:
                                if lineNum in lineNums:
                                    duplicateCount += 1
                                outFile.write(line)
                            else:
                                outDevSet.write(line)
                                devSet.add(line)
                                if lineNum not in lineNums:
                                    duplicateCount -= 1
                                if duplicateCount <= 0 and isDuplicate:
                                    isDuplicate = False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i',
                        help='Input folder path or file list path.')
    parser.add_argument('--output_folder', '-o',
                        help='Output folder for training data.')
    parser.add_argument('--output_dev', '-d',
                        help='dev set file.')
    parser.add_argument('--count', '-c', type=int)
    args = parser.parse_args()

    if not os.path.exists(args.input):
        parser.error("%s doesn't exist.\n" % args.input)

    fileList = []
    if os.path.isfile(args.input):
        with open(args.input) as inf:
            for line in inf:
                tmpLine = line.strip()
                if len(tmpLine) == 0 or tmpLine.startswith('#'):
                    continue
                fileList.append(line.strip())
    else:
        for r, d, f in os.walk(args.input):
            for fileName in f:
                filePath = os.path.join(r, fileName)
                fileList.append(filePath)

    extractDevSet(fileList, args.output_folder, args.output_dev, args.count)
