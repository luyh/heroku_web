from hpg2 import HPG
from transitions.extensions import HierarchicalMachine as Machine
from states import states
import time
import threading
from ulity import china_time,send_email


# # Set up logging; The basic log level will be DEBUG
# import logging
# logging.basicConfig(level=logging.DEBUG)
# # Set transitions' log level to INFO; DEBUG messages will be omitted
# logging.getLogger('transitions').setLevel(logging.INFO)

threadLock = threading.Lock()
threads = []

hpg = HPG()
machine = Machine( hpg, states=states,initial='initial' )
####
machine.add_transition('connect_chrome','initial','connectedChrome',conditions='connectChrome')

#####
machine.add_transition('CheckLogin','*','loginHPG',
                       conditions= 'check_login')

machine.add_transition('QuereTask','*','quereedTask',
                       conditions='queue_task')

machine.add_transition('ReceiveTask','*','receivedTask',
                       conditions= 'receive_task')

print(hpg.state)
old_state = hpg.state

hpg.connect_chrome()

now = china_time.ChinaTime()

send_email.send_email( '接到hpg任务', hpg.now.getChinaTime() )

while(1):
    hpg.CheckLogin()
    hpg.QuereTask()
    hpg.ReceiveTask()

    if hpg.state != old_state:
        print(now.getChinaTime(), hpg.state )

    old_state = hpg.state
    hpg.driver.refresh()
    time.sleep( 15 )

class ReceivingTaskThread(threading.Thread):
    def __init__(self,hpg,delay = 10):
        threading.Thread.__init__(self)
        self.threadID = 'ReceivingTaskThread'
        self.delay = delay
        self.hpg = hpg

        self.hpg.connect_chrome()
        print(hpg.state)

        self.hpg.driver.refresh()
        time.sleep(5)

        self.hpg.Login()
        print( hpg.state )

        self.hpg.QuereTask()
        print( hpg.state )

        self.hpg.start_refresh_thread( 30 )

    def run(self):
        now = china_time.ChinaTime()
        old_state = hpg.state

        while(1):
            if hpg.state != old_state:
                print(now.getChinaTime(), hpg.state )

            threadLock.acquire()
            self.hpg.CheckLogOut()
            self.hpg.QuereTask()
            self.hpg.ReceiveTask()

            threadLock.release()

            old_state = hpg.state
            time.sleep(self.delay)

# receivingTaskThread = ReceivingTaskThread(hpg)
# receivingTaskThread.start()

print('End')