#TODO: TAOBAO
from hpg.hpg3.chrome.connect_chrome import Chrome
from hpg.hpg3.ulity import send_email
from hpg.hpg3.ulity.china_time import chinatime
import os,time
from selenium.webdriver.common.keys import Keys
import random

class Taobao(Chrome):
    def __init__(self,name='taobao'):
        self.driver = None
        self.name = name

        self.taskInfo = None

    def login(self):
        print( '打开taobao' )
        self.driver.get( "https://login.taobao.com" )
        print( self.driver.title )
        print( '请自行完成登陆操作' )
        # TODO:发送淘宝二维码给手机淘宝扫码登陆

    def chek_login(self):
        print('请检查登陆taobao')
        self.driver.get("https://www.taobao.com")
        time.sleep(5)
        return True

    def search(self,key = 'python'):
        self.chek_login()
        taobao_search = self.driver.find_element_by_id( 'q' )
        taobao_search.clear()
        taobao_search.send_keys( key )
        taobao_search.send_keys( Keys.ENTER )

    def mtaobao(self):
        js="window.open('http://m.taobao.com');"
        self.driver.execute_script(js)


    def get_goods(self):
        hrefs = self.driver.find_elements_by_xpath( "//*[@id='mainsrp-itemlist']//div[@class='pic']/a" )
        pic_urls = self.driver.find_elements_by_xpath( "//*[@id='mainsrp-itemlist']//div[@class='pic']/a/img" )
        goods = []
        print( len( hrefs ), len( pic_urls ) )
        for i in range( len( hrefs ) ):
            info = {'name':pic_urls[i].get_attribute( 'alt' ),
                         'pic_url':'http://' + pic_urls[i].get_attribute( 'data-src' )[2:] ,
                          'good_url':hrefs[i].get_attribute( 'href' )
                         }
            goods.append(info)

            # print( i, pic_urls[i].get_attribute( 'alt' ) + '\n',
            #        'http://' + pic_urls[i].get_attribute( 'data-src' )[2:] + '\n',
            #        hrefs[i].get_attribute( 'href' ) )

        return goods

    def get_next_page(self):
        next_page_xpath = '//*[@id="mainsrp-pager"]/div/div/div/ul/li[8]/a'

        next_page = self.driver.find_element_by_xpath( next_page_xpath )
        #next_page_js = 'document.getElementByXpath(“{}”).scrollIntoViewIfNeeded();'.format( next_page_xpath )

        # scroll = round( random.uniform( 3, 8 ), 2 ) * 100
        # for t in range(int(random.uniform( 3, 5 ))):
        #     time.sleep( round( random.uniform( 1, 5 ), 2 ) )
        #     js = "window.scrollTo(0,{});".format(scroll)
        #     print(js)
        #     self.driver.execute_script( js)
        #     scroll = scroll +round( random.uniform( 3, 8 ), 2 ) * 100

        # try:
        #     self.driver.execute_script(next_page_js)
        # except:
        #     print('滑动到下一页出错')

        # try:
        #     next_page.click()
        #     print('点击下一页成功')
        # except:
        #     print('点击下一页出错，直接跳转')
        next_page_url = next_page.get_attribute( 'href' )
        print(next_page.text,next_page_url)
        self.driver.get(next_page_url)

if __name__ == '__main__':
    test = Taobao()

    test.connectChrome()

    next_page_xpath = '//*[@id="mainsrp-pager"]/div/div/div/ul/li[8]/a'
    next_page = test.driver.find_element_by_xpath( next_page_xpath )
    next_page_url = next_page.get_attribute( 'href' )
    for i in range(5):
    #     test.driver.execute_script( "window.scrollTo(0,document.body.scrollHeight)" )
    #     try:
    #         next_page.click()
    #     except:
    #         print('click error')
        data_value = next_page.get_attribute( 'data-value' )
        next_page_url = next_page_url.replace('')
        print( next_page.text, data_value, next_page_url.)

        test.driver.get(next_page_url)
        time.sleep(3)
        # test.driver.refresh()


