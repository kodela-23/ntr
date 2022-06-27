
from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('register',views.register,name="register"),
    path('login',views.login,name="login"),
    path('logout',views.logout,name='logout'),
    path('changePassword',views.changePassword,name="changePassword"),
    path('setNewPassword',views.setNewPassword,name="setNewPassword")
]