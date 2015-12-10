import re
from graph import gdbGraph
from proc import nbsr_process

def loadTxt(file_name):
    "Load text file into a string. I let FILE exceptions to pass."
    f = open(file_name)
    txt = ''.join(f.readlines())
    f.close()
    return txt

def getFunctionsNames(file_name):
    rproc = r"((?<=[\s:~])(\w+)\s*\(([\w\s,<>\[\].=&':/*]*?)\)\s*(const)?\s*(?={))"
    code = loadTxt(file_name)
    cppwords = ['if', 'while', 'do', 'for', 'switch']
    return [i[1] for i in re.findall(rproc, code)]

class GdbAdapter:

    def __init__(self,code_file_name,input_file_name,output_file_name):
        self.gdb_process = nbsr_process("gdb " + code_file_name + " -q")
        self.output_file_name = output_file_name

        defined_functions = getFunctionsNames(code_file_name + ".cpp")
        for function in defined_functions:
            self.gdb_process.write("b " + function)

        self.gdb_process.write("run < " + input_file_name + "> " + output_file_name)
        self.gdb_process.write("target record-full")
        self.gdb_process.clean()

    def next(self):
        self.gdb_process.write("n")
        self.gdb_process.clean()

    def prev(self):
        self.gdb_process.write("reverse-next")
        self.gdb_process.clean()

    def readOutput(self):
        content = ""
        with open(self.output_file_name, 'r') as content_file:
            content = content_file.read()
        return content

    def getGraphEdegs(self,var_name = ""):
        self.gdb_process.write("python bulidGraph(" + var_name + ")")
        return self.gdb_process.readTill("done")

    def bulidGraph(self, edges):
        g = gdbGraph()
        for edge in edges:
            attributes = edge.split(',')
            if attributes[0] == '1':
                g.addNode(attributes[1],attributes[2],attributes[3],attributes[4],attributes[5],attributes[6])
            else:
                g.addChildren(attributes[1],attributes[2],attributes[3],attributes[4],attributes[5])
        return g

    def send_command(command):
        self.gdb_process.write(command + "\n")
        return self.gdb_process.read()
