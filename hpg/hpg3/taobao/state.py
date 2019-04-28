from transitions.extensions import HierarchicalMachine as Machine
import taobao
import threading
import time
from hpg.hpg3.hpg2.statemachine import HPG_thread
from hpg.hpg3.taobao import image
import os

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

            threadLock.release()

            time.sleep(30)


import requests
import cv2

import random



if __name__ == '__main__':
    hpg = HPG_thread( normal=False )
    hpg.start()

    taobao_thread = Taobao_thread()
    taobao_thread.start()

    while True:
        if taobao_thread.received:
            print( 'taobao搜索关键词：{}'.format( taobao_thread.task['keyword'] ) )
            taobao.search( taobao_thread.task['keyword'] )
            print( taobao_thread.task['main_link'] )
            time.sleep(3)

            good_pic = image.url_to_image( taobao_thread.task['main_link'] )
            # cv2.imshow( "good", good_pic )
            # cv2.waitKey( 0 )


            for page in range(5):

                goods = taobao.get_goods()
                # print( goods )

                for good in goods:
                    url = good['pic_url']
                    #print(url)
                    search_pic = image.url_to_image( url )
                    # cv2.imshow( "search_pic", search_pic )
                    # cv2.waitKey( 0 )
                    hist = image.classify_hist_with_split( good_pic, search_pic )
                    # ahash = image.classify_aHash( good_pic, search_pic )
                    # phash = image.classify_pHash( good_pic, search_pic )
                    print( hist )
                    if hist >0.99:
                        print('找到类似图片',hist,url)
                        break

                taobao.get_next_page(page)
                time.sleep( round( random.uniform( 3, 8 ), 2 ) )

            time.sleep(300)

        time.sleep(15)
        print('END')
