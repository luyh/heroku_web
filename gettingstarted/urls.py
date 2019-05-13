from django.urls import include, path , re_path

from django.contrib import admin

admin.autodiscover()

import hello.views
import hpg.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="index"),
    path("login/", hello.views.login, name="login"),
    path("db/", hello.views.db, name="db"),
    path("admin/", admin.site.urls),
    path('hello/', hello.views.hello),

    re_path(r'passport/login.html$', hpg.views.login,name = 'login'),
    path('ajax_login/', hpg.views.ajax_login,name = 'ajax_login'),
    re_path(r'index/index.html$',hpg.views.index),
    re_path(r'user/index.html$',hpg.views.user)
]
