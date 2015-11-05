from subprocess import Popen, PIPE
from Queue import Queue, Empty
import hashlib
import non_blocking_stream
import source_parsing
import time
import string
import random

address_dict = {}

PRIMITIVES_TYPES = ['short', 'short int', 'signed short', 'signed short int', 'unsigned short', 'unsigned short int', 'int', 'signed', 'signed int', 'unsigned', 'unsigned int', 'long', 'long int', 'signed long', 'signed long int', 'unsigned long', 'unsigned long int', 'long long', 'long long int', 'signed long long', 'signed long long int', 'unsigned long long', 'unsigned long long int', 'float', 'double', 'long double ', 'signed char', 'unsigned char', 'char', 'wchar_t', 'char16_t', 'char32_t', 'bool']

gdb_process = Popen('gdb test -q',stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = True)
gdb_process_nbsr = non_blocking_stream.NonBlockingStreamReader(gdb_process.stdout)

graph_process = Popen('./graph',stdin = PIPE, stdout = PIPE, stderr = PIPE,shell = True)
graph_process_nbsr = non_blocking_stream.NonBlockingStreamReader(graph_process.stdout)

POINTER_FLAG = '1'
ARRAY_FLAG = '2'
OBJECT_FLAG = '3'
PRIMITIVE_FLAG = '4'

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

def getVarValue(var_name):

    writeToProcess(gdb_process,"print "+ var_name)
    var_val = praseGdbOutput()
    return var_val[var_val.find("=") + 1:]

def getVarSize(var_name):
    writeToProcess(gdb_process ,"print sizeof(" + var_name + ")")
    var_size = praseGdbOutput()
    var_size = var_size[var_size.rfind("=") + 1:].strip()

def getLocalVariablesName():
    writeToProcess(gdb_process,"info locals")
    var_names = []
    info_local_lines = readProcessOutput(gdb_process_nbsr).split("\n")
    full_var_value = ""
    rem = 0
    print "new line"
    for i in range(0,len(info_local_lines)):
        if rem == 0:
            equal_index = info_local_lines[i].find("=")
            var_name = info_local_lines[i][0:equal_index-1].strip()
            var_value = info_local_lines[i][equal_index+1:]

            var_names.append(var_name)
            full_var_value = getVarValue(var_name)

            if isAPointer(getVarType(var_name)):
                full_var_value = full_var_value[full_var_value.find(")")+1:]
            rem = len(full_var_value) - len(var_value) - 1
            if full_var_value == var_value:
                rem = 0
        else:
            rem -= len(info_local_lines[i])
            if rem > 0:
                rem -= 1
    return var_names

def isAPointer(var_type):
    try:
        return var_type[var_type.rfind(" ") + 1:][0] == "*"
    except Exception:
        return False

def isAObject(var_type):
    try:
        return var_type[0:var_type.find(" ")].strip() == "class" and not isAPointer(var_type)
    except Exception:
        return False

def isAArray(var_type):
    try:
        return var_type[var_type.rfind(" ") + 1:][0] == "["
    except Exception:
        return False

def isPrimitive(var_type):
    try:
        return var_type[var_type.find("=") + 1:].strip() in PRIMITIVES_TYPES
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
    elif isPrimitive(var_type):
        parsePrimitiveVar(var_name)
    else:
        print var_name , var_type
        raise Exception

def parseArrayVar(var_name):
    print var_name + " array"

def parsePointerVar(var_name):
    print var_name + " pointer"
    addVarCommand(var_name,POINTER_FLAG)

    child_var_name = genrateTempVarName("*" + var_name)
    analyzeVar(child_var_name)
    addChildCommand(var_name,child_var_name)

def parseObjectVar(var_name):
    print var_name + " object"

def parsePrimitiveVar(var_name):
    print var_name + " premitave"
    addVarCommand(var_name,PRIMITIVE_FLAG)

def genrateTempVarName(parent_var):
    temp_var_name = "$a" + str(int(random.random() * 10000))
    writeToProcess(gdb_process,("set " + temp_var_name + " = " + parent_var))
    return temp_var_name

def addVarCommand(var_name,flags):
    var_hash = getVarHash(var_name)
    writeToProcess(graph_process,('1,' + var_hash['var_address'] + ',' + var_hash['var_type'] + ',' + var_hash['var_value'] + ',' + flags))

    print "graph out : " + readProcessOutput(graph_process_nbsr)

def addChildCommand(parent_var_name, child_var_name):
    parent_var_address = getVarAddress(parent_var_name)
    child_var_address = getVarAddress(child_var_name)
    print parent_var_name,child_var_name
    writeToProcess(graph_process,"2," + parent_var_address + "," + child_var_address)
    print "graph out : " + readProcessOutput(graph_process_nbsr)

def getVarHash(var_name):
    var_hash = {}
    var_hash['var_type'] = getVarType(var_name)
    var_hash['var_address'] = getVarAddress(var_name)
    var_hash['var_size'] = getVarSize(var_name)
    if isPrimitive(getVarType(var_name)):
        var_hash['var_value'] = getVarValue(var_name)
    else:
         var_hash['var_value'] = ""
    return var_hash

def main():
    print "kos kos"
    for function_name in source_parsing.getFunctionsNames('test.cpp'):
        writeToProcess(gdb_process,('b ' + function_name + '\n'))
        print function_name
    writeToProcess(gdb_process,"run")
    while True:
        writeToProcess(gdb_process,"n")
        x = readProcessOutput(gdb_process_nbsr)
        print x
        if "return 0;" in x:
            break

    time.sleep(0.3)
    praseGdbOutput()

    bulidGraph()

main()
