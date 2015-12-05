from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
import sys
sys.path.append("/home/tk/git_workplace/zoomem/zoomem_site/visualize/graph_py")
from gdb_adapter import GdbAdapter

# Create your views here.
def index(request):
    path = "/home/tk/git_workplace/zoomem/zoomem_site/visualize/graph_py/"
    g_adapter = GdbAdapter(path + "sample",path + "in.txt")
    edges = g_adapter.getGraphEdegs()
    context = {}
    context["edges"] = edges
    return render(request, 'visualize/index.html',context)
