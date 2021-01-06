from django.urls import path, include
from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('details/<pk>', views.details, name='details'),
    path('new_request', views.new_request, name='new_request'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('signout', views.signout, name='signout'),
    path('', views.index, name='index')
    ]
