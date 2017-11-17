from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^Demo$', views.show_demo, name='show_demo'),
    url(r'^Demo/analyze/$', views.getAnalyze_senti, name='getAnalyze_senti'),
    url(r'^MovieGuide$', views.show_movie, name='show_movie'),
    url(r'^Slide$', views.show_slide, name='show_slide'),
    url(r'^MovieGuide/MovieInfo/$', views.getMovieInfo, name='getMovieInfo'),
    url(r'^MovieGuide/MovieReviews/$', views.getMovieReviews, name='getMovieReviews'),
    url(r'^MovieGuide/getStory/$', views.getStory, name='getStory'),
    url(r'^MovieGuide/MovieDetailInfo/$', views.getMovieDetailInfo, name='getMovieDetailInfo'),
    url(r'^MovieGuide/MovieLikeHate/$', views.cal_LikeHate, name='cal_LikeHate'),
]