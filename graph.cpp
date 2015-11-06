#include <iostream>
#include <string>
#include <vector>
#include <map>
using namespace std;

class node;
class edge;
map<string,node*>get_node;

vector<string> split(string s,char c)
{
  string temp = "";
  vector<string>v;
  for(int i = 0 ; i < s.size();i++)
  {
    if(s[i] == c)
    {
      v.push_back(temp);
      temp = "";
    }
    else
		temp+=s[i];
  }
  if(temp.size())
	v.push_back(temp);
  return v;
}

class edge
{
public:
  string name;
  node* to;
  edge(string _name,node* _to)
  {
    name = _name;
    to = _to;
  }
};

class node
{
  public:
    vector<edge> children;
    string address;
    string type;
    string value;
    string flags;
    node(string _address,string _type,string _value,string _flags)
    {
      address = _address;
      type = _type;
      value = _value;
      flags = _flags;
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

  node* addNode(string address,string type,string value,string flag)
  {
    if(get_node.find(address) == get_node.end())
      get_node[address] = new node(address,type,value,flag);

    return get_node[address];
  }

  void addChildren(string parent_address,string child_address,string name)
  {
	node *child = get_node[child_address];
	node *parent = get_node[parent_address];
	
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



graph g;

int main()
{
  string command_str= "";
  while(getline(cin,command_str))
  {
    vector<string>command = split(command_str,',');    
     if(command[0] == "1")
		g.addNode(command[1],command[2],command[3],command[4]);
	else
		g.addChildren(command[1],command[2],command[3]);
		  
  }
  return 0;
}
