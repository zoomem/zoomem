from subprocess import Popen, PIPE
import non_blocking_stream
import time
import subprocess
import source_code_parsing

gdb_process = Popen('gdb sample -q',stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = True)
gdb_process_nbsr = non_blocking_stream.NonBlockingStreamReader(gdb_process.stdout)

graph_process = Popen('./graph',stdin = PIPE, stdout = PIPE, stderr = PIPE,shell = True)
graph_process_nbsr = non_blocking_stream.NonBlockingStreamReader(graph_process.stdout)

def readProcess(process):
    output_lines = ""
    while True:
        output = process.stdout.readline().strip()
        if output == "done":
            break
        print output

def readProcessOutput(nbsr,timeout = 0.2):
    output_lines = ""
    while True:
        output = nbsr.readline(timeout)
        if output == None:
            break
        output_lines += output
    return output_lines.strip()

def readProcessOutputTill(nbsr,end = ""):
    output_lines = []
    while True:
        output = nbsr.readline(0)
        if output == None:
            break
        output = output.strip()
        if output == end:
            break
        output_lines.append(output)
    return output_lines

def writeToProcess(process,command):
    command+="\n"
    process.stdin.write(command.encode())

def main():
    for function_name in source_code_parsing.getFunctionsNames('sample.cpp'):
        writeToProcess(gdb_process,('b ' + function_name + '\n'))

    writeToProcess(gdb_process,"run")
    while True:
        writeToProcess(gdb_process,"n")
        x = readProcessOutput(gdb_process_nbsr)
        if "return 0;" in x:
            break

    writeToProcess(gdb_process,"python bulidGraph()")
    time.sleep(1)
    commands = readProcessOutputTill(gdb_process_nbsr,"done")
    for command in commands:
        writeToProcess(graph_process,command)

    writeToProcess(graph_process,"end")
    time.sleep(1)
    graph_list = readProcessOutputTill(graph_process_nbsr,"done")
    print "\n".join(graph_list)

main()
