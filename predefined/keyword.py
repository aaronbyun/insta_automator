#-*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('./..')
sys.path.append('../..')

import codecs
import random

class Keyword:
    def __init__(self):
        self.load()

    def load(self):
        self.keywords = []
        with codecs.open('../txt/search.txt', 'r', 'utf8') as f:
            for line in f:
                line = line.replace('\r\n', '')
                self.keywords.append(line)

    def get_random_keyword(self):
        idx = random.randint(0, len(self.keywords) - 1)
        return self.keywords[idx]