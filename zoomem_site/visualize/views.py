from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
import sys
sys.path.append("visualize/graph_py")
from gdb_adapter import GdbAdapter
from graph import gdbGraph
import random, string
import os
import time
from django.http import JsonResponse
from django.utils.safestring import mark_safe
gdb_adapters = {}

# Create your views here.
def index(request):
    edges = mark_safe(getEdges(gdb_adapters[request.session.session_key]))
    return render(request, 'visualize/index.html',{"edges":edges,"code":request.session["code"],"output":request.session["output"]})

def home(request):
    return render(request, 'visualize/home.html',{})

def submit(request):
    global gdb_adapters
    gdb_adapters[request.session.session_key] = createNewGdbAdapter(request.POST['code'], request.POST['input'])
    request.session["code"] = request.POST['code']
    request.session["output"] = ""
    return index(request)

def next(request):
    gdb_adapters[request.session.session_key].next()
    request.session["output"] = gdb_adapters[request.session.session_key].readOutput()
    return index(request)

def prev(request):
    gdb_adapters[request.session.session_key].prev()
    request.session["output"] = gdb_adapters[request.session.session_key].readOutput()
    return index(request)

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

def createFile(txt,exten):
    file_name = randomword(20)
    if exten != "":
        f = open('visualize/static/cpp_files/' + file_name + exten,'w')
        f.write(txt)
        f.close()
    return 'visualize/static/cpp_files/' + file_name

def compileFile(file_name):
    res = os.system("g++ -g -o " + file_name + " " + file_name + ".cpp")
    if(res != 0):
        raise Exception("Error Compiling file \n")

def createNewGdbAdapter(code,inpt):
    code_file_name = createFile(code,".cpp")
    input_file_name = createFile(inpt,".txt") + ".txt"
    output_file_name = createFile("",".txt") + ".txt"
    compileFile(code_file_name)
    return GdbAdapter(code_file_name,input_file_name,output_file_name)

def getEdges(g_adapter):
    g = g_adapter.bulidGraph(g_adapter.getGraphEdegs())
    return g.getGraphEdges()
