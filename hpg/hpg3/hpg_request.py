import string
import random
import hashlib
import requests
import time,os
from hpg.hpg3.ulity.china_time import chinatime
from requests_html import HTMLSession

session = HTMLSession()

class HPG():
    def __init__(self,username,password,debug = False):
        self.username = username
        self.password = password

        self.headers = {
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': "hpg.sqk2.cn",
            'Proxy-Connection': "keep-alive",
            'Cache-Control': "max-age=0",
            'Upgrade-Insecure-Requests': "1",
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Referer': "http://hpg.sqk2.cn/public/apprentice.php/task/index.html",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
            'Content-Type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache",
        }

        self.cookies = self._generate_cookies()

        self.normal = 0
        self.activity = 0
        self.traffic = 0

        self.received = 0

        self.debug = debug

    def task(self):
        url = 'http://hpg.sqk2.cn/public/apprentice.php/task/index.html'


    def debug(fn):
        def log(self):
            if self.debug:
                print( chinatime.getChinaTime(),fn.__name__,fn(self))
        return log

    @debug
    def request_continue(self,wait_time=60):
        while self.is_running():
            self.ajax_queue_up()
            time.sleep(wait_time)

    @debug
    def ajax_queue_up(self):
        url = 'http://hpg.sqk2.cn/public/apprentice.php/task/ajax_queue_up'
        # 构造form表单
        data = {
            'normal': self.normal,
            'activity': self.activity,
            'traffic': self.traffic,
            't': random.random()
        }
        response = requests.post( url, data=data,cookies = self.cookies,headers=self.headers ).json()

        if response['normal_stop']:self.normal=0
        if response['activity_stop']:self.activity=0
        if response['traffic_stop']:self.traffic=0

        if response['task']:
            self.received=1

        return response



    def is_running(self):
        return self.normal or self.activity or self.traffic
    def set_running_status(self,normal,activity,traffic):
        sale = normal or activity
        if traffic and sale:
            print('销量与流量任务不能同时排队')
            return False

        self.normal = normal
        self.activity = activity
        self.traffic = traffic

    @debug
    def login(self):
        url = "http://hpg.sqk2.cn/public/apprentice.php/passport/ajax_login.html"

        data = {'username': self.username,
                'password': self._md5(self.password),
                'remember': 0,
                'callback': '',
                't': random.random()}

        response = requests.post(url, data=data, cookies=self.cookies, headers=self.headers ).json()

        return response

    @debug
    def _generate_cookies(self):
        cookie_value = ''.join( random.sample( string.ascii_letters + string.digits, 26 ) )
        # cookies = {'apprentice':'m4jri5j1n1ase9p0j3fsng3kf1'}
        cookies = {'apprentice': cookie_value}
        return cookies

    def _md5(self,password):
        hash = hashlib.md5()
        hash.update( bytes( password, encoding='utf-8' ) )
        return hash.hexdigest()

if __name__ == '__main__':
    username = os.environ.get( 'HPG_USER' )  # 用户名
    password = os.environ.get( 'HPG_PASS' )  #

    hpg = HPG(username,password,debug=True)

    response = hpg.login()
    time.sleep(2)

    hpg.set_running_status(1,1,0)

    hpg.request_continue()
