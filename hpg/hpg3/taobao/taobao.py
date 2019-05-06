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

    # 登录淘宝
    def login(self,weibo_username,weibo_password):
        # 打开网页
        url = 'https://login.taobao.com/member/login.jhtml'
        self.driver.get( url )

        # 等待 密码登录选项 出现
        password_login = self.wait.until(
            EC.presence_of_element_located( (By.CSS_SELECTOR, '.qrcode-login > .login-links > .forget-pwd') ) )
        password_login.click()

        # 等待 微博登录选项 出现
        weibo_login = self.wait.until( EC.presence_of_element_located( (By.CSS_SELECTOR, '.weibo-login') ) )
        weibo_login.click()

        # 等待 微博账号 出现
        weibo_user = self.wait.until( EC.presence_of_element_located( (By.CSS_SELECTOR, '.username > .W_input') ) )
        weibo_user.send_keys( weibo_username )

        # 等待 微博密码 出现
        weibo_pwd = self.wait.until( EC.presence_of_element_located( (By.CSS_SELECTOR, '.password > .W_input') ) )
        weibo_pwd.send_keys( weibo_password )

        # 等待 登录按钮 出现
        submit = self.wait.until( EC.presence_of_element_located( (By.CSS_SELECTOR, '.btn_tip > a > span') ) )
        submit.click()

        # 直到获取到淘宝会员昵称才能确定是登录成功
        taobao_name = self.wait.until( EC.presence_of_element_located( (By.CSS_SELECTOR,
                                                                        '.site-nav-bd > ul.site-nav-bd-l > li#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-user > a.site-nav-login-info-nick ') ) )
        # 输出淘宝昵称
        print( taobao_name.text )


    def chek_login(self):

        self.driver.get( 'https://login.taobao.com/member/login.jhtml' )

        for item in cookies:
            self.driver.add_cookie( item )
        time.sleep(1)

        self.get_qrcode_img_link_address()

        # while True:
        #     try:
        #         if self.driver.find_element_by_link_text( "密码登录" ):
        #             print("请扫码登录...")
        #             time.sleep( 1 )
        #             try:
        #                 if self.driver.find_element_by_link_text( "请点击刷新" ):
        #                     self.driver.find_element_by_link_text( "请点击刷新" ).click()
        #                     time.sleep( 1 )
        #                     self.get_qrcode_img_link_address()
        #             except NoSuchElementException:
        #                 time.sleep( 1 )
        #                 continue
        #     except NoSuchElementException:
        #         print("成功登录...")
        #         print(self.driver.current_url)
        #         break

        return True

    def get_qrcode_img_link_address(self):
        try:
            if self.driver.find_element_by_id( "J_QRCodeImg" ):
                print('get the QRCodeImgUrl.....')
                print(self.driver.find_element_by_id( "J_QRCodeImg" ).find_element_by_tag_name( "img" ).get_attribute( "src" ))
                return True
        except NoSuchElementException:

            return False

    def search(self,key = 'python'):
        self.chek_login()
        taobao_search = self.driver.find_element_by_id( 'q' )
        taobao_search.clear()
        taobao_search.send_keys( key )
        taobao_search.send_keys( Keys.ENTER )
        time.sleep(3)

        next_page_xpath = '//*[@id="mainsrp-pager"]/div/div/div/ul/li[8]/a'
        next_page = self.driver.find_element_by_xpath(next_page_xpath)
        self.next_page_url = next_page.get_attribute('href')
        self.offset = "& bcoffset = 3 & ntoffset = 3 & p4ppushleft = 1 % 2C48 & s = "


    def mtaobao(self):
        js="window.open('http://m.taobao.com');"
        self.driver.execute_script(js)


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

    def get_next_page(self,i):
        data_value = (i+1) + 44
        url = (self.next_page_url + self.offset + str(data_value)).replace(' ', '').replace('#', '')
        print('第{}页'.format(i+2), data_value, url)
        self.driver.get(url)
        time.sleep(3)

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
            's': number_two
        }
        url = r'https://s.taobao.com/search?' + urlencode(data)
        return url
from hpg.hpg3.taobao.taobao_cookie import cookies

if __name__ == '__main__':
    test = Taobao()

    test.connectChrome()
    # weibo_username=os.environ.get( 'weibo_username' )
    # weibo_password=os.environ.get( 'weibo_password' )
    # test.login(weibo_username,weibo_password)

    test.driver.get('https://www.taobao.com')
    for item in cookies:
        test.driver.add_cookie( item )

    test.driver.get( 'https://www.taobao.com' )
    time.sleep(2)

    url = test.get_url( '裤子', 0 )
    test.driver.get(url)
    time.sleep(10)



