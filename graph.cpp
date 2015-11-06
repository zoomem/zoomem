#include <iostream>
#include <string>
#include <set>
#include <vector>
#include <map>
using namespace std;

class node;
class edge;

map<string,node*>get_node;
set<string>child_node;

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
    string size;
    string value;
    string flags;
	void print()
	{
		for(int i = 0 ; i < children.size();i++)
		{
			cout << "var name " << children[i].name;
			node* child = children[i].to;
			cout << " Adress " << child->address;
			cout << " Type " << child->type;
			cout << " Size " << child->size;
			cout << " value " << child->value;
			cout << " Flags " << child->flags;
			cout << endl;
			child->print();
		}
	}
    node(string _address,string _type,string _value,string _size,string _flags)
    {
      address = _address;
      type = _type;
      value = _value;
      flags = _flags;
      size = _size;
    }
    ~node() {
      for(int i = 0 ; i < children.size();i++)
        delete children[i].to;
    }
};


class graph
{

public:

  node *root_node;
  graph()
  {
	  root_node = addNode("$root","root_node","","","");
  }

  node* addNode(string address,string type,string value,string size,string flag)
  {
    if(get_node.find(address) == get_node.end())
      get_node[address] = new node(address,type,value,size,flag);

    node* new_node = get_node[address];

    return new_node;

  }

  void addChildren(string parent_address,string child_address,string name)
  {
	node *child = get_node[child_address];
	node *parent = get_node[parent_address];

    parent->children.push_back(edge(name,child));
  }

  void print_graph()
  {
    root_node->print();
  }
  ~graph()
  {
    delete root_node;
  }

};



graph g;

int main()
{
  string command_str= "";
  while(getline(cin,command_str))
  {
    cout << command_str << endl;
	  if(command_str == "end")
		  break;
    vector<string>command = split(command_str,',');
    if(!command.size())
    {
		    cout << "error 1";
		      continue;
	  }

    if(command[0] == "1")
    {
      if(command.size() < 6)
      {
        cout <<"Error 2";
        continue;
		  }
		g.addNode(command[1],command[2],command[3],command[4],command[5]);
	}

	else if(command[0] == "2")
	{
	  if(command.size() < 4)
		{
			cout <<"Error 3";
			continue;
		}
		g.addChildren(command[1],command[2],command[3]);
	}

  }
  g.print_graph();
  return 0;
}
