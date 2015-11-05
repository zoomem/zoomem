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
class par{
	public:
	int x,y;
	par(){
		x = y = 1;
	}
};
class chld{
	public:
		par ss;
	chld(){
		ss = par();
	}
};
int main(){

	int x = 5;
	int c[100] = {0,1,2,3,4};
	unsigned long long cc = 45464;
	int *p = &x;
	chld hello;
	hello.ss.x = 2;
	a b;
	++x;
	return 0;
}
