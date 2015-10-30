from subprocess import Popen, PIPE
from Queue import Queue, Empty
import hashlib
import non_blocking_stream
import source_parsing

p = Popen('gdb ~/Desktop/py/test',stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = True)
functionsNameList = source_parsing.getFunctionsNames('text.txt')

nbsr = non_blocking_stream.NonBlockingStreamReader(p.stdout)

for name in functionsNameList:
    p.stdin.write('b ' + name + '\n')

varHash = {}
def getVaribleAddress(var_name):
    writeToGdb("p &"+var_name)
    address = praseGdbOutput("varAddress")
    last_index =  address.rfind(" ")
    if last_index != -1:
        address = address[lastIndex+1:]
    return address
def updateVariableleHash(var_name):

    var_address = getVaribleAddress(var_name)
    varHash[var_name] = [] if not exists varHash{var_name};
    varHash[var_name].append(var_address)

def checkScope(gdb_output):

    lastIndex = 0
    info_local_lines = gdb_output.split("\n")
    #print str
    for i in range(0,len(info_local_lines)):
        var_name = info_local_lines[i].split(':').first.strip()
        var_adcheckVarible(var_name)

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
    #print "out : " + temp
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
    p.stdin.write(command + '\n')

varHash = {}
writeToGdb("run")
praseGdbOutput("print")
while True:
    command = raw_input()
    writeToGdb(command)
    praseGdbOutput("print")
    command = "info locals"
    writeToGdb(command)
    praseGdbOutput("scope")
