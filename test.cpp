#include<iostream>
#include<stdio.h>
using namespace std;

class a
{
	public:
	int c,d;
	a()
	{
		c = d = 0;
	}
};
int main(){

	int x = 5;
	int *p = &x;
	int **pp = &p;
	int c[5] = {0,1,2,3,4};
	unsigned long long cc = 45464;
	a b;
	return 0;
}
