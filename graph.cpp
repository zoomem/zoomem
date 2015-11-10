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
set<string>vis;
map<node *,int>node_id;
int id = 0;

int get_id(node *n)
{
  if(node_id.find(n) == node_id.end())
    node_id[n]= ++id;
  return node_id[n];
}

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

string hash_node(node* _node);

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
			cout << "node_iden : " << get_id(children[i].to);
			cout << " ,parent : " << this->address;

			cout << " ,var name : " << children[i].name;
			node* child = children[i].to;
			cout << " ,Adress : " << child->address;
			cout << " ,Type : " << child->type;
			cout << " ,Size  : " << child->size;
			cout << " ,value : " << child->value;
			cout << " ,Flags : " << flags[(child->flag)[0] - '0'];
			cout << endl;
			if(vis.find(hash_node(child)) == vis.end())
			{
				vis.insert(hash_node(child));
				child->print();
			}
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
      for(int i = 0 ; i < children.size();i++)
		if(children[i].to)
		{
			node* child = children[i].to;
			if(del.find(hash_node(child)) == del.end())
			{
				del.insert(hash_node(child));
			}
			else
				cout <<"kos kos";
		}
    }
};

string hash_node(node* _node)
{
	return (_node->address + "_" + _node->type);
}

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
    if(get_node.find(address + "_" + type) == get_node.end())
      get_node[(address + "_" + type)] = new node(address,type,value,size,flag);
    node* new_node = get_node[(address + "_" + type)];
    return new_node;
  }

  void addChildren(string &parent_address,string &parent_type,string &child_address,string child_type,string &name)
  {
	node *child = get_node[(child_address + "_" + child_type)];
	node *parent = get_node[parent_address + "_" + parent_type];

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
		g.addChildren(command[1],command[2],command[3],command[4],command[5]);
  }
  g.print_graph();
  return 0;
}
