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

        hpg_thread = HPG_thread( normal=False )
        hpg_thread.start()

        taobao.connect_chrome()
        #taobao.chek_login()
        taobao.start_refresh_thread( delay=60 )


    def run(self):

        while True:
            if hpg.is_connectedChrome_loginHPG_receivedTask():
                good_pic = image.url_to_image( hpg.taskInfo['main_link'] )
                for page in range( 10 ):


                    url = taobao.get_url( hpg.taskInfo['keyword'], page * 44 )
                    #print( url )

                    taobao.threadLock.acquire()
                    taobao.driver.get( url )
                    goods = taobao.get_goods()
                    taobao.threadLock.release()

                    # print( goods )
                    for good in goods:
                        url = good['pic_url']
                        # print(url)
                        # starttime = datetime.datetime.now()
                        search_pic = image.url_to_image( url )
                        # endtime = datetime.datetime.now()
                        # print('下载及读取图片用时:',(endtime - starttime).seconds,url)
                        # cv2.imshow( "search_pic", search_pic )
                        # cv2.waitKey( 0 )

                        # starttime = datetime.datetime.now()
                        hist = image.classify_hist_with_split( good_pic, search_pic )
                        # endtime = datetime.datetime.now()
                        # print('比较图片用时:', (endtime - starttime).seconds)
                        # ahash = image.classify_aHash( good_pic, search_pic )
                        # phash = image.classify_pHash( good_pic, search_pic )

                        print( 'page:{},id:{},hist:{}'.format( page, good['id'], hist ) )
                        if hist == 1:
                            find_url = good['good_url']
                            print( '找到类似图片', hist, find_url )

                            hpg.threadLock.acquire()
                            if hpg.check_goods(find_url):
                                hpg.submit()
                                break
                            hpg.threadLock.acquire()

                print( '实在没找到，取消订单' )
                hpg.threadLock.acquire()
                hpg.cancle()
                taobao.threadLock.release()

            time.sleep( 5 )

if __name__ == '__main__':


    taobao_thread = Taobao_thread()
    taobao_thread.start()


