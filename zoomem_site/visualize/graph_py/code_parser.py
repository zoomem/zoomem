import commands

def loadTxt(file_name):
    "Load text file into a string. I let FILE exceptions to pass."
    f = open(file_name)
    txt = ''.join(f.readlines())
    f.close()
    return txt

def getStr(Str,idx):
    res = ""
    cnt = 0
    goig = False
    for char in Str:
        if char == ' ':
            if not going:
                if cnt == idx:
                    return res
                cnt = cnt + 1
                going = True
                res = ""
        else:
            res+=char
            going = False
    return res

def parseAttributes(command,cnt):
    lst = []
    idx = 0
    temp = ""
    for i in range(0,len(command)):
        if command[i] == ',':
            if len(temp) > 0:
                lst.append(temp)
            temp = ""
            idx+=1
            if(idx == cnt):
                temp = command[i+1:]
                if(len(temp) > 0):
                    lst.append(temp)
                return lst
        else:
            temp+=command[i]
    if(len(temp) > 0):
        lst.append(temp)
    return lst

def getFunctionsNames(file_name):
    lst = (commands.getstatusoutput('ctags --c++-kinds=f -x ' + file_name))
    lst = lst[1]
    lst =  lst.split("\n")
    functions = []
    for out in lst:
        functions.append(getStr(out,2))
    return functions

def isDummyDeclartionLine(line):
    index = line.find("VarDecl")
    if index == -1:
        return False
    index = line.find("dummyVaribleDeclaredToBeUsedToParseClangOutput__4zoomem",index + 1)
    if index == -1:
        return False
    return True

def isVariableDeclartionStatment(line):
    index = line.find("DeclStmt")
    if index == -1:
        return False
    return True

def getVariableDeclartionLine(line):
    index = line.find("line")
    left = line.find(":",index)+1
    right = line.find(":",left)-1
    return line[left:right + 1]

def isFunctionDefinision(line):
    if line.find("FunctionDecl") != -1:
        return True
    if line.find("CXXMethodDecl") != -1:
        return True
    if line.find("CXXConstructorDecl") != -1:
        return True
    if line.find("CXXDestructorDecl") != -1:
        return True
    return False

def getFunctionBounds(line):
    # returns empty string if the line dosen't declare compound statment
    if isFunctionDefinision(line) == False:
        return ""
    left = line.find("line:")+5
    right = line.find(":",left)-1
    if left == 4 or right == -2:
        return ""
    function_start = line[left:right+1]
    left = line.find("line:",right+1)+5
    right = line.find(":",left)-1
    if left == 4 or right == -2:
        return ""
    function_end = line[left:right+1]
    return function_start + " " + function_end

def getVariableLine(line):
    # returns empty string if the line dosen't declare local variable
    index = line.find("VarDecl")
    if index == -1 or line.find("ParmVarDecl") != -1:
        return ""
    cur_line = ""
    is_global = line.find("line:",index)
    if is_global != -1:
        index = is_global
    else:
        index = line.find("col:",index)
    index = line.find("col:",index+1)
    index = line.find("col:",index+1)
    left = line.find(" ",index)+1
    right = line.find(" ",left)-1
    if line[right+2] != '\'':
        left = line.find(" ",right)+1
        right = line.find(" ",left)-1
    var_name = line[left:right+1]
    cur_line = "-1"
    if is_global != -1:
        cur_line = line[is_global+5:line.find(":",is_global+5)]
    return var_name + " " + cur_line

def reformat(txt):
    lines = []
    line = ""
    for char in txt:
        line += char
        if char == '\n':
            lines.append(line)
            line = ""
    return lines

def getClassBounds(line):
    # returns empty string if the line dosen't declare class
    if line.find("CXXRecordDecl") == -1 or line.find("class") == -1 or line.find("definition") == -1:
        return ""
    left = line.find(":")
    right = line.find(":",left+1)
    class_start = line[left+1:right]
    left = line.find(":",right+1)
    right = line.find(":",left+1)
    class_end = line[left+1:right]
    return class_start + " " + class_end

def getClassMemberName(line):
    # returns empty string if the line dosen't declare a member in class
    index = line.find("FieldDecl")
    if index == -1:
        return ""
    index = line.find("line:",index)
    if index == -1:
        index = line.find("col:")
    index = line.find("col:",index+1)
    index = line.find("col:",index+1)
    left = line.find(" ",index)+1
    right = line.find(" ",left)-1
    if line[right+2] != '\'':
        left = line.find(" ",right)+1
        right = line.find(" ",left)-1
    var_name = line[left:right+1]
    return var_name

def getVariablesDef(txt):
    lines = reformat(txt)
    dummy_var_found = False
    function_start = function_end = cur_line = ""
    class_start = class_end = ""
    list_empty = True
    vars_def_list = ""
    for line in lines:
        if dummy_var_found == False:
            dummy_var_found = isDummyDeclartionLine(line)
            if dummy_var_found == True:
                continue
        elif dummy_var_found == True and isVariableDeclartionStatment(line):
            cur_line = getVariableDeclartionLine(line)

        # still inside library ...
        if dummy_var_found == False:
            continue

        var_info = getVariableLine(line)
        if var_info != "":
            index = var_info.find(" ")
            var_name = var_info[0:index]
            dec_line = var_info[index+1:]
            if list_empty == False:
                vars_def_list += '-'
            if dec_line != "-1":
                vars_def_list += var_name +" 0 0 " + dec_line
            else:
                vars_def_list += var_name +" " + function_start+ " " + function_end + " " + cur_line
            list_empty = False

        #member_name = getClassMemberName(line)
        #if member_name != "":
        #    if list_empty == False:
    #            vars_def_list += '-'
    #        list_empty = False
    #        vars_def_list += member_name + " " + class_start + " " + class_end + " " + class_start

        bounds = getFunctionBounds(line)
        if bounds != "":
            index = bounds.find(" ")
            function_start = bounds[:index]
            function_end = bounds[index+1:]

    #    bounds = getClassBounds(line)
    #    if bounds != "":
    #        index = bounds.find(" ")
    #        class_start = bounds[:index]
    #        class_end = bounds[index+1:]
    print(vars_def_list)
    return vars_def_list
