from django.conf.urls import url
from django.contrib.auth import authenticate, login
from django.urls import path, re_path, include
from . import views

app_name="accounts"
urlpatterns = [
path('login_user/<int:eklid>', views.login_user, name='login'),
path('logout_user/<int:eklid>', views.logout_user, name='logout'),
]

