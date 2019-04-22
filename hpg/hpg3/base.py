from selenium import webdriver
import time

class BASE(object):
    def __init__(self):
        self.login_url = None
        self.toBuy_url = None
        self.status = None
        self.receive_btn_xpath = None
        self.driver = None

    def login(self):
        pass

    def _get(self,url,num = 5):
        i = 0
        if i <num:
            self.driver.get(url)
            if self.driver.title == "hpg.sqk2.cn":
                print('第{}次尝试打开网页:{}没打开'.format(i,url))
                self.driver.refresh()
                time.sleep(3)
                self._get(url,i+1)
            else:
                print('已打开网页：{}，标题：{}'.format(url,self.driver.title))
                return True
        else:
            print('尝试{}次没打开网页：{}'.format(num,url))
            return False

    def toBuy(self):
        print( '切换到我要买页面' )
        self._get( self.task_url )
        time.sleep(3)

    def queue_task(self):
        pass

    def wait_task(self):
        pass

    def check_status(self):
        pass

    def status(self):
        pass
