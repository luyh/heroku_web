#TODO: TAOBAO
from hpg.hpg3.chrome.connect_chrome import Chrome
from hpg.hpg3.ulity import send_email
from hpg.hpg3.ulity.china_time import chinatime
import os,time
from selenium.webdriver.common.keys import Keys
import random
import re
from urllib.parse import urlencode
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
from selenium.common.exceptions import NoSuchElementException

class Taobao(Chrome):
    def __init__(self,name='taobao'):
        self.driver = None
        self.name = name
        self.threadLock = threading.Lock()

        self.taskInfo = None


    def get_goods(self):
        hrefs = self.driver.find_elements_by_xpath( "//*[@id='mainsrp-itemlist']//div[@class='pic']/a" )
        pic_urls = self.driver.find_elements_by_xpath( "//*[@id='mainsrp-itemlist']//div[@class='pic']/a/img" )
        goods = []
        #print( len( hrefs ), len( pic_urls ) )
        for i in range( len( hrefs ) ):
            info = {    'id':i,
                        'name':pic_urls[i].get_attribute( 'alt' ),
                         'pic_url':'http://' + pic_urls[i].get_attribute( 'data-src' )[2:] ,
                          'good_url':hrefs[i].get_attribute( 'href' )
                         }
            goods.append(info)

            # print( i, pic_urls[i].get_attribute( 'alt' ) + '\n',
            #        'http://' + pic_urls[i].get_attribute( 'data-src' )[2:] + '\n',
            #        hrefs[i].get_attribute( 'href' ) )

        return goods


    def get_url(self,key_word, number_two):
        '''
            获取关键字的链接
            :param keyword:    关键字
            :param number_two:    不同的数值对应不同的页码，淘宝上第一页为0 ，第二页为44
                                   第三页为88.。。。
            :return:   不同页码的链接
        '''
        data = {
            'ie': 'utf8',
            'initiative_id': 'staobaoz_20180830',
            'stats_click': 'search_radio_all:1',
            'js': '1',
            'imgfile': ' ',
            'q': key_word,
            'suggest': 'history_3',
            '_input_charset': 'utf - 8',
            'wq': ' ',
            'suggest_query': ' ',
            'source': 'suggest',
            'bcoffset': '6',
            'ntoffset': '6',
            'p4ppushleft': '1, 48',
            's': number_two*44
        }
        url = r'https://s.taobao.com/search?' + urlencode(data)
        return url

from hpg.hpg3.taobao import image
from hpg.hpg3.taobao.taobao_cookie import cookies

if __name__ == '__main__':

    goods_key = '工装裤男'
    target_url = 'http://hpg.968012.com/public/static/task/images/20191116/317e4f29aa86e08f80a33864a352b897u50sw6cen8sitm0avo7lc9skcth1ap1z.jpeg'
    target_pic = image.url_to_image( target_url)

    test = Taobao()

    test.connectChrome()

    test.driver.get('https://www.taobao.com')
    for item in cookies:
        test.driver.add_cookie( item )

    test.driver.get( 'https://www.taobao.com' )
    time.sleep(2)

    for page in range(50):

        url = test.get_url( goods_key, page )
        print( page ,url)
        test.driver.get( url )
        goods = test.get_goods()
        hists = image.classify_hist_with_split( target_pic, goods )
        print(hists)

        for good in goods:
            if good['hist'] > 0.95:
                find_url = good['good_url']
                print( chinatime.getChinaTime(), '找到类似图片', good['hist'], find_url )

                print('pause')

        time.sleep(random.randrange(5,20)+random.random())

    time.sleep(10)



