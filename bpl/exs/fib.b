fib(n)
{
  if (n <= 1) return(n);
  return (fib(n-1)+fib(n-2));
}

main()
{
  extrn putstr(), getint(), putint();
  auto n;

  putstr("enter number of Fibonacci sequence to determine: ");
  n = getint();
  putint(fib(n));
  putstr("*n");
  return(0);
}
