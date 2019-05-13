from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from hpg.hpg3.hpg_request import HPG
import os,time,json


# hpg.set_running_status(0,0,1)
#
# hpg.request_continue()
#
# hpg.receive_task()

# Create your views here.
def login(request):
    return render( request, "login.html" )

def ajax_login(request):
    username = request.POST['username']
    password = request.POST['password']

    # username = os.environ.get( 'HPG_USER' )  # 用户名
    # password = os.environ.get( 'HPG_PASS' )  #

    print( username, password )

    hpg = HPG( username, password, debug=True )

    response = hpg.ajax_login()
    print(response)

    return HttpResponse(json.dumps(response), content_type='application/json')

def index(request):
    response = redirect('../user/index.html')

    return response

def user(request):
    return HttpResponse('user page')

