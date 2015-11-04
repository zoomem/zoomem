from subprocess import Popen, PIPE
from Queue import Queue, Empty
import hashlib
import non_blocking_stream
import source_parsing

address_dict = {}

gdb_process = Popen('gdb test -q',stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = True)
gdb_process_nbsr = non_blocking_stream.NonBlockingStreamReader(gdb_process.stdout)

graph_process = Popen('graph',stdin = PIPE, stdout = PIPE, stderr = PIPE,shell = True)
graph_process_nbsr = non_blocking_stream.NonBlockingStreamReader(graph_process.stdout)

def getVarAddress(var_name):
    writeToProcess(gdb_process,"p &" + var_name)
    var_address = praseGdbOutput()
    return var_address[var_address.rfind(" ") + 1:].strip()

def getVarType(var_name):
    writeToProcess(gdb_process,"ptype "+ var_name)
    var_type = praseGdbOutput()
    var_type = var_type[var_type.rfind("=") + 1:].strip()
    if isAObject(var_type):
        return var_type[0:var_type.find("{")-1].strip()
    return var_type

def getVarSize(var_name):
    writeToProcess(gdb_process ,"print sizeof(" + var_name + ")")
    var_size = praseGdbOutput()
    return var_size[var_size.rfind("=") + 1:].strip()

def getLocalVariablesName():
    writeToProcess(gdb_process,"info locals")
    var_names = []
    info_local_lines = readProcessOutput(gdb_process_nbsr).split("\n")
    for i in range(0,len(info_local_lines)):
        var_name = info_local_lines[i].split('=')[0].strip()
        var_names.append(var_name)
    return var_names

def isAPointer(var_name):
    try:
        return var_name[var_name.rfind(" ") + 1:][0] == "*"
    except Exception:
        return False

def isAObject(var_name):
    try:
        return var_name[0:var_name.find(" ")] == "class" and not isAPointer(var_name)
    except Exception:
        return False

def isAArray(var_name):
    try:
        return var_name[var_name.rfind(" ") + 1:][0] == "["
    except Exception:
        return False

def updateScope():
    var_names = getLocalVariablesName()
    for var_name in var_names:
        addVarNameToDic(var_name)

def addVarNameToDic(var_name):
    var_address = getVarAddress(var_name)
    if not address_dict.has_key(var_name):
        address_dict[var_name] = []
    if not var_address in address_dict[var_name]:
        address_dict[var_name].append(var_address)

def praseGdbOutput(query = ""):
    output = readProcessOutput(gdb_process_nbsr)
    if query == "print":
        print output
    else:
        return output

def readProcessOutput(nbsr):
    output_lines = ""
    while True:
        output = nbsr.readline(0.1)
        if not output:
            break
        output_lines += output
    return output_lines.strip()

def writeToProcess(process,command):
    process.stdin.write(command + '\n')

def bulidGraph():
    var_names = getLocalVariablesName()
    for var_name in var_names:
        analyzeVar(var_name)

def analyzeVar(var_name):
    var_type = getVarType(var_name)

    if isAArray(var_type):
        parseArrayVar(var_name)
    elif isAPointer(var_type):
        parsePointerVar(var_name)
    elif isAObject(var_type):
        parseObjectVar(var_name)
    else:
        parsePrimitiveVar(var_name)

    print getVarHash(var_name)

def parseArrayVar(var_name):
    print var_name + " array"

def parsePointerVar(var_name):
    print var_name + " pointer"

def parseObjectVar(var_name):
    print var_name + " object"

def parsePrimitiveVar(var_name):
    print  var_name + " prem"

def getVarHash(var_name):
    var_hash = {}
    var_hash['var_type'] = getVarType(var_name)
    var_hash['var_address'] = getVarAddress(var_name)
    var_hash['var_size'] = getVarSize(var_name)
    return var_hash

def main():

    for function_name in source_parsing.getFunctionsNames('test.cpp'):
        writeToProcess(gdb_process,('b ' + function_name + '\n'))

    writeToProcess(gdb_process,"run")
    praseGdbOutput()

    bulidGraph()

main()
