main()
{
  extrn getint(), putstr();
  auto a, b, c;
  a = b = c = 0;
  a = getint();
  b = getint();
  c = getint();
  if (a < 1 | b < 1 | c < 1)
    putstr("Dimensions must be positive numbers*n");
  else if (a + b <= c | a + c <= b | c + b <= a)
    putstr("Is not a triangle*n");
  else if (a == b & b == c)
    putstr("The triangle is equilateral*n");
  else if (a == b | b == c | c == a)
    putstr("The triangle is isosceles*n");
  else
    putstr("The triangle is scalene*n");
  return (0);
}
