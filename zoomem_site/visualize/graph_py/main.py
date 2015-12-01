
from gdb_adapter import GdbAdapter
ada = GdbAdapter("sample","in.txt")
edges =  ada.getGraphEdegs()
graph = ada.bulidGraph(edges)
graph.printGraph()
