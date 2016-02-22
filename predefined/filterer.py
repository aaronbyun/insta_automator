#-*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('./..')
sys.path.append('../..')

import codecs

class Filterer:
    def __init__(self):
        self.ban_word_dict   = {}

        with codecs.open('../txt/ban.txt', 'r', 'utf8') as f:
            for line in f:
                line = line.replace('\r\n', '')
                self.ban_word_dict[line] = 1
                self.ban_word_dict['#'+line] = 1

    def have_ban_words(self, content):
        for ban_word in self.ban_word_dict.keys():
            if ban_word in content:
                print '-' * 100
                print 'ban word : ', ban_word
                print '-' * 100
                return True

        for word in content.split(' '):
            if word in self.ban_word_dict:
                print '-' * 100
                print 'ban word : ', word
                print '-' * 100
                return True
        return False