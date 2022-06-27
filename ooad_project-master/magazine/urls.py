from django.urls import URLPattern, path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('/success', views.success, name='success'),
    path('/payment/<int:id>', views.payment, name='payment'),
]