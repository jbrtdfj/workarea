grammar Hello;

top: module+ ; 

module : 'module' ID '(' list_of_ports ')' ';' module_item* ? 'endmodule';

list_of_ports: portname ( ',' portname )* ;

portname : ID; 

module_item : input_port  |
              output_port | 
              inout_port  | 
              wire        |
              supply0     |
              supply1     |
              assign      |
              instance;

input_port:  'input'   range? ID ';' ;
output_port: 'output'  range? ID ';' ;
inout_port:  'inout'   range? ID ';' ;
wire:        'wire'    range? ID ';' ;
supply0:     'supply0' range? ID ';' ;
supply1:     'supply1' range? ID ';' ;

range: '[' INT ':' INT ']' ;

assign: 'assign' ID '=' net ';' ;

instance: ID ID '(' portmap? ')' ';' ;

portmap: aportmap (',' aportmap)* ;

aportmap: '.' ID '(' net ')' ;

net: '{' ID (',' ID)* '}' | 
     CONSTANT             | 
     ID ;

CONSTANT : INT+'\''[bhx]INT+ ;


ID: '\\'? [a-zA-Z/] [a-zA-Z_0-9/_\[\]:]*;

INT: [0-9]+ ;
COMMENT1 : '//' .*? [\r]?[\n] -> skip ;
COMMENT2 : '/*' .*? '*/' -> skip ;
WS :      [ \t\n]+ -> skip ;

