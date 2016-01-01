import re
from graph import gdbGraph
from proc import nbsr_process
import subprocess
import commands
import time
import code_parser

class GdbAdapter:

    def __init__(self,code_file_name,input_file_name,output_file_name):
        self.gdb_process = nbsr_process("gdb " + code_file_name + " -q")
        self.output_file_name = output_file_name

        p = subprocess.Popen(['clang-3.5', '-Xclang' , '-ast-dump' ,'-fsyntax-only',code_file_name +"_parsing.cpp"], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out, err = p.communicate()
        self.vars_def_list = code_parser.getVariablesDef(out)

        defined_functions = code_parser.getFunctionsNames(code_file_name + ".cpp")
        for function in defined_functions:
            self.gdb_process.write("python (executeGdbCommand('b " + function + "'))")

        self.gdb_process.write("python (executeGdbCommand('set confirm off'))")
        self.gdb_process.write("python (executeGdbCommand('run < " + input_file_name + " > " + output_file_name + "'))")
        self.gdb_process.write("python setLastLine()")

        self.gdb_process.write("python (executeGdbCommand('target record-full'))")
        self.gdb_process.write("python print('begin')")
        self.gdb_process.clean()

        self.graph = gdbGraph()

    def endFunciton(self):
        self.gdb_process.write("python (executeGdbCommand('finish'))")
        self.graph = gdbGraph()

    def stackUp(self):
        self.gdb_process.write("python (executeGdbCommand('up'))")
        self.graph = gdbGraph()

    def stackDown(self):
        self.gdb_process.write("python (executeGdbCommand('down'))")
        self.graph = gdbGraph()

    def next(self,number = 1):
        self.gdb_process.write("python next('"+ str(number) + "')")
        self.graph = gdbGraph()

    def prev(self,number = 1):
        self.gdb_process.write("python executeGdbCommand('rn " + str(number) + "')")
        self.graph = gdbGraph()

    def readOutput(self):
        content = ""
        with open(self.output_file_name, 'r') as content_file:
            content = content_file.read()
        return content

    def getGraphData(self,var_name = "",depth = 0):
        self.vars_def_list = self.vars_def_list
        var_name = "\"" + var_name + "\""
        self.gdb_process.write("python generateGraphData(\"" +self.vars_def_list+"\","+var_name+ "," + depth + ")")
        return (self.gdb_process.readTill("done"))

    def getCurrnetLine(self):
        self.gdb_process.write("python getCrrentLine()")
        return int(self.gdb_process.readTill("done")[0])

    def bulidGraph(self, edges):
        for edge in edges:
            if edge.strip() == "":
                continue
            if(edge[0] == '1'):
                attributes = code_parser.parseAttributes(edge,6)
                self.graph.addNode(attributes[1],attributes[2],attributes[3],attributes[4],attributes[5],attributes[6])
            else:
                attributes = code_parser.parseAttributes(edge,5)
                self.graph.addChildren(attributes[1],attributes[2],attributes[3],attributes[4],attributes[5])
        return self.graph

    def removeGraphEdges(self,edges):
        for edge in edges:
            if edge.strip() == "":
                continue
            if(edge[0] == '2'):
                attributes = code_parser.parseAttributes(edge,5)
                self.graph.removeChildren(attributes[1],attributes[2],attributes[3],attributes[4],attributes[5])
        return self.graph
