from transitions.extensions import HierarchicalMachine as Machine
import hpg2
import threading
import time

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
        self.normal = normal
        self.received = False
        self.task = None

        hpg.connect_chrome()
        hpg.start_refresh_thread( delay=60 )


    def run(self):
        while True:
            hpg.threadLock.acquire()

            old_state = hpg.state
            hpg.CheckLogin()

            if hpg.is_connectedChrome_loginHPG( allow_substates=True ):
                if not hpg.today_finish():
                    hpg.QuereTask( normal= True)
                else:
                    hpg.QuereTask(normal = False)

                hpg.ReceiveTask()

            if hpg.state != old_state:
                print( hpg.now.getChinaTime(), hpg.state )

            hpg.threadLock.release()

            time.sleep( 5 )



if __name__ == '__main__':
    test = HPG_thread(normal= False)
    test.start()
