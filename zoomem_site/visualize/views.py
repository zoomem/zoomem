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
    context  = {}
    context["edges"] = getEdges(gdb_adapters[request.session.session_key])
    context["line_num"] = gdb_adapters[request.session.session_key].getCurrnetLine()
    context["code"] = request.session["code"]
    context["output"] = request.session["output"]

    return render(request, 'visualize/index.html',context)

def home(request):
    return render(request, 'visualize/home.html',{})

def submit(request):
    global gdb_adapters
    gdb_adapters[request.session.session_key] = createNewGdbAdapter(request.POST['code'], request.POST['input'])
    request.session["code"] = request.POST['code']
    request.session["input"] = request.POST['input']
    request.session["output"] = ""
    return index(request)

def first(request):
    gdb_adapters[request.session.session_key] = createNewGdbAdapter(request.session["code"],request.session["input"])
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

def go_to(request):
    line =  request.GET["line"]
    gdb_adapters[request.session.session_key].goToLine(line)
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
