from hpg.hpg3.chrome.connect_chrome import Chrome
from hpg.hpg3.ulity import china_time,send_email
import os,time
import threading

class ZKB(Chrome):


    def __init__(self, name='zkb', debug=False, mobileEmulation=None):
        self.name = name
        self.driver = None

        self.threadLock = threading.Lock()

        self.username = os.environ.get( 'HPG_USER' )  # 用户名
        self.password = os.environ.get( 'HPG_PASS' )  #

        self.login_url = 'http://zhuankeban.com/jsp/Mobile/apprentice/ApprenticeLogin.jsp'
        self.task_url = 'http://zhuankeban.com/webmobile/apprentice/toBuy.do'
        self.submitted_url = 'http://zhuankeban.com//jsp/Mobile/apprentice/Task.jsp?ut=apprentice'
        self.user_url = 'http://zhuankeban.com/jsp/Mobile/apprentice/ApprenticeInfo.jsp'
        self.receive_url = ''

        self.username_id = 'user_account'
        self.password_id = 'user_password'
        self.login_button_id = 'Signin'
        self.receive_btn_xpath = '//*[@id="dummybodyid"]/section/div[3]/div/div[2]'

        self.taskInfo = None
        self.taskInfoFlag = False

        self.now = china_time.ChinaTime()



    def login(self):
        if self.driver.current_url in self.login_url:
            self.driver.refresh()
            time.sleep(1)
            try:
                print( '输入用户名及密码...' )
                username = os.environ.get( 'HPG_USER' )  # 用户名
                username_element = self.driver.find_element_by_id( 'user_account' )
                username_element.clear()
                username_element.send_keys( username )

                password = os.environ.get( 'HPG_PASS' )  #
                password_element = self.driver.find_element_by_id( 'user_password' )
                password_element.clear()
                password_element.send_keys( password )

                return True

            except:
                print( self.now.getChinaTime(), '输入帐号密码异常，登陆失败' )
                return False

        else:
            print( '登陆zkb：{}'.format( self.login_url ) )
            self.driver.get(self.login_url)
            time.sleep( 3 )
            self.login()

    def input_vertify_code(self,count = 5,delay =5):
        try:
            verification_code_element = self.driver.find_element_by_id( 'verification_code' )
            verification_code_element.clear()

            value = verification_code_element.get_attribute( 'value' )

            while count:
                print( '请输入验证码' ,count)
                time.sleep( delay )
                value = verification_code_element.get_attribute( 'value' )
                count = count -1

                if value != '':
                    print( '点击登陆...' )
                    sighinButton = self.driver.find_element_by_id( 'Signin' )
                    sighinButton.click()
                    time.sleep( 1 )
                    print( '已登陆zkb' )
                    return True

            return False

        except:
            print('输入验证码报错')
            return False



    def check_login(self):
        if 'zhuankeban.com' in self.driver.current_url:
            if '{"code":"666","msg":"登录失效","success":false}' in self.driver.page_source:
                return False
            elif "Login" in self.driver.current_url:
                return False
            else:
                return True
        else:
            return False

    def queue_task(self):
        # print( '检查我要买' )
        if self.driver.current_url == self.task_url:
            try:
                task_element = self.driver.find_element_by_id( 'queue-up-task' )

                if task_element.text == '停止':
                    return True

                elif task_element.text == '我要买' :
                    task_element.click()
                    time.sleep( 1 )
                    print( self.now.getChinaTime(), '已订阅任务' )
                    return True

                else:
                    return False

            except:
                print( '没找到我要买按钮' )
                return False

        else:
            print( 'open:{}'.format( self.task_url ) )
            self.driver.get( self.task_url )
            time.sleep( 3 )
            self.queue_task()

    def receive_task(self):
        # print('检查领取状态')
            try:
                self.receiveButton = self.driver.find_element_by_xpath(self.receive_btn_xpath)

                if self.receiveButton.text == '提交':
                    return True

                elif self.receiveButton.text == '领取':
                    print(self.driver.current_url)
                    print( '已接到任务，准备领取' )
                    # self.driver.execute_script( "arguments[0].scrollIntoView(false);", self.receiveButton )
                    self.driver.execute_script( "window.scrollTo(0,document.body.scrollHeight)" )
                    self.receiveButton.click()

                    print( '已领取任务，快做单' )
                    self.getTaskInfo()
                    print( self.taskInfo )
                    send_email.send_email( '接到hpg任务', self.taskInfo )

                    return True

            except:
                # print('没找到领取按钮，继续等待接收任务')
                return False

    def getTaskInfo(self):
        key_word = self.driver.find_element_by_xpath( '//*[@id="task-container"]/div[2]/div/input').get_attribute( 'value' )
        #print(key_word)
        main_link = self.driver.find_element_by_xpath( '//*[@id="task-container"]/div[3]/img').get_attribute( 'src' )
        #print(main_link)
        price = self.driver.find_element_by_xpath( '//*[@id="task-container"]/div[4]' ).text
        remarks_word = self.driver.find_element_by_xpath( '//*[@id="goods-validate-hint"]' ).text
        #print(price,remarks_word)
        self.taskInfo = {'keyword': key_word,
                         'main_link': main_link,
                         'price': price,
                         'remarks_word': remarks_word,

                         }

    def taskInfo(self):  #TODO:
        key_word = self.driver.find_element_by_id( 'target' ).get_attribute( 'value' )
        # print(key_word)
        main_link = self.driver.find_element_by_class_name( 'main_link' ).get_attribute( 'src' )
        # print(main_link)
        price = self.driver.find_element_by_class_name( 'customer_order' ).text
        remarks_word = self.driver.find_element_by_class_name( 'remarks_word' ).text
        # print(price,remarks_word)
        return key_word, main_link, price, remarks_word





if __name__ == '__main__':
    zkb = ZKB()
    zkb.connectChrome()
