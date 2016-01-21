from subprocess import Popen, PIPE
import hashlib
import time
import subprocess
import time


class BreakReturn(gdb.Command):

    def __init__(self):
        super(BreakReturn, self).__init__("break-return", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        frame = gdb.selected_frame()
        # TODO make this work if there is no debugging information, where
        # .block() fails.
        block = frame.block()
        # Find the function block in case we are in an inner block.
        while block:
            if block.function:
                break
            block = block.superblock
        start = block.start
        end = block.end
        arch = frame.architecture()
        pc = gdb.selected_frame().pc()
        instructions = arch.disassemble(start, end - 1)
        for instruction in instructions:
            if instruction['asm'].startswith('retq '):
                gdb.Breakpoint('*{}'.format(instruction['addr']))
BreakReturn()

PRIMITIVES_TYPES = ['std::string', 'short', 'short int', 'signed short', 'signed short int', 'unsigned short', 'unsigned short int', 'int', 'signed', 'signed int', 'unsigned', 'unsigned int', 'long', 'long int', 'signed long', 'signed long int', 'unsigned long',
                    'unsigned long int', 'long long', 'long long int', 'signed long long', 'signed long long int', 'unsigned long long', 'unsigned long long int', 'float', 'double', 'long double ', 'signed char', 'unsigned char', 'char', 'wchar_t', 'char16_t', 'char32_t', 'bool']

graph_process = Popen('./graph', stdin=PIPE, stdout=PIPE,
                      stderr=PIPE, shell=True)

POINTER_FLAG = '1'
ARRAY_FLAG = '2'
OBJECT_FLAG = '3'
PRIMITIVE_FLAG = '4'
LAST_LINE = '0'
current_steps = 0
visted_list = {}
vars_def = {}
global_vars = {}
vis_vars = {}

def makeVarVis(ident):
    vis_vars[ident] = "1"

def makeVarNotBis(ident):
    vis_vars[ident] = "0"

def setLastLine():
    command = executeGdbCommand("break-return")
    line = command[command.rfind(" "):command.rfind(".")]
    global LAST_LINE
    LAST_LINE = line.strip()


def getVarAddress(var_name):
    var_address = executeGdbCommand("p &" + var_name)
    index = var_address.rfind("0x")
    last = var_address.find(" ", index + 1)
    if last == -1:
        return var_address[index:]
    else:
        return var_address[index:last]


def getVarType(var_name):
    var_type = executeGdbCommand("ptype " + var_name)
    var_type = var_type[var_type.find("=") + 1:].strip()
    if '{' in var_type:
        return (var_type[0:var_type.find("{") - 1] + var_type[var_type.find("}") + 1:]).strip()
    return var_type


def getVarValue(var_name):
    var_val = executeGdbCommand("print " + var_name)
    start_index = var_val.find("=") + 1
    if isAPointer(getVarType(var_name)):
        temp = var_val.find(")", start_index)
        if temp != -1:
            start_index = temp + 1
    return (var_val[start_index:]).strip()


def getVarSize(var_name):
    var_size = executeGdbCommand("print sizeof(" + var_name + ")")
    return var_size[var_size.find("=") + 1:].strip()


def getNumberOfArrayElements(var_name):
    return int(int(getVarSize(var_name)) / int(getVarSize("(" + var_name + ")[0]")))


def parseInfoLines(info_lines):
    var_names = []
    full_var_value = ""
    rem = 0
    for i in range(0, len(info_lines)):
        if rem == 0:
            equal_index = info_lines[i].find("=")
            var_name = info_lines[i][0:equal_index - 1].strip()
            var_value = info_lines[i][equal_index + 1:].strip()
            var_names.append(var_name)
            full_var_value = getVarValue(var_name)
            rem = len(full_var_value) - len(var_value) - 1
            if full_var_value == var_value:
                rem = 0
            rem = max(rem, 0)
        else:
            rem -= len(info_lines[i])
            if rem > 0:
                rem -= 1
            rem = max(rem, 0)
    return var_names


def getVariablesNames(info_command, info_empty_response):
    info_lines = (executeGdbCommand(info_command)).split("\n")
    if info_lines[0] == info_empty_response:
        return []
    return parseInfoLines(info_lines)



def getCurrentClassMembersNames():
    var_names = []
    try:
        object_varibals = (getVarValue("*this")).split("\n")
        for member in object_varibals:
            member_var = (member[0:member.find("=")]).strip()
            if member_var != "":
                var_names.append(member_var)
    except Exception:
        error = "exception"
    return var_names


def getAllVariablesNames():
    var_names = getVariablesNames("info locals", "No locals.")
    var_names += getCurrentClassMembersNames()
    global global_vars
    for key, value in global_vars.items():
        var_names.append(key)
    definied_vars = getVariablesNames("info args", "No arguments.")
    for var_name in var_names:
        if isDefined(var_name):
            definied_vars.append(var_name)
    return definied_vars


def isAPointer(var_type):
    try:
        index = var_type.rfind("*")
        if index == -1:
            return False
        if index == len(var_type) - 1 or var_type[index + 1] == "[":
            return True
        return False
    except Exception:
        return False


def isAObject(var_type):
    try:
        return var_type[0:var_type.find(" ")].strip() == "class" and not isAPointer(var_type)
    except Exception:
        return False


def isAReference(var_type):
    try:
        index = var_type.rfind("&")
        if index == -1:
            return False
        if index == len(var_type) - 1 or var_type[index + 1] == "[":
            return True
        return False
    except Exception:
        return False


def isAArray(var_type):
    try:
        close_index = var_type.rfind("]")
        if close_index == -1:
            return False
        open_index = var_type.rfind("[")
        return var_type[open_index + 1:close_index].find("with") == -1
    except Exception:
        return False


def isPrimitive(var_type):
    try:
        return var_type[var_type.find("=") + 1:].strip() in PRIMITIVES_TYPES
    except Exception:
        return False


def addVarNameToDic(var_name):
    var_address = getVarAddress(var_name)
    if not address_dict.has_key(var_name):
        address_dict[var_name] = []
    if not var_address in address_dict[var_name]:
        address_dict[var_name].append(var_address)


def executeGdbCommand(command):
    return (gdb.execute(command, True, True)).strip()

line_number = 0


def getLineNumber():
    global line_number
    line_number = executeGdbCommand("frame").split("\n")[1].split()[0]
    return line_number


def getCrrentLine():
    print(getLineNumber())
    print ("done")


def next(n):
    global LAST_LINE
    global current_steps
    n = int(n)
    for i in range(0, n):
        if str(getLineNumber()) != (LAST_LINE):
            s = executeGdbCommand("n")
            current_steps += 1
            if s.find("Program received signal ") >= 0:
                print (s)
                break
        else:
            break
    print("done")
    gdb.flush()


def goToLine(line):
    global LAST_LINE
    global current_steps
    line = int(line)
    while(True):
        if str(getLineNumber()) != LAST_LINE and int(getLineNumber()) != line:
            s = executeGdbCommand("n")
            current_steps += 1
            if s.find("Program received signal ") >= 0:
                print (s)
                break
        else:
            break
    print("done")
    gdb.flush()


def getCurrentSteps():
    global current_steps
    print(current_steps)
    print "done"


def prev(n):
    n = int(n)
    global current_steps
    current_steps = max(current_steps - n, 0)
    for i in range(0, n):
        s = executeGdbCommand("rn")
    gdb.flush()


def initlizeHashes(vars_def_list):
    global vars_def
    global global_vars
    vars_def = {}
    global_vars = {}
    if vars_def_list == "":
        vars_def["$$"] = 1
    if len(vars_def_list) > 0:
        vars_def_list = vars_def_list.split("-")
        for defin in vars_def_list:
            var = defin.split(" ")
            if var[1] == "0":
                global_vars[var[0]] = var[3]
            else:
                if not var[0] in vars_def:
                    vars_def[var[0]] = []
                vars_def[var[0]].append(var[1] + " " + var[2] + " " + var[3])


def generateGraphData(vars_def_list="", var_name="", depth=0):
    start_time = time.time()
    executeGdbCommand("set print pretty on")
    initlizeHashes(vars_def_list)
    getLineNumber()
    if var_name == "":
        var_names = getAllVariablesNames()
        for var_name in var_names:
            analyseVar(var_name, var_name, True)
    else:
        analyseVar(var_name, var_name, False, "", depth)
    global visted_list
    visted_list = {}
    print("done")


def isDefined(var_short_name):
    global vars_def
    if "$$" in vars_def:
        return True
    global line_number
    global global_vars
    line_number = int(line_number)
    if var_short_name in vars_def:
        for defini in vars_def[var_short_name]:
            nums = defini.split(" ")
            function_start = int(nums[0]) - 1
            function_end = int(nums[1]) - 1
            declartion_line = int(nums[2]) - 1
            if function_start < line_number and function_end >= line_number and declartion_line < line_number:
                return True
    if var_short_name in global_vars:
        if int(global_vars[var_short_name]) < line_number:
            return True
    return False


def analyseVar(var_short_name, var_name, root_var=False, Type="", depth=0):
    var_type = getVarType(var_name) if Type == "" else Type
    if check_node(var_name, var_type, var_short_name):
        return
    if isPrimitive(var_type):
        parsePrimitiveVar(var_short_name, var_name, root_var)
    elif isAArray(var_type):
        parseArrayVar(var_short_name, var_name, root_var, depth)
    elif isAPointer(var_type):
        parsePointerVar(var_short_name, var_name, root_var)
    elif isAObject(var_type):
        parseObjectVar(var_short_name, var_name, root_var)
    elif isAReference(var_type):
        parseReferanceVar(var_short_name, var_name, root_var)


def check_node(var_name, var_type, var_short_name):
    var_address = getVarAddress(var_name)
    ident = (var_address + "_" + var_type)
    if ident in visted_list:
        if visted_list[ident] != "$":
            return True
        elif var_short_name != "$":
            visted_list[ident] = var_short_name
            return False
        return True
    else:
        visted_list[ident] = var_short_name
        return False

def getArrayIdent(arr_name):
    return arr_name + "_"  + getVarAddress(var_name) + "_" + getVarType(var_name)

def parseArrayVar(var_short_name, var_name, root_var, depth):
    addVarCommand(var_short_name, var_name, ARRAY_FLAG)
    if root_var:
        addChildCommand("$root", var_name)
    prev_node = var_name
    child_type = getVarType(var_name + "[0]")
    array_ident = getArrayIdent(arr_name)

    if depth > 0 or (array_ident in vis_vars and vis_vars[array_ident] == "1"):
        for i in range(0, getNumberOfArrayElements(var_name)):
            child_var_name = var_name + "[" + str(i) + "]"
            analyseVar(var_short_name + "[" + str(i) + "]",
                       child_var_name, False, child_type, depth - 1)
            addChildCommand(var_name, child_var_name)


def parsePointerVar(var_short_name, var_name, root_var):
    addVarCommand(var_short_name, var_name, POINTER_FLAG)
    if root_var:
        addChildCommand("$root", var_name)
    child_var_name = "(*" + var_name + ")"
    try:
        analyseVar("$", child_var_name)
        addChildCommand(var_name, child_var_name)
    except Exception:
        return


def parseReferanceVar(var_short_name, var_name, root_var):
    addVarCommand(var_short_name, var_name, POINTER_FLAG)
    if root_var:
        addChildCommand("$root", var_name)
    child_var_name = "(*(&" + var_name + "))"
    try:
        analyseVar("$", child_var_name)
        addChildCommand(var_name, child_var_name)
    except Exception:
        return


def parseObjectVar(var_short_name, var_name, root_var):
    addVarCommand(var_short_name, var_name, OBJECT_FLAG)
    if root_var:
        addChildCommand("$root", var_name)
    object_value = getVarValue(var_name)
    next_member_start = object_value.find("{") + 1
    next_member_end = object_value.find("=") - 1
    while True:
        if next_member_start <= 0:
            break
        member_name = object_value[next_member_start:next_member_end].strip()
        member_value_length = len(getVarValue(var_name + "." + member_name))
        analyseVar(member_name, var_name + "." + member_name, False)
        addChildCommand(var_name, var_name + "." + member_name)
        next_member_start = object_value.find(
            ",", member_value_length + next_member_end) + 1
        next_member_end = object_value.find("=", next_member_start) - 1


def parsePrimitiveVar(var_short_name, var_name, root_var):
    addVarCommand(var_short_name, var_name, PRIMITIVE_FLAG)
    if root_var:
        addChildCommand("$root", var_name)


def addVarCommand(var_short_name, var_name, flags):
    var_hash = getVarHash(var_name)
    command = '1,' + var_hash['var_address'] + ',' + var_hash['var_type'] + ',' + str(
        var_hash['var_size']) + ',' + flags + ',' + var_short_name + ',' + var_hash['var_value']
    print(command)


def addChildCommand(parent_var_name, child_var_name):
    parent_var_address = "$root" if parent_var_name == "$root" else getVarAddress(
        parent_var_name)
    parent_var_type = "$root" if parent_var_name == "$root" else getVarType(
        parent_var_name)
    child_var_address = getVarAddress(child_var_name)
    child_var_type = getVarType(child_var_name)
    command = "2," + parent_var_address + "," + parent_var_type + "," + \
        child_var_address + "," + child_var_type + "," + child_var_name
    print(command)


def getVarHash(var_name):
    var_hash = {}
    var_hash['var_type'] = getVarType(var_name)
    var_hash['var_address'] = getVarAddress(var_name)
    var_hash['var_size'] = getVarSize(var_name)
    if isAArray(var_hash['var_type']):
        var_hash['var_value'] = str(getNumberOfArrayElements(var_name))
    else:
        var_value = getVarValue(var_name)
        if var_hash['var_type'] == "char" or var_hash['var_type'] == "signed char" or var_hash['var_type'] == "unsigned char":
            var_hash['var_value'] = var_value[
                var_value.find("\'") + 1:var_value.rfind("\'")]
        else:
            var_hash['var_value'] = (var_value if isPrimitive(
                var_hash['var_type']) else "NULL")
    return var_hash
