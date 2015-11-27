import re

def loadTxt(fileName):
    "Load text file into a string. I let FILE exceptions to pass."
    f = open(fileName)
    txt = ''.join(f.readlines())
    f.close()
    return txt

def getFunctionsNames(fileName):
    rproc = r"((?<=[\s:~])(\w+)\s*\(([\w\s,<>\[\].=&':/*]*?)\)\s*(const)?\s*(?={))"
    code = loadTxt(fileName)
    cppwords = ['if', 'while', 'do', 'for', 'switch']
    return [i[1] for i in re.findall(rproc, code)]
