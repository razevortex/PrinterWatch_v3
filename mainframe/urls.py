from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainframeset),
    path('signup/', views.signup),
    path('help/', views.help),
]
