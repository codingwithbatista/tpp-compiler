#include<string.h>
#include "../lib/lex.h"

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
Token create_token() {
    Token token;
    token.lexeme = "";
    token.number_of_line = -1;
    token.init_column_number = -1;
    token.final_column_number = -1;
    token.tokenval = "";
    return token;
}

Token getToken(FILE *sourceCode_file) {
    char character = fgetc(sourceCode_file);
    Token token = create_token();

    if(character == EOF) return token;

    char *lexeme = malloc(sizeof(char));
    int index = 0;
    while(character != EOF && is_tokenLimiter(character) == FALSE) {
        if(index > 0) lexeme = realloc(lexeme, (index + 1) * sizeof(char));
        lexeme[index] = character;
        character = fgetc(sourceCode_file);
        index++;
    }
    
    token.lexeme = (char*) malloc(sizeof(char) * strlen(lexeme));
    strcpy(token.lexeme, lexeme);
    free(lexeme);
    return token;     
}

TokenList create_tokenlist() {
    TokenList tokenlist;
    tokenlist.size = 0;
    return tokenlist;
}

void add_to_tokenlist(TokenList tokenlist, Token token) {
    tokenlist.elements = (Token*) malloc(sizeof(Token) * (tokenlist.size + 1));
    tokenlist.elements[tokenlist.size] = token;
    tokenlist.size = tokenlist.size + 1;
}