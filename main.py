from subprocess import Popen, PIPE
from Queue import Queue, Empty
import hashlib
import non_blocking_stream
import source_parsing

name_to_address_hash = {}

def getVarAddressByName(var_name):
    writeToGdb("p &"+var_name)
    address = praseGdbOutput("varAddress")
    last_index =  address.rfind(" ")
    if last_index != -1:
        address = address[lastIndex+1:]
    return address

def hashVarNameAdd(var_name):
    var_address = getVarAddressByName(var_name)
    if not name_to_address_hash.has_key(var_name):
        name_to_address_hash[var_name] = []

    name_to_address_hash[var_name].append(var_address)

def checkScope(gdb_output):
    lastIndex = 0
    info_local_lines = gdb_output.split("\n")
    #print str
    for i in range(0,len(info_local_lines)):
        var_name = info_local_lines[i].split(':')[0].strip()
        hashVarNameAdd(var_name)

def readGdbOutput():
    temp = ""
    while True:
        output = nbsr.readline(0.2)
        if not output:
            break
        temp += output
    return temp

def praseGdbOutput(query):
    temp = readGdbOutput()
    if query == "print":
        print temp
        return
    if query == "scope":
        checkScope(temp)
        return
    if query == "varAddress":
        return temp

def writeToGdb(command):
    if(command == "exit"):
        return
    gdp_process.stdin.write(command + '\n')


gdp_process = Popen('gdb test -q',stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = True)
nbsr = non_blocking_stream.NonBlockingStreamReader(gdp_process.stdout)

for function_name in source_parsing.getFunctionsNames('test.cpp'):
    gdp_process.stdin.write('b ' + function_name + '\n')

writeToGdb("run")
praseGdbOutput("print")

while True:
    print readGdbOutput()
    command = raw_input()
    writeToGdb(command)
    praseGdbOutput("print")
    command = "info locals"
    writeToGdb(command)
    praseGdbOutput("scope")
