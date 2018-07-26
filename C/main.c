#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#define TRUE 1
#define FALSE 0
#define BOOLEAN int

FILE* read_sourceCode(char *filepath) {
    FILE *fp = fopen(filepath, "r");
    return fp;
}

BOOLEAN is_tokenLimiter(char character) {
    if(character == ':' || character == '(' || character == ')' || character == '[' || character == ']' 
    || character == '&' || character == '|' || character == '+' || character == '-' || character == '/'
    || character == '*' || character == '=' || character == '<' || character == '>' || character == ','
    || character == '{' || character == '}') 
        return TRUE;
    
    else return FALSE;
}

char* getToken(FILE *sourceCode_file) {
    char character = fgetc(sourceCode_file);
    if(character == EOF) return NULL;
    char *lexeme = malloc(sizeof(char));
    int index = 0;
    while(character != EOF && is_tokenLimiter(character) == FALSE) {
       //printf("%d\n",is_tokenLimiter(character));
        if(index > 0) lexeme = realloc(lexeme, (index + 1) * sizeof(char));
        lexeme[index] = character;
        character = fgetc(sourceCode_file);
        index++;
    }
    return lexeme;     
}


int main(int argc, char **argv) {
    char *filepath = argv[1];
    FILE *fp = read_sourceCode(filepath);
    char *lexeme = getToken(fp);
    printf("%s\n", lexeme);
    return 0;
}