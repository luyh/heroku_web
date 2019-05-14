from hpg.hpg3.chrome.connect_chrome import Chrome
from hpg.hpg3.ulity import china_time,send_email
import os,time
import threading




class HPG(Chrome):
    def __init__(self,name = 'hpg',debug = False,mobileEmulation = None):
        self.name = name
        self.driver = None
        self.threadLock = threading.Lock()

        self.username = os.environ.get( 'HPG_USER' )  # 用户名
        self.password = os.environ.get( 'HPG_PASS' )  #

        if self.username==None:
            print('hpg用户名为空')

        self.login_url = 'http://hpg.sqk2.cn/public/apprentice.php/passport/login.html'
        self.task_url= 'http://hpg.sqk2.cn/public/apprentice.php/task/index.html'
        self.submitted_url = 'http://hpg.sqk2.cn/public/apprentice.php/task/submitted.html'
        self.user_url = 'http://hpg.sqk2.cn/public/apprentice.php/user/index.html'


        self.username_id = 'username'
        self.password_id = 'password'
        self.login_button_id = 'login-btn'
        self.normal_task_button_xpath = '//*[@id="normal-task"]'
        self.activity_task_button_xpath = '//*[@id="activity-task"]'
        self.receive_btn_xpath = '//*[@id="operation"]/a[2]'
        self.traffic_task_xpath = '//*[@id="traffic-task"]'

        self.taskInfo = None
        self.taskInfoFlag = False
        self.today = 0

        self.now = china_time.ChinaTime()

    def login(self):
        if self.driver.current_url in self.login_url:
            try:
                # 输入用户名及密码
                username_element = self.driver.find_element_by_id( self.username_id )
                username_element.clear()
                username_element.send_keys( self.username )

                password_element = self.driver.find_element_by_id( self.password_id )
                password_element.clear()
                password_element.send_keys( self.password )

                login_element = self.driver.find_element_by_id( self.login_button_id )
                login_element.click()
                print( '已登陆HPG，完成初始化操作' )

                return True
            except:
                print(self.now.getChinaTime(),'登陆失败')
                return False

        else:
            print( '登陆hpg：{}'.format( self.login_url ) )
            self.driver.get(self.login_url)
            time.sleep( 1 )
            self.login()

    def check_login(self):
        if self.driver.current_url in [self.user_url,self.task_url,self.submitted_url]:
            return True
        else:
            if self.login():
                return True

    def queue_task(self,normal = True):
        #print( '检查我要买' )
        if self.driver.current_url == self.task_url:
            self.today_finish()
            if normal:
                try:
                    normal_task = self.driver.find_element_by_id( 'normal-task' )
                    activity_task = self.driver.find_element_by_id( 'activity-task' )

                    if normal_task.text == '停止' and activity_task.text == '停止':
                        return True

                    elif normal_task.text == '我要买' and activity_task.text == '活动单':
                        normal_task.click()
                        #time.sleep( 1 )
                        activity_task.click()
                        #time.sleep( 1 )
                        print(self.now.getChinaTime(),'已订阅任务')
                        return True

                    else:return False

                except:
                    return False

            else:
                try:
                    traffic_task = self.driver.find_element_by_id('traffic-task'  )

                    if traffic_task.text == '停止':
                        return True

                    elif traffic_task.text == '我要找':
                        traffic_task.click()
                        time.sleep( 1 )
                        print( self.now.getChinaTime(), '已订阅任务' )
                        return True

                    else:
                        print( '没找到流量任务我要买1' )
                        return False

                except:
                    #print('没找到流量任务我要买2')
                    return False

        else:
            print('open:{}'.format(self.task_url))
            self.driver.get(self.task_url)
            time.sleep(1)
            self.queue_task(normal)

    def receive_task(self):
        #print('检查领取状态')
        if self.driver.current_url == self.task_url:

            #试着去找任务弹窗，刷新页面
            try:
                popop_task_item = self.driver.find_element_by_id('lsCustomDialog171125')
                time.sleep(2)
                self.driver.refresh()
                time.sleep(4)
            except:
                pass


            try:
                self.receiveButton = self.driver.find_element_by_xpath(self.receive_btn_xpath)

                if self.receiveButton.text == '请先验证宝贝':
                    self.getTaskInfo()
                    return True

                elif self.receiveButton.text == '领取':
                    #self.driver.execute_script( "arguments[0].scrollIntoView(false);", self.receiveButton )
                    self.driver.execute_script( "window.scrollTo(0,document.body.scrollHeight)" )
                    self.receiveButton.click()
                    time.sleep(1)

                    self.driver.refresh()
                    time.sleep(5)

                    print( '已领取任务，快做单' )
                    self.getTaskInfo()
                    print( '任务详情：',self.taskInfo )
                    send_email.send_email( '接到hpg任务', str(self.taskInfo ))

                    time.sleep(3)

                    self.receive_task()

            except:
                #print('没找到领取按钮，继续等待接收任务')
                return False

        else:
            print('open:{}'.format(self.task_url))
            self.driver.get(self.task_url)
            time.sleep(5)
            self.receive_task()



    def getTaskInfo(self):
        key_word = self.driver.find_element_by_xpath( '//*[@id="task-container"]/div[2]/div/input').get_attribute( 'value' )
        #print(key_word)
        main_link = self.driver.find_element_by_xpath( '//*[@id="task-container"]/*/img').get_attribute( 'src' )
        #print(main_link)
        price = self.driver.find_element_by_xpath( '//*[@id="task-container"]/div[4]' ).text
        task_remark = self.driver.find_element_by_xpath('//*[@id="task-container"]/div[5]').text
        remarks_word = self.driver.find_element_by_xpath( '//*[@id="goods-validate-hint"]' ).text
        #print(price,remarks_word)
        self.taskInfo = {'keyword': key_word,
                         'main_link': main_link,
                         'task_remark':task_remark,
                         'price': price,
                         'remarks_word': remarks_word,

                         }
        return self.taskInfo

    def check_goods(self,url):
        try:
            validate_item = self.driver.find_element_by_id('goods-validate-content')
            validate_item.send_keys( url )
            time.sleep(0.5)

            btn_item = self.driver.find_element_by_id('goods-validate-btn')
            btn_item.click()
            time.sleep(0.5)

            check_item=self.driver.find_element_by_id('goods-validate-message')
            print(check_item.get_attribute('class'))
            if check_item.get_attribute('class')=='pass':
                return True
            else:
                return False

        except:
            print('验证商品失败')

    def cancle(self):
        try:
            print('取消任务')
            cancle_element = self.driver.find_element_by_xpath('//*[@id="operation"]/a[1]')
            #print(cancle_element.text)
            self.driver.execute_script( "window.scrollTo(0,document.body.scrollHeight)" )
            cancle_element.click()

            try:
                yes_element = self.driver.find_element_by_xpath('//*[@id="lsCustomDialog171125"]/div[2]/div[2]/div[2]/a')
                self.driver.execute_script( "window.scrollTo(0,document.body.scrollHeight)" )
                yes_element.click()
            except:
                print('没找到确认按钮')
        except:
            print('没找到取消按钮')

    def submit(self):
        try:
            print('提交任务')
            submit_element = self.driver.find_element_by_xpath('//*[@id="operation"]/a[2]')
            self.driver.execute_script( "window.scrollTo(0,document.body.scrollHeight)" )
            submit_element.click()

        except:
            print( '没找到提交按钮' )

    def today_finish(self):
            try:
                today = self.driver.find_element_by_xpath('//*[@id="main-page"]/div[2]/div[4]/div[1]/div[1]/b')
                self.today = int(today.text)
                return self.today
            except:
                pass

if __name__ == '__main__':
    #测试验证链接
    hpg = HPG()
    hpg.connectChrome()
    hpg.check_login()

    hpg.today_finish()
    print(hpg.today)
    exit()
    print('订阅任务')
    hpg.queue_task()
    hpg.receive_task()


    url = 'https://detail.tmall.com/item.htm?id=567531156975&ns=1&abbucket=9'
    print( '验证' )
    if hpg.check_goods(url):
        hpg.submit()
    # else:
    #     hpg.cancle()










