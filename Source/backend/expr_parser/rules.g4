grammar rules;

rules
   : (singleRule)*
   ;

singleRule
   : variable COLON expression ARROW expression AT (constraint)? AT (constraint)? AT SUCCCOUNT SEMICOLON
   ;

constraint
   : equation
   | prefix=('~'|'!') constraint
   | constraint bop='&&' constraint
   | constraint bop='||' constraint
   ;

equation
   : expression relop expression
   ;


SUCCCOUNT
   : 'w''0'..'9'+
   ;

expression
   : expression (PLUS | MINUS) multiplyingExpression
   | multiplyingExpression 
   ;

multiplyingExpression
   : multiplyingExpression (TIMES | DIV) powExpression
   | powExpression 
   ;

powExpression
   : signedAtom (POW signedAtom)*
   ;

signedAtom
   : PLUS signedAtom
   | MINUS signedAtom
   | func
   | atom
   ;

atom
   : scientific
   | variable
   | constant
   | LPAREN expression RPAREN
   ;

scientific
   : SCIENTIFIC_NUMBER
   ;

constant
   : PI
   | EULER
   | I
   ;

variable
   : VARIABLE
   ;

func
   : funcname LPAREN expression (COMMA expression)* RPAREN
   ;

funcname
   : COS
   | SINH
   | COSH
   | TANH
   | POWF
   | EXP
   | TAN
   | SIN
   | SEC
   | CSC
   | COT
   | ACOS
   | ATAN
   | ASIN
   | LOG
   | LN
   | SQRT
   | CBRT
   | GAMMA
   | BERNOULLI
   | SUM
   | ABS
   | FACTORIAL
   | GET_ARC
   ;

relop
   : EQ
   | GT
   | LT
   | NEQ | GTE | LTE
   ;

POWF
   : 'pow'
   ;

EXP
   : 'exp'
   ;

COS
   : 'cos'
   ;

SINH
   : 'sinh'
   ;

COSH
   : 'cosh'
   ;

TANH
   : 'tanh'
   ;

SIN
   : 'sin'
   ;


TAN
   : 'tan'
   ;

COT
   : 'cot'
   ;

SEC
   : 'sec'
   ;

CSC
   : 'csc'
   ;

ACOS
   : 'acos'
   ;


ASIN
   : 'asin'
   ;


ATAN
   : 'atan'
   ;


LN
   : 'ln'
   ;


LOG
   : 'log'
   ;


SQRT
   : 'sqrt'
   ;

CBRT
   : 'cbrt'
   ;

GAMMA
   : 'gamma'
   ;

BERNOULLI
   : 'bnl'
   ;

SUM
   : 'sum'
   ;

ABS
   : 'abs'
   ;

FACTORIAL
   : 'fac'
   ;

GET_ARC
   : 'get_arc'
   ;

LPAREN
   : '('
   ;


RPAREN
   : ')'
   ;


PLUS
   : '+'
   ;


MINUS
   : '-'
   ;


TIMES
   : '*'
   ;


DIV
   : '/'
   ;


GT
   : '>'
   ;

GTE : '>=' ;

LT
   : '<'
   ;

LTE : '<=' ;

EQ
   : '='
   ;

NEQ : '!=' ;


COMMA
   : ','
   ;

COLON
   : ':'
   ;

SEMICOLON
   : ';'
   ;

POINT
   : '.'
   ;


POW
   : '^'
   | '**'
   ;


PI
   : 'pi'
   ;


EULER
   : 'r'
   ;


I
   : 'I'
   ;


ARROW
   : '->'
   ;

AT
   : '@'
   ;

VARIABLE
   : VALID_ID_START VALID_ID_CHAR*
   ;


fragment VALID_ID_START
   : ('a' .. 'z') | ('A' .. 'Z') | '_'
   ;


fragment VALID_ID_CHAR
   : VALID_ID_START | ('0' .. '9')
   ;


SCIENTIFIC_NUMBER
   : NUMBER ((E1 | E2) SIGN? NUMBER)?
   ;


fragment NUMBER
   : ('0' .. '9') + ('.' ('0' .. '9') +)?
   ;


fragment E1
   : 'E'
   ;


fragment E2
   : 'e'
   ;

fragment SIGN
   : ('+' | '-')
   ;

WhiteSpace
   : [ \r\n\t] + -> skip
   ;

LineComment
: '#' ~[\r\n]* -> skip
;
