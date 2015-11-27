from subprocess import Popen, PIPE
import non_blocking_stream
import time
import subprocess
import source_code_parsing
import graph

gdb_process = Popen('gdb sample -q',stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = True)
gdb_process_nbsr = non_blocking_stream.NonBlockingStreamReader(gdb_process.stdout)

def readProcess(process):
    output_lines = ""
    while True:
        output = process.stdout.readline().strip()
        if output == "done":
            break
        print output

def readProcessOutput(nbsr,timeout = 0.5):
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
        output = nbsr.readline()
        if output == None:
            time.sleep(0.1)
            continue;

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
    current_line = ""

    while True:
        task = raw_input()
        if task == "run":
            start_time = time.time()
            readProcessOutput(gdb_process_nbsr)
            writeToProcess(gdb_process,"python bulidGraph()")
            commands = readProcessOutputTill(gdb_process_nbsr,"done")
            print "\n".join(commands)
            g = graph.gdbGraph()
            for command in commands:
                attributes = command.split(',')
                if attributes[0] == '1':
                    g.addNode(attributes[1],attributes[2],attributes[3],attributes[4],attributes[5])
                else:
                    g.addChildren(attributes[1],attributes[2],attributes[3],attributes[4],attributes[5])
            g.printGraph()

            print "end of program", time.time() - start_time
            if "return 0;" in current_line:
                return
        elif task == "end":
            return
        writeToProcess(gdb_process,"n")
        current_line = readProcessOutput(gdb_process_nbsr)


main()
