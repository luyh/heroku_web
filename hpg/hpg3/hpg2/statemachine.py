from transitions.extensions import HierarchicalMachine as Machine
from hpg.hpg3.hpg2 import hpg2
import threading
import time
threadLock = threading.Lock()
threads = []

hpg = hpg2.HPG()

states = ['initial',

          {'name' : 'connectedChrome','children':[

              {'name':'loginHPG','children':[
                  'quereedTask',
                  'receivedTask',
                        ]},

               ],
           },

          'closedChrome',
          ]

machine = Machine( model=hpg, states=states, initial='initial' )
machine.add_transition( 'connect_chrome', 'initial', 'connectedChrome',
                        conditions='connectChrome' )

machine.add_transition( 'CheckLogin', '*', 'connectedChrome_loginHPG',
                        conditions ='check_login' )

machine.add_transition( 'QuereTask', '*', 'connectedChrome_loginHPG_quereedTask',
                        conditions='queue_task' )

machine.add_transition( 'ReceiveTask', '*', 'connectedChrome_loginHPG_receivedTask',
                        conditions='receive_task' )




class HPG_thread(threading.Thread):
    def __init__(self,normal = True):
        threading.Thread.__init__( self )
        self.connect_chrome()
        self.normal = normal
        self.received = False
        self.task = None

    def run(self):
        while True:
            self.quere_up_task()

    def connect_chrome(self):
        print( hpg.state )
        hpg.connect_chrome()

    def quere_up_task(self):
        hpg.CheckLogin()

        if hpg.is_connectedChrome_loginHPG( allow_substates=True ):
            hpg.QuereTask( self.normal )
            hpg.ReceiveTask()

        print( hpg.now.getChinaTime(), hpg.state )

        if hpg.is_connectedChrome_loginHPG_receivedTask():
            print( '接到任务' )
            threadLock.acquire()
            self.received = True
            self.task = hpg.getTaskInfo()
            print(self.task)
            threadLock.release()
            time.sleep( 60 )
            hpg.driver.refresh()
        else:
            self.received = False
            time.sleep( 30 )
            hpg.driver.refresh()

if __name__ == '__main__':
    test = HPG_thread(normal= False)
    test.start()
