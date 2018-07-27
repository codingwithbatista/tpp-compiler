#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include "lib/lex.h"


int main(int argc, char **argv) {
    char *filepath = argv[1];
    FILE *fp = read_sourceCode(filepath);
    Token token = getToken(fp);
    printf("%s\n", token.lexeme);
    return 0;
}