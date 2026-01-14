from errors import IllegalCharError, InvalidSyntaxError
class TokenType:
    #Literali
    NUMBER= 'NUMBER'
    STRING= 'STRING'
    TRUE= 'TRUE'
    FALSE= 'FALSE'
    #Keywords
    IF= 'IF'
    ELSE= 'ELSE'
    WHILE= 'WHILE'
    BEGIN='BEGIN'
    DO='DO'
    END='END'
    FOR= 'FOR'
    TO='TO'
    DEF= 'DEF'
    RETURN= 'RETURN'
    PRINT= 'PRINT'
    AND= 'AND'
    OR= 'OR'
    NOT= 'NOT'
    LEN = 'LEN'
    INPUT = 'INPUT'
    TO_INT = 'TO_INT'
    TO_STR = 'TO_STR'

    #Identificatori nume variabile
    IDENTIFIER= 'IDENTIFIER'
    #Operatori
    PLUS= 'PLUS'#+
    MINUS= 'MINUS'#-
    MULTIPLY= 'MULTIPLY'#*
    DIVIDE= 'DIVIDE'#/
    MODULO= 'MOD'#%
    ASSIGN= 'ASSIGN'#=
    EQUAL= 'EQUAL'#==
    NOT_EQUAL= 'NEQUAL'#!=
    LESS= 'LESS'#
    LESS_EQUAL= 'LQUAL'#<=
    GREATER= 'GREATER'#>
    GREATER_EQUAL= 'GQUAL' #>=
    #Paranteze si separatori
    LPAREN= 'LPAREN' #(
    RPAREN= 'RPAREN' #)
    LBRACE= 'LBRACE' #{
    RBRACE= 'RBRACE' #}
    COMMA= 'COMMA' #,
    COLON= 'COLON' #:
    SEMICOLON= 'SEMICOLON' #;
    LBRACKET='LBRACKET'
    RBRACKET='RBRACKET'
    #Altele
    EOF= 'EOF' 
    NEWLINE= 'NEWLINE' 

class Token:
    def __init__(self, type, value,line,column):
        self.type=type
        self.value=value
        self.line=line
        self.column=column
    def __repr__(self):
        return f"Token({self.type},{self.value!r},{self.line}:{self.column})"
