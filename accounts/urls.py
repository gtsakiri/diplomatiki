from django.urls import path, re_path, include
from . import views

app_name="accounts"
urlpatterns = [
path('login/<int:eklid>', views.login_user, name='login'),
path('logout/<int:eklid>', views.logout_user, name='logout'),
]

