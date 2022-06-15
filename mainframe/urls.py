from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainframeset),
    path('help/', views.help),
]
