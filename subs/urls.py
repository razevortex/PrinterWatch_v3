from django.urls import path
from . import views

urlpatterns = [
    path('deviceMgr/', views.dmgr),
    path('userMgr/', views.umgr),
    path('monitor/', views.PrintMonitor),
    path('storage_tracker/', views.cartTrack),
    path('analytics/', views.analytics),
    path('details/', views.details),
]
