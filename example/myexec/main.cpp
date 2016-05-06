#include "main.h"

#include <cstdio>
#include <cstdlib>


int main(int argc, char* argv[]) {
	if        (argc!=2) {
		printf("Usage:\n%s [num]\n",argv[0]);
	} else {
		int x = atoi(argv[1]);
		int x_sq = mylib::square(x);
		printf("%d\n",x_sq);
	}
	printf("ENTER to exit.\n");
	getchar();

	return 0;
}
