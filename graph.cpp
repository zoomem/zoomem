#include <iostream>
#include <string>
#include <vector>
#include <map>
using namespace std;

class node;
class edge;
map<string,node*>get_node;

class edge
{
public:
  string name;
  node* to;
  edge(string Name,node* To)
  {
    Name = name;
    to = To;
  }
};

class node
{
  public:
    vector<edge> children;
    string address;
    string type;
    string value;
    int flags;
    node(string Address,string Type,string Value,int Flags)
    {
      address = Address;
      type = Type;
      value = Value;
      flags = Flags;
    }
    ~node() {
      for(int i = 0 ; i < children.size();i++)
        delete children[i].to;
    }
};


class graph
{

public:
  vector<node*>graph_nodes;

  node* addNode(string address,string type,string value)
  {
    if(get_node.find(address) == get_node.end())
      get_node[address] = new node(address,type,value,0);

    return get_node[address];
  }

  void addChildren(node* parent,node *child,string name)
  {
    parent->children.push_back(edge(name,child));
  }

  ~graph()
  {
    for(int i = 0 ; i < graph_nodes.size();i++)
    {
      delete graph_nodes[i];
    }
  }

};

int main()
{
  return 0;
}
