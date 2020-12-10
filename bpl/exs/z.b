main()
{
  extrn putchar(), char(), argc(), argv();
  auto i, ch, str;

  if (argc() > 1) {
    i = 0;
    str = argv(1);
    while ((ch = char(str,i)) != '*0') {
      putchar(ch);
      i++;
    }
    putchar('*n');
  }
  return(0);
}
