#include <stdio.h>
#ifdef UNDERSCORE
#define printi _printi
#define prints _prints
#define println _println
#endif
extern int _main();
int main() { return _main(); }
int printi(int i) { return printf("%d", i); }
int prints(char *s) { return printf("%s", s); }
int println() { return printf("\n"); }
