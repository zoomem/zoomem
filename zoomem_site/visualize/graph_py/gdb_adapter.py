from graph import gdbGraph
from proc import nbsr_process
import code_parser
import os
import time
import commands
import subprocess
import re
import datetime


class ProcRunTimeError(Exception):

    def __init__(self, message, errors):
        super(ProcRunTimeError, self).__init__(message)
        self.errors = errors


class GdbAdapter:

    def __init__(self, code_file_name, input_file_name, output_file_name, id):
        self.code_data_id = id
        self.current_line = 0
        self.output_file_name = output_file_name
        self.current_steps = 0
        self.last_edit = datetime.datetime.utcnow()

        p = subprocess.Popen(['clang-3.5', '-Xclang', '-ast-dump', '-fsyntax-only',
                              code_file_name + "_parsing.cpp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()

        self.vars_def_list = code_parser.getVariablesDef(out)
        defined_functions = code_parser.getFunctionsNames(
            code_file_name + ".cpp")
        self.gdb_process = nbsr_process("gdb " + code_file_name + " -q")
        os.remove(code_file_name + "_parsing.cpp")
        os.remove(code_file_name + ".cpp")

        self.gdb_process.write("python (executeGdbCommand('b main'))")
        self.gdb_process.write("python (executeGdbCommand('set confirm off'))")
        self.gdb_process.write(
            "python (executeGdbCommand('run < " + input_file_name + " > " + output_file_name + "'))")
        for function in defined_functions:
            self.gdb_process.write(
                "python (executeGdbCommand('b " + function + "'))")

        self.gdb_process.write("python setLastLine()")

        self.gdb_process.write(
            "python (executeGdbCommand('target record-full'))")
        self.gdb_process.write("python print('begin')")
        self.gdb_process.readTill("begin")

        self.graph = gdbGraph()

    def lastChanged(self):
        return self.last_edit

    def exitProcess(self):
        self.gdb_process.exitProc()

    def endFunciton(self):
        self.gdb_process.write("python (executeGdbCommand('finish'))")
        self.graph = gdbGraph()
        self.updateGraph()

    def stackUp(self):
        self.gdb_process.write("python (executeGdbCommand('up'))")
        self.graph = gdbGraph()
        self.updateGraph()

    def stackDown(self):
        self.gdb_process.write("python (executeGdbCommand('down'))")
        self.graph = gdbGraph()
        self.updateGraph()

    def getCurrentSteps():
        self.gdb_process.write("python getCurrentSteps()")
        current_steps = int(self.gdb_process.readTill("done")[0])
        self.current_steps = current_steps
        return current_steps

    def next(self, number=1):
        self.gdb_process.write("python next('" + str(number) + "')")
        mess = (self.gdb_process.readTill("done"))
        if len(mess) > 0:
            raise ProcRunTimeError(("\n").join(mess), "RuntimeError")
        self.graph = gdbGraph()
        self.updateGraph()

    def prev(self, number=1):
        self.gdb_process.write("python prev(" + str(number) + ")")
        self.graph = gdbGraph()
        self.updateGraph()

    def goToLine(self, line):
        self.gdb_process.write("python goToLine(" + str(number) + ")")
        mess = (self.gdb_process.readTill("done"))
        if len(mess) > 0:
            raise ProcRunTimeError(("\n").join(mess), "RuntimeError")
        self.graph = gdbGraph()
        self.updateGraph()

    def readOutput(self):
        content = ""
        with open(self.output_file_name, 'r') as content_file:
            content = content_file.read()
        return content

    def getCurrnetLine(self):
        self.gdb_process.write("python getCrrentLine()")
        line = int(self.gdb_process.readTill("done")[0])
        self.current_line = line
        return line

    def getGraphData(self, var_name="", depth=0):
        self.vars_def_list = self.vars_def_list
        var_name = "\"" + var_name + "\""
        self.gdb_process.write("python generateGraphData(\"" +
                               self.vars_def_list + "\"," + var_name + "," + str(depth) + ")")
        return (self.gdb_process.readTill("done"))

    def bulidGraph(self, grahData):
        for data in grahData:
            if data.strip() == "":
                continue
            if(data[0] == '1'):
                attributes = code_parser.parseAttributes(data, 6)
                self.graph.addNode(attributes[1], attributes[2], attributes[
                                   3], attributes[4], attributes[5], attributes[6])
            else:
                attributes = code_parser.parseAttributes(data, 5)
                self.graph.addChildren(attributes[1], attributes[2], attributes[
                                       3], attributes[4], attributes[5])
        return self.graph

    def updateGraph(self):
        self.last_edit = datetime.datetime.utcnow()
        self.graph = self.bulidGraph(self.getGraphData())

    def removeGraphEdges(self, edges):
        for edge in edges:
            if edge.strip() == "":
                continue
            if(edge[0] == '2'):
                attributes = code_parser.parseAttributes(edge, 5)
                self.graph.removeChildren(attributes[1], attributes[2], attributes[
                                          3], attributes[4], attributes[5])
        return self.graph
