#include <iostream>
#include <string>
#include <vector>
#include <map>
using namespace std;
map<string,node*>get_node;
class node
{
  public:
    vector<edge*> children;
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
      for(int i = 0 ; i < children[i].size();i++)
        delete children[i];
    }
};

class edge
{
public:
  string name;
  node*to;
  edge(string Name,node* To)
  {
    Name = name;
    to = To;
  }
};

class graph
{

public:
  vector<node*>graph_nodes;

  node* addNode(string address,string type,string name,string value)
  {
    if(get_node.find(address) == get_node.end())
      get_node[address] = new node(address,type,name,value);

    return get_node[adress];
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
