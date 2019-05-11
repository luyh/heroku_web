import random
import hashlib
import time,os,pickle,threading
from hpg.hpg3.ulity.china_time import chinatime
from hpg.hpg3.ulity.sms_twilio import msm

from requests_html import HTMLSession
session = HTMLSession()

class HPG():
    def __init__(self,username,password,debug = False):
        self.username = username
        self.password = password

        self.url = 'http://hpg.sqk2.cn'

        self.headers = {
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': self.url,
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
        try:
            with open('hpg.cookies','rb') as f:
                self.cookies = pickle.load(f)
            print(self.cookies)
            print('load cookies success')
        except:
            print('load cookies error')
            self.cookies = None

        self.normal = 0
        self.activity = 0
        self.traffic = 0

        self.received = False
        self.Login = False
        self.Keep_alive = True

        self.threadLock = threading.Lock

        self.debug = debug

    def cancle(self):
        self.set_running_status(0,0,0)

    def receive_task(self):
        url = 'http://hpg.sqk2.cn/public/apprentice.php/task/index.html'
        response = session.get(url)
        print(response.html.html)
        operation_form = response.html.find('#operation-form')
        print(operation_form.html)
        print( operation_form.attrs['action'] )


    def debug(fn):
        def log(self):
            if self.debug:
                print( chinatime.getChinaTime(),fn.__name__,fn(self))
        return log

    @debug
    def request_continue(self,wait_time=60):
        while self.is_running():
            self.ajax_queue_up()
            if self.received:
                self.receive_task()
                break
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
        response = session.post( url, data=data,headers=self.headers ).json()

        if response['normal_stop']:self.normal=0
        if response['activity_stop']:self.activity=0
        if response['traffic_stop']:self.traffic=0

        if response['task']:
            self.received=1
            msm('接到红苹果任务')


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
        if self.checklogin():
            if not self.Login:
                session.cookies = self.cookies
                self.Login = True
                self.checklogin()
        else:
            self.ajax_login()

        if self.Login:
            print('刷新保持登陆')
            t = threading.Thread( target=self.checklogin, name='Checklgin_Thread' )
            t.start()
            return True
    @debug
    def ajax_login(self):
        url = "http://hpg.sqk2.cn/public/apprentice.php/passport/ajax_login.html"

        data = {'username': self.username,
                'password': self._md5( self.password ),
                'remember': 0,
                'callback': '',
                't': random.random()}

        response = session.post( url, data, headers=self.headers )
        if response.status_code == 200:
            if response.json()['success'] == 1:
                self.cookies = session.cookies
                print( self.cookies )
                with open( 'hpg.cookies', 'wb' ) as f:
                    pickle.dump( self.cookies, f )
                print( 'save cookies done' )
                self.Login = True
        else:
            self.Login = False
            print( 'hpg not login' )

        return response.json()

    def _md5(self,password):
        hash = hashlib.md5()
        hash.update( bytes( password, encoding='utf-8' ) )
        return hash.hexdigest()

    def checklogin(self):
        url = 'http://hpg.sqk2.cn/public/apprentice.php/task/index.html'
        response = session.get( url, cookies=self.cookies, headers=self.headers )
        #print(response.html.html)
        wait = response.html.find( 'b#wait', first=True )
        if wait:
            return False
        else:
            return True

    def keep_alive(self):
        while(self.Keep_alive):
            self.checklogin()
            time.sleep(60)

if __name__ == '__main__':
    username = os.environ.get( 'HPG_USER' )  # 用户名
    password = os.environ.get( 'HPG_PASS' )  #

    print(username,password)

    hpg = HPG(username,password,debug=True)

    hpg.login()
    time.sleep(2)

    if hpg.received == False:
        hpg.set_running_status(0,0,1)

        hpg.request_continue()

        hpg.receive_task()


