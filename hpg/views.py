from django.shortcuts import render
from django.http import HttpResponse
from hpg.hpg3.hpg_request import HPG
import os,time


# hpg.set_running_status(0,0,1)
#
# hpg.request_continue()
#
# hpg.receive_task()

# Create your views here.
def hpg(request):
    ctx = {}
    username='空'
    password=None

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        if username==None:username='空'

        # username = os.environ.get( 'HPG_USER' )  # 用户名
        # password = os.environ.get( 'HPG_PASS' )  #


        print( username, password )

        hpg = HPG( username, password, debug=True )

        hpg.login()

        ctx['username'] = '您登陆的用户名为:'+username
        if hpg.Login:
            ctx['login_status'] = '您已登后台陆红苹果后台接单用手'
        else:
            ctx['login_status'] = '登陆失败，请检查红苹果帐号密码是否正确'

    return render( request, "login.html", ctx )

def post(request):
    ctx = {}

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        # username = os.environ.get( 'HPG_USER' )  # 用户名
        # password = os.environ.get( 'HPG_PASS' )  #

        print( username, password )

        hpg = HPG( username, password, debug=True )

        ctx['username'] = '您登陆的帐号为：{username}'.format()
        if hpg.Login:
            ctx['login_status'] = '您已登后台陆红苹果'
        else:
            ctx['login_status'] = '登陆失败，请检查帐号密码是否正确'

    return render( request, "login.html", ctx )



