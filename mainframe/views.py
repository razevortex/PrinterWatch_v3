from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def mainframeset(request):
    return render(request, 'mainframeset.html')
