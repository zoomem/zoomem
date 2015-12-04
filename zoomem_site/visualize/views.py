from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
import sys

# Create your views here.
def index(request):
    return render(request, 'visualize/index.html')
