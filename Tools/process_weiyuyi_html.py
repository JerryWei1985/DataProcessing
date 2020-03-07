#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os
import argparse
import urllib.request
from bs4 import BeautifulSoup


def parseWeiyuyiHTML(html) -> list:
    sourceList = []
    soup = BeautifulSoup(html, 'html.parser')
    tableSoup = soup.find('table')
    trSoup = tableSoup.find_all('tr')
    for trItem in trSoup:
        if not trItem.has_attr('id'):
            continue
        tdSoup = trItem.find_all('td')
        contentSoup = tdSoup[0].find('span')
        wavSoup = tdSoup[1].find('source')
        content = contentSoup.text
        wavUrl = wavSoup['src']
        wavId = os.path.splitext(os.path.basename(wavUrl))[0]
        sourceList.append((wavId, content, wavUrl))
    return sourceList

def outputTestSet(sourceList, outputFolder):
    textPath = os.path.join(outputFolder, 'text')
    wavScpPath = os.path.join(outputFolder, 'wav.scp')
    wavFolderPath = os.path.join(outputFolder, 'wav')
    if not os.path.exists(wavFolderPath):
        os.makedirs(wavFolderPath)
    with open(textPath, 'a') as tf:
        with open(wavScpPath, 'a') as wf:
            for item in sourceList:
                wavPath = os.path.join(wavFolderPath, item[0] + '.wav')
                urllib.request.urlretrieve(item[2], wavPath)
                tf.write('{} {}\n'.format(item[0], item[1]))
                wf.write('{} {}\n'.format(item[0], wavPath))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--html', nargs='+')
    parser.add_argument('--output-folder')
    args = parser.parse_args()
    html = ''
    for item in args.html:
        with open(item) as inf:
            html = inf.read()
        sourceList = parseWeiyuyiHTML(html)
        outputTestSet(sourceList, args.output_folder)
