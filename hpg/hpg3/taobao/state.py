from transitions.extensions import HierarchicalMachine as Machine
import taobao
import threading
import time
from hpg_state import HPG_thread,hpg
from hpg.hpg3.taobao import image
import os
import requests
import cv2
import random
import datetime
import sys
from hpg.hpg3.ulity.china_time import chinatime
from hpg.hpg3.ulity.sms_twilio import msm


_output = sys.stdout

taobao = taobao.Taobao()

states = ['initial','connectedChrome','login','search','closedChrome']

machine = Machine( model=taobao, states=states, initial='initial' )
machine.add_transition( 'connect_chrome', 'initial', 'connectedChrome',
                        conditions='connectChrome' )

machine.add_transition( 'CheckLogin', '*', 'login',
                        conditions ='check_login' )

machine.add_transition( 'Search', 'login', 'search',)
#
# machine.add_transition( 'ReceiveTask', '*', 'connectedChrome_loginHPG_receivedTask',
#                         conditions='receive_task' )



class Taobao_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__( self )

        taobao.connect_chrome()
        taobao.chek_login()
        taobao.start_refresh_thread( delay=60 )


    def run(self):

        while True:
            if hpg.is_connectedChrome_loginHPG_receivedTask():
                target_pic = image.url_to_image( hpg.taskInfo['main_link'] )
                find = False
                for page in range( 15 ):

                    url = taobao.get_url( hpg.taskInfo['keyword'], page * 44 )


                    taobao.threadLock.acquire()
                    try:
                        taobao.driver.get( url )
                        goods = taobao.get_goods()
                    except:
                        print('taobao打开页面{}失败:{}'.format(page,url))

                    taobao.threadLock.release()

                    try:
                        print( chinatime.getChinaTime(), '对比页面{}图片'.format( page ) )
                        hists = image.classify_hist_with_split( target_pic, goods )
                        print( chinatime.getChinaTime(), '页面{}，hists:{}'.format(page,hists) )

                    except:
                        print('对比图失败')
                        continue
                    for good in goods:
                        if good['hist']>0.95:
                            find_url = good['good_url']
                            print( chinatime.getChinaTime(),'找到类似图片', good['hist'], find_url )

                            hpg.threadLock.acquire()
                            check = hpg.check_goods(find_url)
                            hpg.threadLock.release()

                            if check:

                                taobao.threadLock.acquire()
                                taobao.driver.get( good['good_url'] )
                                taobao.threadLock.release()

                                time.sleep(30)

                                if not hpg.today:
                                    msm( hpg.taskInfo, find_url )
                                else:
                                    hpg.threadLock.acquire()
                                    hpg.submit()
                                    hpg.threadLock.release()

                                find = True
                                break

                    if find == True:
                        break

                if find == False:
                    print( '没找到宝贝，取消订单' )
                    hpg.threadLock.acquire()
                    hpg.cancle()
                    hpg.threadLock.release()
                    time.sleep(15)

            time.sleep( 5 )

if __name__ == '__main__':
    hpg_thread = HPG_thread()
    hpg_thread.start()

    taobao_thread = Taobao_thread()
    taobao_thread.start()


