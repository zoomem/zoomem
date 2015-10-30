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

q = Queue()
def checkVarible(str):
    varName = ""
    for i in str:
        if i == " ":
            break
        varName += i
    writeToGdb("p &"+varName)
    address = gdbOutput("varAddress")
    lastIndex =  address.rfind(" ")
    if lastIndex != -1:
        address = address[lastIndex+1:]
    #print "varible name : " + varName
    #print "varible address : " + address

def checkScope(str):
    temp = ""
    q = Queue()
    for i in str:
        if (i == "\n"):
            checkVarible(temp)
            temp = ""
        else:
            temp += i

def readGdbOutput():
    temp = ""
    while True:
        output = nbsr.readline(0.2)
        if not output:
            break
        temp += output
    return temp

def gdbOutput(query):
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


writeToGdb("run")
gdbOutput("print")
while True:
    command = raw_input()
    writeToGdb(command)
    gdbOutput("print")
    command = "info locals"
    writeToGdb(command)
    gdbOutput("scope")
