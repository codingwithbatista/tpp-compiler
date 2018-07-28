#include<stdio.h>
#include<stdlib.h>
#ifndef _LEX1_H
#define _LEX1_H

#define TRUE 1
#define FALSE 0
#define BOOLEAN int
 typedef struct token{
     char *lexeme;
     char *tokenval;
     int number_of_line;
     int init_column_number;
     int final_column_number;
 } Token;

typedef struct {
    Token *elements;
    int size;
}TokenList;

Token create_token();
TokenList create_tokenlist();
FILE* read_sourceCode(char*);
BOOLEAN is_tokenLimiter(char);
void add_to_tokenlist(TokenList, Token);
Token getToken(FILE *);

#endif 