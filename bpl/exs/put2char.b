main( ) {
  extrn a,b,c,d, put2char();
  put2char(a,b) ;
  put2char(c,d) ;
}
put2char(x,y) {
extrn putchar();
putchar(x);
putchar(y);
}

a 'hell'; b 'o, w'; c 'orld'; d '!*n';
