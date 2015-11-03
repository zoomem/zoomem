from subprocess import Popen, PIPE
from Queue import Queue, Empty
import hashlib
import non_blocking_stream
import source_parsing

address_dict = {}
gdb_process = Popen('gdb test -q',stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = True)
gdb_process_nbsr = non_blocking_stream.NonBlockingStreamReader(gdb_process.stdout)

def getVarAddress(var_name):
    writeToProcess(gdb_process,"p &" + var_name)
    var_address = praseGdbOutput()
    return var_address[var_address.rfind(" ") + 1:]

def getVarType(var_name):
    writeToProcess(gdb_process,"ptype "+ var_name)
    var_type = praseGdbOutput()
    return var_type[var_type.rfind("=") + 1:]

def getLocalVariablesName():
    writeToProcess(gdb_process,"info locals")
    var_names = []
    info_local_lines = readProcessOutput(gdb_process_nbsr).split("\n")
    for i in range(0,len(info_local_lines)):
        var_name = info_local_lines[i].split('=')[0].strip()
        var_names.append(var_name)
    return var_names

def is_a_pointer(str):
    return str[str.rfind(" ") + 1:][0] == "*"

def is_a_object(str):
    return False

def is_a_array(str):
    return str[str.rfind(" ") + 1:][0] == "["

def checkScope():
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
        output = nbsr.readline(0.2)
        if not output:
            break
        output_lines += output
    return output_lines.strip()

def writeToProcess(process,command):
    process.stdin.write(command + '\n')

def main():
    for function_name in source_parsing.getFunctionsNames('test.cpp'):
        writeToProcess(gdb_process,('b ' + function_name + '\n'))

    writeToProcess(gdb_process,"run")
    praseGdbOutput()

    while True:
        command = raw_input()
        writeToProcess(gdb_process,command)
        praseGdbOutput("print")
        var_names = getLocalVariablesName()

        for var_name in var_names:
            var_type =  getVarType(var_name)
            print var_type
            print is_a_array(var_type)
            print is_a_pointer(var_type)

main()
