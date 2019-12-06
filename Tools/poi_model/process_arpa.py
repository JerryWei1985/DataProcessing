#!/usr/bin/env python3
#-*- coding:utf-8 -*-

"""
调节参数有两个：
1. nnet_config中的insertion penalty
2. base arpa中$poi开头的概率的log的变化量
3. poi model本身概率的整体变化量（这个需要想想，有没有什么数学公式可以总结）
"""

import os, sys, re, argparse
from decimal import Decimal, localcontext

class ModelProcessor(object):
    def __init__(self, arpa, output):
        self.arpa = arpa
        self.output = output
        self.arpaInfoMarkRe = re.compile('^(?:\\\\data\\\\|\\\\end\\\\|'
                                         'ngram \\d+=\\d+|\\\\\\d+-grams:)$')

    def process(self, processFunc):
        if not os.path.exists(self.arpa):
            print('"{}" doesn\'t exit'.format(self.arpa), file=sys.stderr)
            exit(-1)
        outputFolder = os.path.dirname(self.output)
        if len(outputFolder) > 0 and not os.path.exists(outputFolder):
            os.makedirs(outputFolder)

        with open(self.output, 'w') as output:
            with open(self.arpa, 'r') as inArpa:
                for line in inArpa:
                    tmpLine = line.strip()
                    if len(tmpLine) == 0 or self.arpaInfoMarkRe.match(tmpLine):
                        output.write(line)
                        continue
                    output.write(processFunc(tmpLine) + '\n')

class BaseModelProcessor(ModelProcessor):
    def __init__(self, arpa, output, delta):
        ModelProcessor.__init__(self, arpa, output)
        self.delta = Decimal(delta)
        self.numRe = re.compile('-?\\d+(?:\\.\\d+)?')
        self.whiteSpace = re.compile('(\\s)')
#        self.delta = [0.2, 0.4, 0.6, 0.8, 1.0,
#                      1.2, 1.4, 1.6, 1.8, 2.0]

    def processPOI(self, line):
        tmp = line.split()
        try:
            if tmp[1] == '$poi':
                sep = self.whiteSpace.search(line).group(1)
                prob = Decimal(tmp[0])
                with localcontext() as ctx:
                    ctx.prec = 6
                    prob += self.delta
                    if prob > 0:
                        prob = 0
                if self.numRe.match(tmp[-1]):
                    return '{}{}{}{}{}'.format(prob, sep,
                    ' '.join(tmp[1:-1]), sep, tmp[-1])
                else:
                    return '{}{}{}'.format(prob, sep, ' '.join(tmp[1:]))
            return line
        except:
            return line
    
    def run(self):
        self.process(self.processPOI)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--arpa', required=True, help='')
    parser.add_argument('--output', required=True, help='')
    parser.add_argument('--delta', required=True, help='')
    args = parser.parse_args()

    poiModel = BaseModelProcessor(args.arpa, args.output, args.delta)
    poiModel.run()