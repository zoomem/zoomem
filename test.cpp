#include<iostream>
#include<stdio.h>
using namespace std;

class a
{
        public:
        int c,d;
				int cc[3];
				int *p;
        a()
        {
                c = d = 0;
								cc[0] = 1;
								p = &c;
        }
};
class type1{
	public:
	int x , y;
	type1(){
		x = y = 1;
	}
};
class type2{
	public:
	type1 s,t;
	type2(){
		s = t = type1();
	}
};
int main(){
	type2 tt;
	int x = 5;
	int *p = &x;
	int **pp = &p;
	int c[3] = {0,1,2};
	unsigned long long cc = 45464;
	a b;
	a *ccc = &b;

	return 0;
}
