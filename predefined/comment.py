#-*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('./..')
sys.path.append('../..')

import codecs
import random

class Comment:
    def __init__(self):
        self.load()

    def load(self):
        self.comments = []
        with codecs.open('../txt/comment.txt', 'r', 'utf8') as f:
            for line in f:
                line = line.replace('\r\n', '')
                self.comments.append(line)

    def get_random_comment(self):
        idx = random.randint(0, len(self.comments) - 1)
        return self.comments[idx]