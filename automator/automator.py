#-*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('./..')
sys.path.append('../..')

import codecs
import time
import unittest
import os
import random
import argparse
from random import shuffle
from selenium import webdriver
from selenium.webdriver.support import ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from predefined.filterer import Filterer
from predefined.comment import Comment
from predefined.keyword import Keyword

class Automator:
    def __init__(self):
        pass

    def init(self, commenter, filterer):
        chromedriver = '/Users/aaronbyun/development/Libs/chromedriver'
        os.environ['webdriver.chrome.driver'] = chromedriver
        self.driver = webdriver.Chrome(chromedriver)

        self.commenter = commenter
        self.filterer = filterer

    def login(self, id, pwd):
        self.driver.get('https://www.instagram.com')

        try:
            btn_login = self.driver.find_element_by_css_selector('button[class="_rz1lq _k2yal _84y62 _7xso1 _nv5lf"]')
        except NoSuchElementException, e:
            print e

            link_login = self.driver.find_element_by_css_selector('a[class="_k6cv7"]')
            link_login.click()

            btn_login = self.driver.find_element_by_css_selector('button[class="_rz1lq _k2yal _84y62 _7xso1 _nv5lf"]')

        username = self.driver.find_element_by_name('username')
        password = self.driver.find_element_by_name('password')

        username.send_keys(id)
        password.send_keys(pwd)
        
        btn_login.click()

    def like_feed(self, probability):
        try:
            self.driver.get('https://www.instagram.com')
            wait = ui.WebDriverWait(self.driver, 120)
            wait.until(lambda driver: driver.find_elements_by_css_selector('article[class="_8ab8k _j5hrx _pieko"]'))
            likes = self.driver.find_elements_by_css_selector('a[class="_ebwb5 _1tv0k _345gm coreSpriteHeartOpen"]')
            contents = self.driver.find_elements_by_css_selector('div[class="_es1du _rgrbt"]')

            article_num = len(likes)
            rand_indice = range(article_num)
            shuffle(rand_indice)

            target_num = int(article_num * probability)
            rand_indice = rand_indice[:target_num]

            print target_num, 'is about to be liked out of', article_num, 'new feeds.'
            for index in rand_indice:
                content = contents[index]
                if not self.filterer.have_ban_words(content.text):
                    like = likes[index]
                    #like.send_keys(Keys.NULL)
                    like.click()

                    # delay
                    time.sleep(2)

        except Exception, e:
            print e

    def search_tag(self, probability, term):
        tag_url = 'https://www.instagram.com/explore/tags/%s/' % term
        self.driver.get(tag_url)

        wait = ui.WebDriverWait(self.driver, 120)
        wait.until(lambda driver: driver.find_element_by_css_selector('a[class="_8mlbc _t5r8b"]'))

        feeds = self.driver.find_elements_by_css_selector('a[class="_8mlbc _t5r8b"]') 

        feed_num = len(feeds)
        rand_indice = range(feed_num)
        shuffle(rand_indice)

        target_num = int(feed_num * probability)
        rand_indice = rand_indice[:target_num]

        for index in rand_indice:
            feeds[index].click()
            
            op_code = random.randint(4, 7)
            op_bits = "{0:03b}".format(op_code)

            wait.until(lambda driver: driver.find_element_by_css_selector('a[class="_4zhc5 _ook48"]'))
            insta_id = self.driver.find_element_by_css_selector('a[class="_4zhc5 _ook48"]').text 

            print insta_id

            content = self.driver.find_element_by_css_selector('ul[class="_mo9iw _123ym"]').text
            if not self.filterer.have_ban_words(content):
                if op_bits[0] == '1':
                    if self.like():
                        print 'likes', insta_id
                        time.sleep(3)

                if op_bits[1] == '1':
                    if self.follow():
                        print 'follows', insta_id
                        time.sleep(3)

                if op_bits[2] == '1':
                    message = self.comment.get_random_comment()
                    '''if self.leave_comment(message):
                        print 'leaves a comment', message, 'to', insta_id 
                        time.sleep(3)'''
            else:
                print 'Suspicious spammer was detected!!!'

            btn_close = self.driver.find_element_by_css_selector('button[class="_3eajp"]')
            btn_close.click()

            time.sleep(5)

    def like(self):
        try:
            wait = ui.WebDriverWait(self.driver, 120)
            wait.until(lambda driver: driver.find_element_by_css_selector('a[class="_ebwb5 _1tv0k _345gm coreSpriteHeartOpen"]'))

            btn_like = self.driver.find_element_by_css_selector('a[class="_ebwb5 _1tv0k _345gm coreSpriteHeartOpen"]')
            if btn_like != None:
                btn_like.click()
                return True
            return False
        except Exception, e:
            print e
            return False

    def follow(self):
        try:
            wait = ui.WebDriverWait(self.driver, 120)
            wait.until(lambda driver: driver.find_element_by_css_selector('button[class="_jvpff _k2yal _csba8 _i46jh _nv5lf"]'))

            btn_follow = self.driver.find_element_by_css_selector('button[class="_jvpff _k2yal _csba8 _i46jh _nv5lf"]')
            if btn_follow != None and btn_follow.text == 'FOLLOW':
                btn_follow.click()
                return True
            return False
        except Exception, e:
            print e
            return False
        

    def leave_comment(self, cmt):
        try:
            wait = ui.WebDriverWait(self.driver, 120)
            wait.until(lambda driver: driver.find_element_by_css_selector('input[class="_7uiwk"]'))

            comment = self.driver.find_element_by_css_selector('input[class="_7uiwk"]')
            comment.send_keys(cmt)
            comment.send_keys(Keys.RETURN)
            return True
        except Exception, e:
            print e
            return False


    def close(self):
        self.driver.close()
        

    def quit(self):
        self.driver.quit()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', help='instagram user id', required = True)
    parser.add_argument('-p', '--pwd', help='instagram user password', required = True)
    parser.add_argument('-f', '--feed', help='feed like probability', type = float, default = 0.2)
    parser.add_argument('-t', '--tag', help='tag selection probability', type = float, default = 0.4)
    parser.add_argument('-d', '--delay', help='tag selection probability', type = int, default = 10)

    args = vars(parser.parse_args())
    user        = args['user']
    password    = args['pwd']
    feed_prob   = args['feed']
    tag_prob    = args['tag']
    delay       = args['delay']

    keyword = Keyword()

    filterer = Filterer()
    commenter = Comment()

    automator = Automator()
    automator.init(commenter, filterer)
    automator.login(user, password)

    while True:
        automator.like_feed(feed_prob)
        tag = keyword.get_random_keyword()
        print 'searching tag :', tag, '....'
        time.sleep(2)
        automator.search_tag(tag_prob, tag)

        time.sleep(delay)




