import sys
import random
import string
import os
import time
import json
sys.path.append("visualize/graph_py")
from visualize.models import CodeData
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from gdb_adapter import GdbAdapter, ProcRunTimeError
from graph import gdbGraph
from subprocess import Popen, PIPE
from proc import TimeLimitError
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from datetime import datetime

gdb_adapters = {}


class CompilationError(Exception):

    def __init__(self, message, errors):
        super(CompilationError, self).__init__(message)
        self.errors = errors

# Create your views here.


def index(request):
    session_id = int(request.GET["session_id"])
    code = CodeData.objects.get(id=session_id).code
    return render(request, 'visualize/index.html', {'code': code, 'session_id': session_id, 'valid': validEdit(session_id, request)})


def home(request):
    code = "#include <iostream>\nusing namespace std;\nint main()\n{\n  return 0;\n}"
    inpt = ""
    session_id = "none"
    if 'session_id' in request.GET:
        code_data = CodeData.objects.get(id=request.GET['session_id'])
        code = code_data.code
        inpt = code_data.code_input
        session_id = request.GET["session_id"]
    return render(request, 'visualize/home.html', {'code': code, 'input': inpt, 'session_id': session_id})


def submit(request):
    global gdb_adapters
    try:
        submitted_code_data = None
        if not request.session.exists(request.session.session_key):
            request.session.create()
        if "session_id" in request.POST and request.POST["session_id"] != "none":
            session_id = int(request.POST["session_id"])
            if validEdit(session_id, request):
                submitted_code_data = CodeData.objects.get(id=session_id)
                submitted_code_data.code = request.POST['code']
                submitted_code_data.code_input = request.POST['input']
            else:
                return
        else:
            submitted_code_data = CodeData(code=request.POST['code'], code_input=request.POST[
                                           'input'], code_key=request.session.session_key)
        submitted_code_data.save()
        gdb_adapters[submitted_code_data.id] = createNewGdbAdapter(
            request.POST['code'], request.POST['input'], submitted_code_data.id)
        return HttpResponseRedirect("/visualize/index?session_id=" + str(submitted_code_data.id))
    except CompilationError as e:
        e.message = e.message.replace("visualize/static/cpp_files/", "\n/")
        return render(request, 'visualize/error.html', {'error': e.message, 'error_type': e.errors, 'state': "compile", 'session_id': submitted_code_data.id})


def render_graph(request,session_id = ""):
    if(session_id == ""):
        session_id = int(request.GET["session_id"])
    data = json.dumps({
        'edges': gdb_adapters[session_id].graph.getGraphEdges(),
        'cnt': gdb_adapters[session_id].graph.id_cnt,
        'line_num': gdb_adapters[session_id].getCurrnetLine(),
        'output':  gdb_adapters[session_id].readOutput(),
        'vis_arrays
':gdb_adapters[session_id].vis_arrays
    })
    return HttpResponse(data, content_type='application/json')


def new_data(request):
    session_id = int(request.GET["session_id"])
    last_seen = 0
    if 'last_seen' in request.GET:
        last_seen = datetime.strptime(
            request.GET['last_seen'], "%a, %d %b %Y %H:%M:%S %Z")
    if last_seen == 0 or gdb_adapters[session_id].lastChanged() > last_seen:
        return HttpResponse("true")
    return HttpResponse("false")


def next(request):
    session_id = int(request.GET["session_id"])
    if not validEdit(session_id, request):
        return
    try:
        step = request.GET["step"]
        if(step == ""):
            step = 1
        gdb_adapters[session_id].next(step)
        return render_graph(request)
    except ProcRunTimeError as e:
        gdb_adapters[session_id].exitProcess()
        return render(request, 'visualize/error.html', {'error': e.message, 'error_type': e.errors, 'state': "run", 'session_id': session_id})
    except TimeLimitError as e:
        gdb_adapters[session_id].exitProcess()
        line = str(gdb_adapters[session_id].current_line)
        gdb_adapters[session_id].exitProcess()
        return render(request, 'visualize/error.html', {'error': "Faild it line " + line, 'error_type': e.errors, 'state': 'run', 'session_id': session_id})


def prev(request):
    session_id = int(request.GET["session_id"])
    if not validEdit(session_id, request):
        return
    step = request.GET["step"]
    if(step == ""):
        step = 1
    gdb_adapters[session_id].prev(step)
    return render_graph(request)


