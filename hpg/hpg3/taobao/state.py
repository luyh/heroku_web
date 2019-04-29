from transitions.extensions import HierarchicalMachine as Machine
import taobao
import threading
import time
from hpg.hpg3.hpg2.statemachine import HPG_thread
from hpg.hpg3.taobao import image
import os
import requests
import cv2
import random
import datetime

threadLock = threading.Lock()
threads = []

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

        self.task = None
        self.received = False

    def run(self):
        while True:
            threadLock.acquire()
            taobao.driver.refresh()
            if hpg.received:
                self.received = True
                self.task = hpg.task

            taobao.driver.refresh()
            threadLock.release()
            time.sleep(30)



if __name__ == '__main__':
    hpg = HPG_thread( normal=False )
    hpg.start()

    taobao_thread = Taobao_thread()
    taobao_thread.start()

    while True:
        find = False
        if taobao_thread.received:
            good_pic = image.url_to_image( taobao_thread.task['main_link'] )
            for page in range(10):
                if find == True:
                    break
                url = taobao.get_url(taobao_thread.task['keyword'], page*44)
                print(url)
                taobao.driver.get(url)
                time.sleep(1)
                goods = taobao.get_goods()
                # print( goods )
                find = False
                for good in goods:
                    url = good['pic_url']
                    #print(url)
                    #starttime = datetime.datetime.now()
                    search_pic = image.url_to_image( url )
                    #endtime = datetime.datetime.now()
                    #print('下载及读取图片用时:',(endtime - starttime).seconds,url)
                    # cv2.imshow( "search_pic", search_pic )
                    # cv2.waitKey( 0 )

                    #starttime = datetime.datetime.now()
                    hist = image.classify_hist_with_split( good_pic, search_pic)
                    #endtime = datetime.datetime.now()
                    #print('比较图片用时:', (endtime - starttime).seconds)
                    # ahash = image.classify_aHash( good_pic, search_pic )
                    # phash = image.classify_pHash( good_pic, search_pic )
                    print( 'page:{},id:{},hist:{}'.format(page,good['id'],hist) )
                    if hist ==1:
                        find_url = good['good_url']
                        print('找到类似图片',hist,find_url)
                        find =True
                        break

                time.sleep( round( random.uniform(1, 3 ), 2 ) )

            time.sleep(300)

        time.sleep(15)
        print('END')
