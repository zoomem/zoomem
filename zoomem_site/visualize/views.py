from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
import sys
sys.path.append("/home/tk/git_workplace/zoomem/zoomem_site/visualize/graph_py")
from gdb_adapter import GdbAdapter
from graph import gdbGraph

# Create your views here.
def index(request):
    path = "/home/tk/git_workplace/zoomem/zoomem_site/visualize/graph_py/"
    g_adapter = GdbAdapter(path + "sample",path + "in.txt")
    g_adapter.next()
    g_adapter.next()
    edges = g_adapter.getGraphEdegs()
    g_gdb = gdbGraph()
    g_gdb = g_adapter.bulidGraph(edges)
    context = {}
    edges = g_gdb.getGraphEdges()
    context["edges"] = edges
    print edges
    return render(request, 'visualize/index.html',context)

def home(request):
    return render(request, 'visualize/home.html',{})

def submit(request):
    print "hey"
    code = request.POST['code']
    print code
    return render(request, 'visualize/home.html',{})
