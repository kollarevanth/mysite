from django.conf.urls import url
from django.urls import path,include
from django.contrib import admin
from django.conf import settings
from udan.views import *
urlpatterns=[
    path('screens',getScreenDetails),
    path('screens/<slug:slug>/reserve',reserve),
    path('screens/<slug:slug>/seats',unreservedSeats),
    path('screens/<slug:slug>/seats/<int:noOfSeats>/<slug:choice>',getChoiceBasedSeats)


]