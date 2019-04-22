from django.shortcuts import render
from django.http import HttpResponse
from gettingstarted import zkb_thread
import threading

threadLock = threading.Lock()


# Create your views here.
def zkb(request):

    # print(1,driver.page_source)
    context = {}
    threadLock.acquire()
    driver = zkb_thread.driver
    context['hello'] = zkb_thread.state
    threadLock.release()

    return render( request, 'hello.html', context )