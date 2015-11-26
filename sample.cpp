#include <iostream>
using namespace std;
class oo
{
	public:
	int x,y;
	int a[100];
	oo()
	{
		x = y= 6;
		for(int i = 0 ; i < 100 ; i++)
			a[i] = i;
	}
	void print()
	{
		cout << "Fw";
	}
};

int main()
{
	int x = 5,y = 6;
	oo bob;
	bob.print();
	return 0;
}
