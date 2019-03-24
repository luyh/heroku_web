from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import  re
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
import requests


def wechat_sent(title,text):
    try:
        requests.post( 'https://sc.ftqq.com/SCU23707T1a6b7b5527ba64588859a61ecfca18775ab65ce918f4f.send', \
                       data={'text': title, 'desp': text} )
        print(title,text)
    except:
        print('发送微信报错')

class hpg():
    def __init__(self):
        self.driver = None
    def start(self):
        print(u'正在连接chrome浏览器...')
        driver = webdriver.Chrome('/Users/Hebbelu/Downloads/chromedriver')
        self.driver = driver
        print(u'已打开chrome浏览器，并成功连接')


        print('打开红1网页...')
        driver.get("http://hpg.sqk2.cn/public/apprentice.php/passport/login.html")
        print(driver.title)

        print('输入用户名及密码...')
        input_user = driver.find_element_by_id('username')
        input_user.clear()
        input_user.send_keys("luyhaa")

        password = driver.find_element_by_id('password')
        password.clear()
        password.send_keys("aa123456")

        print('点击登陆...')
        sighinButton = driver.find_element_by_id('login-btn')
        sighinButton.click()
        time.sleep(1)

        print('切换我要买页面...')
        toBuy = driver.find_element_by_link_text('我要买')
        toBuy.click()
        time.sleep(1)


    def subscrib_task(self):
        driver = self.driver

        try:
            normal_task = driver.find_element_by_id( 'normal-task' )
            activity_task = driver.find_element_by_id( 'activity-task' )

            normal_task.click()
            time.sleep( 1 )
            activity_task.click()
            time.sleep( 1 )
        except:
            print('没找到领任务按钮')

    def receive_button(self):
        try:
            receive_button = self.driver.find_element_by_link_text( '领取' )
            print( receive_button, receive_button.text )
            receive_button.click()
            time.sleep( 5 )
            return True
        except:
            print( datetime.now(), '没找到领取按钮' )

    def keywords(self):
        try:
            print( '找关键词' )
            data_text = self.driver.find_element_by_class_name( 'copy-lookup-data-text' )
            text = data_text.get_attribute( 'value' )
            print( '关键词', text )
            wechat_sent( '领取任务', text )
        except:
            print( 4, '没找到关键词' )

    def receive(self):
        driver = self.driver
        while (1):
            now = datetime.now()
            if (now.second == 15):
                print( now, '每分钟的第15s刷新页面' )
                driver.refresh()

            if self.receive_button():
                self.keywords()
            time.sleep( 10 )



def main():
    demo = hpg()
    demo.start()
    demo.subscrib_task()
    demo.receive()

if __name__ == '__main__':
    main()
