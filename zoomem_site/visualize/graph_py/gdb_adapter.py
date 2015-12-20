import re
from graph import gdbGraph
from proc import nbsr_process
import subprocess

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

def getVariablesDef(txt):
    lines = []
    line = ""
    for char in txt:
        line += char
        if char == '\n':
            lines.append(line)
            line = ""
    namespace_std_found = False
    function_start = 0
    function_end = 0
    cur_line = 0
    list_empty = True
    vars_def_list = ""
    for line in lines:
        index = line.find("DeclStmt")
        if index != -1 :
			index = line.find("line")
			left = line.find(":",index)+1
			right = line.find(":",left)-1
			cur_line = int(line[left:right + 1])
        if namespace_std_found == 0:
            if line.find("UsingDirectiveDecl") != -1 and line.find("Namespace") != -1 and line.find("std") != -1:
                namespace_std_found = True
        elif line.find("ParmVarDecl") == -1:
            index = line.find("VarDecl")
            if index != -1:
                Idx = line.find("line:",index)
                if Idx != -1:
                    index = Idx
                else :
                    index = line.find("col:",index)
                index = line.find("col:",index+1)
                index = line.find("col:",index+1)
                left = line.find(" ",index)+1
                right = line.find(" ",left)-1
                if line[right+2]  != '\'':
                    left = line.find(" ",right)+1
                    right = line.find(" ",left)-1
                var_name = line[left:right+1]
                if Idx != -1:
                    function_start = function_end = 0
                    cur_line = int(line[Idx+5:line.find(":",Idx+5)])
                if list_empty == False:
                    vars_def_list += "-"
                list_empty = False
                #print line
                vars_def_list += var_name + " " + str(function_start - 1) + " " + str(function_end - 1) + " " + str(cur_line - 1)

        index = line.find("FunctionDecl")
        if index != -1 :
            left = line.find("line:",index+1)+5
            right = line.find(":",left)-1
            if left == 4 or right == -2:
                continue
            temp_start = int(line[left:right+1])
            left = line.find("line:",right+1)+5
            right = line.find(":",left)-1
            if left == 4 or right == -2:
                continue
            temp_end = int(line[left:right+1])
            function_start = temp_start
            function_end = temp_end
    return vars_def_list

class GdbAdapter:

    def __init__(self,code_file_name,input_file_name,output_file_name):
        self.gdb_process = nbsr_process("gdb " + code_file_name + " -q")
        self.output_file_name = output_file_name

        p = subprocess.Popen(['clang-3.5', '-Xclang' , '-ast-dump' ,'-fsyntax-only',
         code_file_name +"_parsing.cpp"],
         stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out, err = p.communicate()
        self.vars_def_list = getVariablesDef(out)

        defined_functions = getFunctionsNames(code_file_name + ".cpp")
        for function in defined_functions:
            self.gdb_process.write("b " + function)

        self.gdb_process.write("run < " + input_file_name + "> " + output_file_name)
        self.gdb_process.write("target record-full")
        self.gdb_process.clean()

    def next(self,number = 1):
        self.gdb_process.write("n " + str(number))
        self.gdb_process.clean()

    def prev(self,number = 1):
        self.gdb_process.write("rn " + str(number))
        self.gdb_process.clean()

    def readOutput(self):
        content = ""
        with open(self.output_file_name, 'r') as content_file:
            content = content_file.read()
        return content

    def goToLine(self,line):
        self.gdb_process.write("until " + line)
        print (self.gdb_process.clean())


    def getGraphEdegs(self,var_name = ""):
        self.vars_def_list = self.vars_def_list
        var_name = "\"" + var_name + "\""
        self.gdb_process.write("python bulidGraph(\"" +self.vars_def_list+"\","+var_name+ ")")
        return self.gdb_process.readTill("done")

    def getCurrnetLine(self):
        self.gdb_process.write("python getCrrentLine()")
        return int(self.gdb_process.readTill("done")[0])

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
