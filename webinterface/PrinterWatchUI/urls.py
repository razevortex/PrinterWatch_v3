from django.urls import path

from . import views

urlpatterns = [
    path("page/", views.mainpage, name="mainpage"),
    path("plot/", views.plot, name="plot"),
    path("login/", views.login, name="login"),
]