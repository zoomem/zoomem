from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'gdb_end/index.html')
