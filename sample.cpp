#include <iostream>
using namespace std;
class a
{
	public:
	int x,y;
	a(int X ,int Y)
	{
		x = X;
		y = Y;
	}
	a()
	{
		x = y = 3;
	}
};
int main()
{
	a data2[4];
	int data[6] = {1,2,3,4,5};
	a temp(2,3);
	cout << "hey you";
	
	return 0;
}
