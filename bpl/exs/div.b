main()
{
  extrn getint(), putint(), putstr();
  auto i, n, d;

  d = 0;
  n = getint();
  if (n > 0) {
    i = 2;
    while (i <= n/2) {
      if (n % i == 0) {
	putint(n);
	putstr(" divides by ");
	putint(i);
	putstr("*n");
	d = d + 1;
      }
      i = i + 1;
    }
    if (d == 0) {
      putint(n);
      putstr(" is prime.*n");
    }
  }
  return(0);
}
