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

# Create your views here.
def index(request,code_file_name = None,input_file_name = None):
    g_adapter = GdbAdapter(code_file_name,input_file_name)
    g = g_adapter.bulidGraph(g_adapter.getGraphEdegs())
    edges = g.getGraphEdges()
    return render(request, 'visualize/index.html',{"edges":edges,"code":request.POST['code'].strip()})

def home(request):
    return render(request, 'visualize/home.html',{})

def submit(request):
    code = request.POST['code']
    inpt = request.POST['input']
    code_file_name = createFile(code,".cpp")
    input_file_name = createFile(inpt,".txt") + ".txt"
    print code_file_name , input_file_name

    compileFile(code_file_name)
    return index(request,code_file_name,input_file_name)

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

def createFile(txt,exten):
    file_name = randomword(20)
    f = open('visualize/static/cpp_files/' + file_name + exten,'w')
    f.write(txt)
    f.close()
    return 'visualize/static/cpp_files/' + file_name

def compileFile(file_name):
    res = os.system("g++ -g -o " + file_name + " " + file_name + ".cpp")
    if(res != 0):
        raise Exception("Error Compiling file \n")
