grammar snap;
tokens { FILE, DECLS, NIL }
@header {
	//package snap;
}
@members {
}

SPACE:		[ \t\r\n]+ -> skip;
COMMENT:	'//' (~('\n'|'\r'))* -> skip;
STR:		'"' ( ~'"' )* '"';
INT:		[0-9]+ ;
ASSIGN:		'=' ;
SEP:		';' ;
PRINT:		'print' ;
COMMA:		',' ;
LBR:		'{' ;
RBR:		'}' ;
ADD:		'+' ;
ID:		[a-zA-Z_][a-zA-Z_0-9]* ;

snap	: decl* LBR instr* RBR EOF ;

decl	: ID ASSIGN STR SEP
	| ID ASSIGN INT SEP
	;

instr	: PRINT strs SEP
	;

strs	: expr
	| strs COMMA expr
	;

expr	: ID
	| INT
	| STR
	| expr ADD expr
	;
