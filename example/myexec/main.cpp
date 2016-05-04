#include "main.h"


int main(int argc, char* argv[]) {
	if        (argc!=2) {
		printf("Usage:\n%s [num]\n",argv[0]);
	} else {
		int x = atoi(argv[1]);
		int x_sq = mylib::square(x);
		printf("%d\n",x_sq);
	}

	return 0;
}
