import string
import random,os
import hashlib
import requests
import time
from hpg.hpg3.ulity.china_time import chinatime
from requests_html import HTMLSession
from hpg.hpg3.taobao.image import url_to_image
import cv2
from hpg.hpg3.vertify_code_recognize.vertify_code_recognize import count as count_img
import numpy as np

session = HTMLSession()

class ZKB():
    def __init__(self,username=None,password=None,debug = False):
        self.username = username
        self.password = password

        self.headers = {
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': "zhuankeban.com",
            'Proxy-Connection': "keep-alive",
            'Cache-Control': "max-age=0",
            'Upgrade-Insecure-Requests': "1",
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Referer': "http://zhuankeban.com//jsp/Mobile/apprentice/ApprenticeLogin.jsp",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
            'Content-Type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache",
        }

        self.proxies = None

        self.normal = 0
        self.activity = 0
        self.traffic = 0

        self.debug = debug


    def debug(fn):
        def log(self):
            if self.debug:
                print( chinatime.getChinaTime(),fn.__name__,fn(self))
        return log

    @debug
    def request_continue(self,normal=1,activity=1,traffic=0,wait_time=60):
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
        url = 'http://zhuankeban.com/jsp/Mobile/apprentice/ApprenticeLogin.jsp'
        response = session.get(url,headers = self.headers)

        verification_code = self.count_vertify_code()

        url = "http://zhuankeban.com:80/user/login.do"

        data = {'user_account': self.username,
                'user_password': self._md5(self.password),
                'user_type': '0',
                'verification_code':verification_code,
                }
        response = session.get(url,params= data,headers = self.headers)
        return response.json()

    def set_proxies(self):
        #todo:设置proxies
        pass

    def count_vertify_code(self):
        image = self._get_verification_code_jpg()

        verification_code = count_img( image, self.debug )

        if 0:
            print( verification_code )
            cv2.imshow( 'vertify_code.jpg', image )
            cv2.waitKey(0)

        return verification_code

    def _get_verification_code_jpg(self,debug=False):
        url = 'http://zhuankeban.com/verificationCode.jpg'
        resp = session.get( url )
        image = cv2.imdecode( np.fromstring( resp.content, np.uint8 ), 1 )
        #image = url_to_image(url,cookies=self.cookies)

        return image

    def _md5(self,password):
        hash = hashlib.md5()
        hash.update( bytes( password, encoding='utf-8' ) )
        if self.debug:
            print(hash.hexdigest())
        return hash.hexdigest()


if __name__ == '__main__':
    username = os.environ.get( 'HPG_USER' )  # 用户名
    password = os.environ.get( 'HPG_PASS' )  #

    zkb = ZKB(username,password,debug=True)
    zkb.login()
    # time.sleep(2)

    # hpg.set_running_status(1,1,0)
    #
    # hpg.request_continue()
