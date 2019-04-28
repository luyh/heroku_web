from transitions.extensions import HierarchicalMachine as Machine
import zkb
import threading
import time

zkb = zkb.ZKB()

states = ['initial',

          {'name' : 'connectedChrome','initial' :'logoutZKB' ,'children':[
              'prelogin',
              'input_vatification_code',

              {'name':'loginZKB','children':[
                  'quereedTask',
                  'receivedTask',
                        ]},

               'logoutZKB'],
           },

          'closedChrome',
          ]

machine = Machine( model=zkb, states=states, initial='initial' )
machine.add_transition( 'connect_chrome', 'initial', 'connectedChrome',
                        conditions='connectChrome' )

machine.add_transition( 'CheckLogin', '*', 'connectedChrome_logoutZKB',
                        unless='check_login' )


machine.add_transition( 'CheckLogin', '*', 'connectedChrome_loginZKB',
                        conditions ='check_login' )


machine.add_transition( 'Login', 'connectedChrome_logoutZKB', 'connectedChrome_prelogin',
                        conditions ='login' )

machine.add_transition( 'Vartifacation', 'connectedChrome_prelogin', 'connectedChrome_loginZKB',
                        conditions ='input_vertify_code' )

machine.add_transition( 'QuereTask', '*', 'connectedChrome_loginZKB_quereedTask',
                        conditions='queue_task' )

machine.add_transition( 'ReceiveTask', '*', 'connectedChrome_loginZKB_receivedTask',
                        conditions='receive_task' )


def connect_chrome():
    print( zkb.state )
    zkb.connect_chrome()

def quere_up_task():
    old_state = zkb.state
    while True:
            zkb.CheckLogin()

            if zkb.is_connectedChrome_logoutZKB():
                print('登陆',zkb.state)
                zkb.Login()
                print( '输入用户资料', zkb.state )

            if zkb.is_connectedChrome_prelogin():
                print('输入验证码',zkb.state)
                zkb.Vartifacation(count = 5,delay =1)

            if zkb.is_connectedChrome_loginZKB(allow_substates=True):
                zkb.QuereTask()
                zkb.ReceiveTask()

            print(zkb.now.getChinaTime() ,zkb.state)

            if zkb.is_connectedChrome_loginZKB_receivedTask():
                print( '接到任务' )
                time.sleep(300)
                zkb.driver.refresh()
            else:
                time.sleep( 15 )
                zkb.driver.refresh()


if __name__ == '__main__':
    connect_chrome()
    quere_up_task()
