from subprocess import Popen, PIPE
import hashlib
import time
import subprocess

PRIMITIVES_TYPES = ['short', 'short int', 'signed short', 'signed short int', 'unsigned short', 'unsigned short int', 'int', 'signed', 'signed int', 'unsigned', 'unsigned int', 'long', 'long int', 'signed long', 'signed long int', 'unsigned long', 'unsigned long int', 'long long', 'long long int', 'signed long long', 'signed long long int', 'unsigned long long', 'unsigned long long int', 'float', 'double', 'long double ', 'signed char', 'unsigned char', 'char', 'wchar_t', 'char16_t', 'char32_t', 'bool']

graph_process = Popen('./graph',stdin = PIPE, stdout = PIPE, stderr = PIPE,shell = True)

POINTER_FLAG = '1'
ARRAY_FLAG = '2'
OBJECT_FLAG = '3'
PRIMITIVE_FLAG = '4'

def getVarAddress(var_name):
    var_address = executeGdbCommand("p &" + var_name)
    return var_address[var_address.rfind(" ") + 1:].strip()

def getVarType(var_name):
    var_type = executeGdbCommand("ptype " + var_name)
    var_type = var_type[var_type.rfind("=") + 1:].strip()
    if '{' in var_type:
        return (var_type[0:var_type.find("{")-1]+var_type[var_type.find("}")+1:]).strip()
    return var_type

def getVarValue(var_name):
    var_val = executeGdbCommand("print " + var_name)
    return (var_val[var_val.find("=") + 1:])

def getVarSize(var_name):
    var_size =  executeGdbCommand("print sizeof(" + var_name + ")")
    return var_size[var_size.rfind("=") + 1:].strip()

def getNumberOfArrayElements(var_name):
    return int(int(getVarSize(var_name)) / int(getVarSize("(" + var_name + ")[0]")))

def getLocalVariablesName():
    var_names = []
    info_local_lines = (executeGdbCommand("info locals")).split("\n")
    full_var_value = ""
    rem = 0
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
    if not address_dict.has_key(var_name):address_dict[var_name] = []
    if not var_address in address_dict[var_name]:address_dict[var_name].append(var_address)

def executeGdbCommand(command):
    return (gdb.execute(command,True,True)).strip()

def getCrrentLine():
    line = executeGdbCommand("frame").split("\n")[1].split()[0]
    print(line)
    print ("done")

def bulidGraph(var_name = ""):
    start_time = time.time();
    executeGdbCommand("set print pretty on")
    if var_name == "":
        var_names = getLocalVariablesName()
        for var_name in var_names:
            analyseVar(var_name,var_name,True)
    else:
        analyseVar(var_name,var_name,True,"",True)
    print("done")

def analyseVar(var_short_name,var_name,root_var = False,Type = "",depth = False):
    var_type = getVarType(var_name) if Type == "" else Type
    if isPrimitive(var_type):
        parsePrimitiveVar(var_short_name,var_name,root_var)
    elif isAArray(var_type):
        parseArrayVar(var_short_name,var_name,root_var,depth)
    elif isAPointer(var_type):
        parsePointerVar(var_short_name,var_name,root_var)
    elif isAObject(var_type):
        parseObjectVar(var_short_name,var_name,root_var)

def parseArrayVar(var_short_name,var_name,root_var,depth):
    addVarCommand(var_short_name,var_name,ARRAY_FLAG)
    if root_var: addChildCommand("$root",var_name)
    prev_node = var_name
    child_type = getVarType(var_name + "[0]")
    if depth == True:
        for i in range(0,getNumberOfArrayElements(var_name)):
            child_var_name = var_name+ "[" + str(i) + "]"
            analyseVar(var_short_name+"[" + str(i) + "]",child_var_name,False,child_type,depth)
            addChildCommand(var_name,child_var_name)

def parsePointerVar(var_short_name,var_name,root_var):
    addVarCommand(var_short_name,var_name,POINTER_FLAG)
    if root_var : addChildCommand("$root",var_name)
    child_var_name = "(*" + var_name+ ")"
    try:
        analyseVar("DA",child_var_name)
        addChildCommand(var_name,child_var_name)
    except Exception:
        return

def parseObjectVar(var_short_name,var_name,root_var):
    addVarCommand(var_short_name,var_name,OBJECT_FLAG)
    if root_var : addChildCommand("$root",var_name)
    object_varibals = (getVarValue(var_name)).split("\n")
    for member in object_varibals:
        member_var = (member[0:member.find("=")]).strip()
        if member_var!= "":
            analyseVar(member_var,var_name + "." + member_var,False)
            addChildCommand(var_name,var_name + "." + member_var)

def parsePrimitiveVar(var_short_name,var_name,root_var):
    addVarCommand(var_short_name,var_name,PRIMITIVE_FLAG)
    if root_var : addChildCommand("$root",var_name)

def addVarCommand(var_short_name,var_name,flags):
    var_hash = getVarHash(var_name)
    command = '1,' + var_hash['var_address'] + ',' + var_hash['var_type'] + ',' + var_hash['var_value'] + ',' + str(var_hash['var_size']) +',' + flags + ',' + var_short_name
    print(command)

def addChildCommand(parent_var_name, child_var_name):
    parent_var_address = "$root" if parent_var_name == "$root" else getVarAddress(parent_var_name)
    parent_var_type = "$root" if parent_var_name == "$root" else getVarType(parent_var_name)
    child_var_address = getVarAddress(child_var_name)
    child_var_type = getVarType(child_var_name)
    command = "2," + parent_var_address + "," + parent_var_type + "," + child_var_address + "," + child_var_type + "," + child_var_name
    print(command)

def getVarHash(var_name):
    var_hash = {}
    var_hash['var_type'] = getVarType(var_name)
    var_hash['var_address'] = getVarAddress(var_name)
    var_hash['var_size'] = getVarSize(var_name)
    if isAArray(var_hash['var_type']):
        var_hash['var_value'] = str(getNumberOfArrayElements(var_name))
    else:
        var_hash['var_value'] = (getVarValue(var_name) if isPrimitive(var_hash['var_type']) else  "none")
    return var_hash

def compileFiles():
    subprocess.Popen("g++ -g -o test test.cpp", shell = True)
    subprocess.Popen("g++ -o graph graph.cpp",shell = True)
