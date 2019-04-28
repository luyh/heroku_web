from selenium import webdriver
from . import mywebdriver
import pickle
import time,sys
import threading
from hpg.hpg3.ulity import china_time

# 打印系统系统
systerm = sys.platform
print( '系统类型:', systerm )



class Refresh(threading.Thread):
    def __init__(self,driver,delay = 30):
        threading.Thread.__init__(self)
        self.threadID = 'refreshChrome_thread'
        self.delay = delay
        self.driver = driver

    def run(self):
        now = china_time.ChinaTime()
        while(1):
            threadLock.acquire()
            print(now.getChinaTime(),'刷新chrome')
            self.driver.refresh()
            time.sleep(3)
            threadLock.release()

            time.sleep(self.delay)


class Chrome():
    mobileEmulation = None
    def __init__(self,name = 'chrome',mobileEmulation = None):
        self.name = name
        self.driver = None
        self.mobileEmulation = mobileEmulation

    def connectChrome(self):
        print( '正在读取{}.data 尝试连接chrome:{}'.format( self.name,self.name ) )
        try:
            f = open( "{}.data".format(self.name), 'rb' )
            # 从文件中载入对象
            params = pickle.load( f )
            # print( params )
            browser = mywebdriver.myWebDriver( service_url=params["server_url"],
                                               session_id=params["session_id"] )
            try:
                browser.title
                print( '已连上chrome参数为:{}'.format( params ) )
                self.driver = browser
                return True
            except :
                print( 'chrome not reachable，连接chrome失败' )
                self.newChrome()

                return True

        except FileNotFoundError:
            print('没找到：{}.data文件'.format(self.name))
            self.newChrome()
            return True

    def newChrome(self):
        options = webdriver.ChromeOptions()
        if self.mobileEmulation != None:
            options.add_experimental_option( 'mobileEmulation', self.mobileEmulation )
        #options.add_argument('detach = True')
        # 连接Chrome
        print(u'正在新建chrome浏览器...')
        if systerm.startswith('darwin'):

            #options.add_argument( "user-data-dir='~/Library/Application''Support/Google/Chrome/Default'" )

            #options.add_argument( '–disk-cache-dir=./cache' )
            driver = webdriver.Chrome('/Users/Hebbelu/Downloads/chromedriver', 0,\
                                      chrome_options=options)
        elif systerm.startswith('linux'):
            driver = webdriver.Chrome(chrome_options=options)


        elif systerm.startswith('win32'):
            driver = webdriver.Chrome(executable_path='E:\luyh\heroku\calm-scrubland-72089\hpg\hpg3\chrome\chromedriver.exe', chrome_options=options)
        time.sleep(3)

        #print(u'已新建chrome浏览器，并成功连接')
        self.driver = driver

        params = {}
        params["session_id"] = driver.session_id
        params["server_url"] = driver.command_executor._url

        #print('正在保存chrome参数至{}.data' .format(self.name))
        f = open( "{}.data".format(self.name), 'wb' )
        # 转储对象至文件
        pickle.dump( params, f )
        f.close()
        #print('已保存chrome参数至{}.data' .format(self.name))

    def start_refresh_thread(self,delay = 30):
        thread = Refresh(self.driver,delay)
        print('Starting Refresh Chrome Thread')
        thread.start()



