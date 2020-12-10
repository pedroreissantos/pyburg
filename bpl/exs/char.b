v[] 0, 0;
bpb 8; /* bits per byte */
bpw 0; /* bytes per word */

char(vec, pos)
{
  bpw = &v[1] - &v[0];
  return ((vec[pos/bpw] >> (pos % bpw * bpb)) & 255);
}

lchar(vec, pos, val)
{
  bpw = &v[1] - &v[0];
  return (vec[pos/bpw] = (vec[pos/bpw] & ~(255 << (pos % bpw * bpb))) | ((val & 255) << (pos % bpw * bpb)));
}

putchar(ch)
{
  extrn putstr();
  auto i, prt;
  i = -1;
  bpw = &v[1] - &v[0];
  while ((++i < bpw) & ((ch & 255) != 0)) {
    prt = ch & 255;
    putstr(&prt);
    ch = ch >> bpb;
  }
  return (i);
}
