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
    path('hpg/', hpg.views.hpg,name = 'hpg'),
]