def go_to_line(request):
    session_id = int(request.GET["session_id"])
    if not validEdit(session_id, request):
        return
    try:
        step = request.GET["line"]
        if(step == ""):
            step = 1
        gdb_adapters[session_id].goToLine(line)
        return render_graph(request)
    except ProcRunTimeError as e:
        gdb_adapters[session_id].exitProcess()
        return render(request, 'visualize/error.html', {'error': e.message, 'error_type': e.errors, 'state': "run", 'session_id': session_id})
    except TimeLimitError as e:
        gdb_adapters[session_id].exitProcess()
        line = str(gdb_adapters[session_id].current_line)
        gdb_adapters[session_id].exitProcess()
        return render(request, 'visualize/error.html', {'error': "Faild it line " + line, 'error_type': e.errors, 'state': 'run', 'session_id': session_id})


def end_funciton(request):
    session_id = int(request.GET["session_id"])
    if not validEdit(session_id, request):
        return
    gdb_adapters[session_id].endFunciton()
    return render_graph(request)


def stack_up(request):
    session_id = int(request.GET["session_id"])
    if not validEdit(session_id, request):
        return
    gdb_adapters[session_id].stackUp()
    return render_graph(request)


def stack_down(request):
    session_id = int(request.GET["session_id"])
    if not validEdit(session_id, request):
        return
    gdb_adapters[session_id].stackDown()
    return render_graph(request)


def add_graph_edges(request):
    data = {}
    for x in request.POST:
        data = json.loads(x)
    session_id = int(data.get("session_id",''))
    if not validEdit(session_id, request):
        return
    array_ident = data.get("array_ident",'').strip()
    var_name =  data.get("var_name",'').strip()
    g_adapter = gdb_adapters[session_id]
    g_adapter.makeVarVis(var_name, array_ident)
    return render_graph(request,session_id)



def remove_graph_edges(request):
    data = {}
    for x in request.POST:
        data = json.loads(x)
    session_id = int(data.get("session_id",''))
    if not validEdit(session_id, request):
        return
    array_ident = data.get("array_ident",'').strip()
    var_name =  data.get("var_name",'').strip()
    g_adapter = gdb_adapters[session_id]
    g_adapter.makeVarNotVis(var_name, array_ident)
    return render_graph(request,session_id)

# anything below this line can't be accessd from urls k ?


def validEdit(session_id, request):
    return (CodeData.objects.get(id=session_id).code_key == request.session.session_key)


def getRecorderLines(txt):
    lines = []
    line = ""
    for char in txt:
        line += char
        if char == '\n':
            lines.append(line)
            line = ""
    return lines


def reorder(txt):
    non_include = 0
    code = []
    for line in getRecorderLines(txt):
        if len(line.strip()) >= 8 and line.strip()[0:8] == "#include" and non_include == 0:
            code.append(line)
        else:
            if non_include == 0:
                non_include = 1
                code.append(
                    "int dummyVaribleDeclaredToBeUsedToParseClangOutput__4zoomem;\n")
            code.append(line)
    return code


def randomWord(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))


def createFile(txt, exten):
    file_name = randomWord(20)
    if exten != "":
        f = open('visualize/static/cpp_files/' + file_name + exten, 'w')
        f.write(txt)
        f.close()
        # _parsing file to be used to get the line for each var declartion
        if exten == ".cpp":
            f = open('visualize/static/cpp_files/' +
                     file_name + "_parsing" + exten, 'w')
            new_code = reorder(txt)
            for line in new_code:
                f.write(line)
            f.close()
    return 'visualize/static/cpp_files/' + file_name


def compileFile(file_name):
    proc = Popen("g++ -g -w -O0 -o " + file_name + " " + file_name +
                 ".cpp", stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    out, err = proc.communicate()
    if len(err) > 0:
        raise CompilationError(err, "CompilationError")


def createNewGdbAdapter(code, inpt, id):
    code_file_name = createFile(code, ".cpp")
    input_file_name = createFile(inpt, ".txt") + ".txt"
    output_file_name = createFile("", ".txt") + ".txt"
    compileFile(code_file_name)
    return GdbAdapter(code_file_name, input_file_name, output_file_name, id)


def getEdges(g_adapter, var_name):
    depth = 0
    if var_name != "":
        depth = 1
    g = g_adapter.bulidGraph(g_adapter.getGraphData(var_name, str(depth)))
    data = {}
    data["edges"] = g.getGraphEdges()
    data["cnt"] = g.id_cnt
    return data
