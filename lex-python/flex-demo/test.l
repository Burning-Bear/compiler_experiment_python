%{
    #include <stdio.h>
    #include <stdlib.h> 
    int count = 0;
    # define IF =15
    # define THEN = 16
    # define WHILE = 17
    # define DO = 18
    # define INTEGER = 19
    # define FLOAT = 20
%} 
if if
then then
while while
do do
operator \+|-|\*|\/|=
relation_op >=|<=|==|!=
type int|float
delim [ \n\t] 
whitespace {delim}+ 
delimiter [,\.;\(\)]
digit [0-9]
constant {digit}+
letter [A-Za-z]
identfier {letter}(letter|{digit})* 
block [{}]
%% 
{if} {count++;printf("%d\t(if,‘%s’)\n",count,yytext);}
{then} {count++;printf("%d\t(then,‘%s’)\n",count,yytext);}
{while} {count++;printf("%d\t(while,‘%s’)\n",count,yytext);}
{do} {count++;printf("%d\t(do,‘%s’)\n",count,yytext);}
{type} {count++;printf("%d\t(type,‘%s’)\n",count,yytext);}
{operator} { count++;printf("%d\t(operator,‘%s’)\n",count,yytext); }
{relation_op} { count++;printf("%d\t(relation_op,‘%s’)\n",count,yytext); }
{delimiter} {count++;printf("%d\t(delimiter,‘%s’)\n",count,yytext);}
{constant} {count++;printf("%d\t(constant,‘%s’)\n",count,yytext);}
{block} {count++;printf("%d\t(block,‘%s’)\n",count,yytext);} 
{identfier} {count++;printf("%d\t(identfier,‘%s’)\n",count,yytext);} 
{whitespace} { /* do    nothing*/ } 
%% 

void main() 
{
    printf("词法分析器输出类型说明:\n");
    printf("1：保留字\n");
    printf("2：运算符\n");
    printf("3：分界符\n");
    printf("4：常  数\n");
    printf("5：标识符\n");
    printf("\n");
    yyin=fopen("test.txt","r"); 
        yylex(); /* start the analysis*/ 
    fclose(yyin);
} 
 int yywrap() 
 { 
    return 1; 
 } 