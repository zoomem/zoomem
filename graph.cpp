#include <iostream>
#include <string>
#include <set>
#include <vector>
#include <map>
using namespace std;

class node;
class edge;
string flags[5] = {"","POINTER_FLAG","ARRAY_FLAG","OBJECT_FLAG","PRIMITIVE_FLAG"};

map<string,node*>get_node;
set<string> del;
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

int x = 0;
class node
{
  public:
    vector<edge> children;
    string address;
    string type;
    string size;
    string value;
    string flag;
    
	void print()
	{
		for(int i = 0 ; i < children.size();i++)
		{
			cout << "parent : " << this->address;
			cout << " var name : " << children[i].name;
			node* child = children[i].to;
			cout << " Adress : " << child->address;
			cout << " Type : " << child->type;
			cout << " Size  : " << child->size;
			cout << " value : " << child->value;
			cout << " Flags : " << flags[(child->flag)[0] - '0'];
			cout << endl << endl;
			child->print();
		}
	}
	
    node(string &_address,string &_type,string &_value,string &_size,string &_flag)
    {
      address = _address;
      type = _type;
      value = _value;
      flag = _flag;
      size = _size;
    }
    
    ~node() {
	  x++;
      for(int i = 0 ; i < children.size();i++)
		if(children[i].to)
		{
			if(del.find(children[i].to->address) == del.end())
			{
				del.insert(children[i].to->address);
				delete children[i].to;
			}
		}
    }
};


class graph
{

public:

  node *root_node;
  
  graph()
  {
	  string name = "$root";
	  root_node = addNode(name,name,name,name,name);
  }

  node* addNode(string &address,string &type,string &value,string &size,string &flag)
  {
    if(get_node.find(address) == get_node.end())
      get_node[address] = new node(address,type,value,size,flag);
    node* new_node = get_node[address];
    return new_node;
  }
  
  void addChildren(string &parent_address,string &child_address,string &name)
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

int main()
{
  graph g;
  //reopen("in.txt","r",stdin);
  string command_str= "";
  while(getline(cin,command_str))
  {
	if(command_str == "end")
		break;
		
    vector<string>command = split(command_str,',');
    if(command[0] == "1")
		g.addNode(command[1],command[2],command[3],command[4],command[5]);

	else if(command[0] == "2")
		g.addChildren(command[1],command[2],command[3]);
  }
  g.print_graph();
  return 0;
}
