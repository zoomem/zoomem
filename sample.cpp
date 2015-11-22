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
	void print()
	{
		cout << x << " "<< y << endl;
	}

};
int main()
{
	a v1(2,3);
	v1.print();
	int a[3] = {0};
	return 0;
}
