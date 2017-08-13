from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^MainPage$', views.show_main, name='show_main'),
    url(r'^Intro$', views.show_intro, name='show_intro'),
    url(r'^Demo$', views.show_demo, name='show_demo'),
]