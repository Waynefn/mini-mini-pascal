# mini-mini-pascal
A mini-mini-pascal language compiler and execute machine.

Contributor
- C. XB (TMU) 90%
- L. ZX (UT) 10%

## Grammar
### Character:
- Number: [0-9]
- Alphabeta: [A-Z]
- Symbol: SPACE ( ) * / + - ; : < = >
- Keyword: READ, WRITE, WHILE, DO, ENDWHILE
### program
- statement(;statement)*\\.
### statement
- READ(var)
- WRITE(var)
- VAR:=expr
- WHILE cmp DO statement (;statement)* ENDWHILE
### cmp
- expr (>|=|<) expr
### expr
- (+|-) term ((+|-)term)*
### term
- factor ((*|/)factor)*
### factor
- var
- constant
- \\(expr\\)
### finite mark
- var: [A-Z]
- constant: [0-9]+

## Machine

Machine command:
```
GET X:	Get
PUT X:	Put
LOD X:	Load
LDC I:	Load Constant
STR X:	Store
ADD:	Add
SUB:	Subtract
MLT:	Multiply
DIV:	Divide
EQL:	Equal
GRT:	Greater than
LES:	Less than
CJP K:	Conditional Jump
UJP K:	Unconditional Jump
```

## Compile process
source --(lex)--> token --(syntax)--> syntax --(coding)--> assamble --(machine)--> execution
### Example
#### source
```
READ(L);
A:= 0; K:= 1;
WHILE K < L+1 DO
A:= A+K;
K:= K+1
ENDWHILE;
WRITE(A).
```
#### token
```
KEYWORD:READ
 OP:(
 VAR:L
 OP:)
 SEP:;
 VAR:A
 OP::
 OP:=
 NUMBER:0
 SEP:;
 VAR:K
 OP::
 OP:=
 NUMBER:1
 SEP:;
 KEYWORD:WHILE
 VAR:K
 OP:<
 VAR:L
 OP:+
 NUMBER:1
 KEYWORD:DO
 VAR:A
 OP::
 OP:=
 VAR:A
 OP:+
 VAR:K
 SEP:;
 VAR:K
 OP::
 OP:=
 VAR:K
 OP:+
 NUMBER:1
 KEYWORD:ENDWHILE
 SEP:;
 KEYWORD:WRITE
 OP:(
 VAR:A
 OP:)
 SEP:.
```

#### syntax
```
READ:L
['ASSIGN', 'A', [NUMBER:0]]
['ASSIGN', 'K', [NUMBER:1]]
['GOTO_REL', 75442]
['RELATION', ['<', [VAR:K], [VAR:L, NUMBER:1, OP:+]]]
['GOTO_CJP', 75442]
['ASSIGN', 'A', [VAR:A, VAR:K, OP:+]]
['ASSIGN', 'K', [VAR:K, NUMBER:1, OP:+]]
['GOTO_UJP', 75442]
WRITE:A
```
#### assamble
```
GET 11
LDC 0
STR 0
LDC 1
STR 10
LOD 10
LOD 11
LDC 1
ADD
LES
CJP 20
LOD 0
LOD 10
ADD
STR 0
LOD 10
LDC 1
ADD
STR 10
UJP 5
PUT 0
```
