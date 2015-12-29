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
import json
from django.utils.safestring import mark_safe
gdb_adapters = {}

# Create your views here.
def index(request):
    return render(request, 'visualize/index.html',{'code':request.session["code"]})

def home(request):
    return render(request, 'visualize/home.html',{})

def submit(request):
    global gdb_adapters
    gdb_adapters[request.session.session_key] = createNewGdbAdapter(request.POST['code'], request.POST['input'])
    request.session["code"] = request.POST['code']
    request.session["input"] = request.POST['input']
    return index(request)

def update(request):
    var_name = ""
    if "var_name" in request.GET:
        var_name = request.GET["var_name"]
    g_data = getEdges(gdb_adapters[request.session.session_key],var_name)
    data = json.dumps({
        'edges': g_data["edges"],
        'cnt': g_data["cnt"],
        'line_num': gdb_adapters[request.session.session_key].getCurrnetLine(),
        'output':  gdb_adapters[request.session.session_key].readOutput(),
    })
    s = lambda: int(round(time.time() * 1000))
    print s()
    return HttpResponse(data, content_type='application/json')

def removeGraphEdges(request):
    var_name = ""
    if "del_name" in request.GET:
        var_name = request.GET["del_name"]
    g_adapter = gdb_adapters[request.session.session_key]
    edges = g_adapter.getGraphEdegs(var_name,'100')
    g_adapter.removeGraphEdges(edges)
    return update(request)

def reorder(txt):
    code = []
    non_include = 0
    lines = []
    line = ""
    for char in txt:
        line += char
        if char == '\n':
            lines.append(line)
            line = ""

    for line in lines:
        if len(line.strip()) >= 8 and line.strip()[0:8] == "#include" and non_include == 0:
            code.append(line)
        else:
            if non_include == 0:
                non_include = 1
                code.append("int dummyVaribleDeclaredToBeUsedToParseClangOutput__4zoomem;\n")
            code.append(line)
    return code

def next(request):
    step =  request.GET["step"]
    if(step == ""):
        step = 1
    gdb_adapters[request.session.session_key].next(step)
    return update(request)

def prev(request):
    step =  request.GET["step"]
    if(step == ""):
        step = 1
    gdb_adapters[request.session.session_key].prev(step)
    return update(request)

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

def createFile(txt,exten):
    file_name = randomword(20)
    if exten != "":
        f = open('visualize/static/cpp_files/' + file_name + exten,'w')
        f.write(txt)
        f.close()
        # _parsing file to be used to get the line for each var declartion
        if exten == ".cpp":
            f = open('visualize/static/cpp_files/' + file_name +"_parsing"+ exten,'w')
            new_code = reorder(txt)
            for line in new_code:
                f.write(line)
            f.close()
    return 'visualize/static/cpp_files/' + file_name

def compileFile(file_name):
    res = os.system("g++ -g -O0 -o " + file_name + " " + file_name + ".cpp")
    if(res != 0):
        raise Exception("Error Compiling file \n")

def createNewGdbAdapter(code,inpt):
    code_file_name = createFile(code,".cpp")
    input_file_name = createFile(inpt,".txt") + ".txt"
    output_file_name = createFile("",".txt") + ".txt"
    compileFile(code_file_name)
    return GdbAdapter(code_file_name,input_file_name,output_file_name)

def getEdges(g_adapter,var_name):
    depth = 0
    if var_name != "":
        depth = 1
    g = g_adapter.bulidGraph(g_adapter.getGraphEdegs(var_name,str(depth)))
    data = {}
    data["edges"] = g.getGraphEdges()
    data["cnt"] = g.id_cnt
    return data
