import hashlib


flags = ["","POINTER_FLAG","ARRAY_FLAG","OBJECT_FLAG","PRIMITIVE_FLAG"]
class node(object):
    def __init__(self, address, type, value, size, flag, id,name):
        self.address = address
        self.type = type
        self.value = value
        self.size = size
        self.flag = flag
        self.children = []
        self.id = id
        self.name = name

    def printNode(self, vs):
        for child_edge in self.children:
            child_node = child_edge.to
            parent_id = self.id
            command = "parent "
            if parent_id == 1:
                command+= "root"
            else:
                command += str(parent_id)
            command += " ,node " + str(child_node.id) + ", var name : " + child_edge.name
            command +=  " ,Adress : "  +  child_node.address +  " ,Type : " + child_node.type
            command +=  " ,Size  : " + child_node.size +  " ,value : "  + child_node.value  + " ,Flag : " + flags[int(child_node.flag)]
            print command
            if(not child_node.id in vs):
                vs[child_node.id] = True
                child_node.printNode(vs);

class Edge:
    def __init__(self, name ,to):
        self.name = name
        self.to = to

class gdbGraph:
    def __init__(self):
        self.root = node("$root", "$root" ,"$root" , "$root" ,"$root",1,"$root")
        self.id_cnt = 2
        self.node_hash = {}
        self.node_hash["$root_$root"] = self.root

    def addNode(self,address, typ, value, size, flag,name):
        ident = address + "_" + typ
        if not ident in self.node_hash:
            self.node_hash[ident] = node(address,typ,value,size,flag,self.id_cnt,name);
            self.id_cnt+= 1
            return self.node_hash[ident];
        elif self.node_hash[ident].name == "DA":
            self.node_hash[ident].name = name

    def addChildren(self,parent_address, parent_type, child_address, child_type, name):
        child = self.node_hash[child_address + "_" + child_type];
        parent = self.node_hash[parent_address + "_" + parent_type];
        parent.children.append(Edge(name,child));

    def printGraph(self):
        self.root.printNode({})