class Lexer:
    KEYWORDS={
        'if':TokenType.IF,
        'else':TokenType.ELSE,
        'while':TokenType.WHILE,
        'begin':TokenType.BEGIN,
        'end':TokenType.END,
        'do': TokenType.COLON,
        'for':TokenType.FOR,
        'to':TokenType.TO,
        'def':TokenType.DEF,
        'return':TokenType.RETURN,
        'print':TokenType.PRINT,
        'true':TokenType.TRUE,
        'false':TokenType.FALSE,
        'and':TokenType.AND,
        'or':TokenType.OR,
        'not':TokenType.NOT,
        'len': TokenType.LEN,
        'input': TokenType.INPUT,
        'to_int': TokenType.TO_INT,
        'to_str': TokenType.TO_STR,


    }
    def __init__(self, source):
        self.source=source
        self.pos=0
        self.line=1
        self.column=1
        self.tokens=[]
    def peek(self):
        """Se uita la caracterul curent fara sa avanseze"""
        if self.pos < len(self.source):
            return self.source[self.pos]
        return None #daca am terminat cuvantul
    def advance(self):
        """Returneaza caracterul curent si avanseaza pozitia"""
        if self.pos<len(self.source):
            char=self.source[self.pos]
            self.pos+=1
            if char=='\n':
                self.line+=1
                self.column=1
            else:
                self.column+=1
            return char
        return None
    #metode ajustatoare
    def skip_whitespace(self):
        """Sare peste spatii"""
        while self.peek() is not None and self.peek() in ' \t\r':
            self.advance()
    def read_number(self):
        """Citeste numere (ex: 10 sau 12.2)"""
        start_col =self.column
        num_str=''
        has_dot = False
        while self.peek() is not None and (self.peek().isdigit() or self.peek() == '.'):
            if self.peek() == '.':
                if has_dot:
                    raise InvalidSyntaxError(
                        f"Numar invalid: prea multe puncte In '{num_str}.'",
                        self.line,
                        self.column
                    )
                has_dot = True
            num_str += self.advance()
        
        if '.' in num_str:
            return Token(TokenType.NUMBER, float(num_str), self.line, start_col)
        return Token(TokenType.NUMBER, int(num_str), self.line, start_col)
    def read_identifier(self):
        """Citeste variabile (x, suma) sau keywords (if, while)"""
        start_col = self.column
        ident = ''
        while self.peek() is not None and (self.peek().isalnum() or self.peek() == '_'):
            ident += self.advance()
            
        token_type = self.KEYWORDS.get(ident.lower(), TokenType.IDENTIFIER)
        return Token(token_type, ident, self.line, start_col)
    def read_string(self):
        """Citeste text intre ghilimele"""
        start_col = self.column
        quote = self.advance()  # " sau '
        content = ''
        while self.peek() is not None and self.peek() != quote:
            if self.peek() == '\n':
                raise InvalidSyntaxError(
                    "String neinchis (lipseste ghilimea de inchidere)",
                    self.line,
                    start_col
                )
            content += self.advance()
        if self.peek() is None:
            raise InvalidSyntaxError(
                "String neinchis (lipseste ghilimea de inchidere)",
                self.line,
                start_col
            )
        self.advance()  
        return Token(TokenType.STRING, content, self.line, start_col)
    def tokenize(self):
        """Transforma sursa in lista de tokeni"""
        while self.pos <len(self.source):
            current_char = self.peek()
            self.skip_whitespace()
            char = self.peek()
            if char is None:
                break
            #numere
            if char.isdigit():
                token = self.read_number()
                self.tokens.append(token)
                continue
            #identificatori litere
            if char.isalpha() or char == '_':
                token = self.read_identifier()
                self.tokens.append(token)
                continue
            #stringuri
            if char in ['"',"'"]:
                token = self.read_string()
                self.tokens.append(token)
                continue
            #operatori si simboluri: trebuie sa tratam si cazurile duble == != <= >=
            col=self.column
            if char == '\n' :
                self.tokens.append(Token(TokenType.NEWLINE, '\n', self.line, col))
                self.advance()
                continue
            if char == '+':
                self.advance()
                self.tokens.append(Token(TokenType.PLUS,'+',self.line,col))
                continue
            if  char == '-':
                self.advance()
                self.tokens.append(Token(TokenType.MINUS,'-',self.line,col))
                continue
            if  char == '*':
                self.advance()
                self.tokens.append(Token(TokenType.MULTIPLY,'*',self.line,col))
                continue
            if  char == '/':
                self.advance()
                self.tokens.append(Token(TokenType.DIVIDE,'/',self.line,col))
                continue
            if  char == '%':
                self.advance()
                self.tokens.append(Token(TokenType.MODULO,'%',self.line,col))
                continue
            if char == ':':
                self.tokens.append(Token(TokenType.COLON, ':', self.line, col))
                self.advance()
                continue
            if char == ',':
                self.tokens.append(Token(TokenType.COMMA, ',', self.line, col))
                self.advance()
                continue
            if char == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', self.line, col))
                self.advance()
                continue
            if char == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', self.line, col))
                self.advance()
                continue
            if char == '[':
                self.tokens.append(Token(TokenType.LBRACKET, '[', self.line, col))
                self.advance()
                continue
            if char == ']':
                self.tokens.append(Token(TokenType.RBRACKET, ']', self.line, col))
                self.advance()
                continue
            if  char == '=':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.EQUAL,'==',self.line,col))
                else:
                    self.tokens.append(Token(TokenType.ASSIGN,'=',self.line,col))
                continue
            if char == '!':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.NOT_EQUAL, '!=', self.line, col))
                else:
                    raise InvalidSyntaxError("Se asteapta '=' dupa '!')",self.line,col)
                continue
            if char == '>':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.GREATER_EQUAL, '>=', self.line, col))
                else:
                    self.tokens.append(Token(TokenType.GREATER, '>', self.line, col))
                continue
            if char == '<':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.LESS_EQUAL, '<=', self.line, col))
                else:
                    self.tokens.append(Token(TokenType.LESS, '<', self.line, col))
                continue
            if char == '#':
                while self.peek() is not None and self.peek() != '\n':
                    self.advance()
                continue
            raise IllegalCharError(f"Caracterul '{char}' nu este permis",self.line,col)
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
    