main()
{
  extrn getstr(), putchar(), putstr(), strlen();
  auto x, v, i;
  v # 2;
  v[0] # 100;
  v[1] # 100;
  i = 0;
  x = v[i];
  getstr(x, 400);
  while (strlen(x) != 0) {
    i = 1 - i;
    x = v[i];
    getstr(x, 400);
    x = v[0]; putstr(x); putchar('*n');
    x = v[1]; putstr(x); putchar('*n');
    x = v[i];
  }
  return (0);
}
