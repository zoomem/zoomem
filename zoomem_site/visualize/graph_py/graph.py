import hashlib
from sets import Set
edges_list = []
flags = ["", "POINTER_FLAG", "ARRAY_FLAG", "OBJECT_FLAG", "PRIMITIVE_FLAG"]


class node(object):

    def __init__(self, address, type, value, size, flag, id, name):
        self.address = address
        self.type = type
        self.value = value
        self.size = size
        self.flag = flag
        self.children = []
        self.parents = Set()
        self.id = id
        self.name = name

    def calcGraphEdges(self, vs, edges, vs2):
        for child_edge in self.children:
            child_node = child_edge.to
            command = []
            command.append(str(self.id))
            command.append(str(child_node.id))
            command.append(child_node.name)
            command.append(child_node.address)
            command.append(child_node.type)
            command.append(child_node.size)
            command.append(str(child_node.value))
            command.append(int(child_node.flag))
            if child_node.flag == "2":
                command.append(child_edge.name)
            else:
                command.append("")
            temp = str(self.id) + "_" + str(child_node.id)
            if(not temp in vs2):
                edges.append(command)
                vs2[temp] = True
            if not child_node.id in vs:
                vs[child_node.id] = True
                child_node.calcGraphEdges(vs, edges, vs2)

    def printNode(self, vs):
        for child_edge in self.children:
            child_node = child_edge.to
            parent_id = self.id
            command = "parent "
            if parent_id == 1:
                command += "root"
            else:
                command += str(parent_id)
            command += " ,node " + \
                str(child_node.id) + ", var name : " + child_edge.name
            command += " ,Adress : " + child_node.address + " ,Type : " + child_node.type
            command += " ,Size  : " + child_node.size + " ,value : " + \
                child_node.value + " ,Flag : " + flags[int(child_node.flag)]
            print command
            if(not child_node.id in vs):
                vs[child_node.id] = True
                child_node.printNode(vs)

    def __eq__(self, other):
        return (other.getIdenty() == self.getIdenty())

    def getIdenty(self):
        return self.type + "_" + self.address


class Edge:

    def __init__(self, name, to):
        self.name = name
        self.to = to

    def __eq__(self, other):
        return (other.to == self.to)


class gdbGraph:

    def __init__(self):
        self.root = node("$root", "$root", "$root",
                         "$root", "$root", 1, "$root")
        self.id_cnt = 1
        self.node_hash = {}
        self.node_hash["$root_$root"] = self.root

    def addNode(self, address, typ, size, flag, name, value):
        ident = address + "_" + typ
        if not ident in self.node_hash:
            self.id_cnt += 1
            self.node_hash[ident] = node(
                address, typ, value, size, flag, self.id_cnt, name)
            return self.node_hash[ident]

        elif self.node_hash[ident].name == "$":
            self.node_hash[ident].name = name

    def addChildren(self, parent_address, parent_type, child_address, child_type, name):
        try:
            child = self.node_hash[child_address + "_" + child_type]
            parent = self.node_hash[parent_address + "_" + parent_type]
            if not Edge(name, child) in parent.children:
                parent.children.append(Edge(name, child))
            child.parents.add(parent.getIdenty())

        except Exception:
            print "erorrrrrrrr", name

    def removeChildren(self, parent_address, parent_type, child_address, child_type, name):
        try:
            child = self.node_hash[child_address + "_" + child_type]
            parent = self.node_hash[parent_address + "_" + parent_type]
            child.parents.discard(parent.getIdenty())
            parent.children = filter(
                lambda ed: ed.to.getIdenty() != child.getIdenty(), parent.children)
            if len(child.parents) == 0 and child.getIdenty() in self.node_hash:
                del self.node_hash[child.getIdenty()]

        except Exception:
            print "erorrrrrrrr", name

    def getGraphEdges(self):
        edges = []
        self.root.calcGraphEdges({}, edges, {})
        return edges
