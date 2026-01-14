from lexer import TokenType
from nodes import *
class Parser:
    def __init__(self, tokens):
        self.tokens=tokens
        self.pos=0
        self.current_token=self.tokens[0] if tokens else None
    def error(self,message):
        """Opreste totul daca apare o eroare de sintaxa"""
        raise Exception(f"Eroare de sintaxa: {self.current_token.line}:{message}")
    def advance(self):
        """Trece la urmatorul token"""
        self.pos+=1
        if self.pos <len(self.tokens):
            self.current_token=self.tokens[self.pos]
        else:
            self.current_token=None  
    def expect(self,token_type):
        """Verifica daca tokenul curent este cel asteptat.
        Daca DA il avanseaza si il returneaza.
        Daca NU da eroare. Ex: asteptam '=' dar am gasit '10.
        """
        if self.current_token.type == token_type:
            token=self.current_token
            self.advance()
            return token
        else:
            self.error(f"Ma asteptam la {token_type},dar am gasit {self.current_token.type}")
    def peek(self):
        """Se uita la urmatorul token fara sa avanseze"""
        if self.pos+1 <len(self.tokens):
            return self.tokens[self.pos+1]
        return None
    def parse(self):
        """Metoda principala care parcurge tot fisierul"""
        statements = []
        #cat timp nu am ajuns la finalul fisierului 
        while self.current_token and self.current_token.type!= TokenType.EOF:
            #sarim peste liniile goale / \n 
            if self.current_token.type ==TokenType.NEWLINE:
                self.advance()
                continue
            stmt=self.statement()
            statements.append(stmt)
        return statements
    def compound_statement(self):
        self.expect(TokenType.BEGIN)
        nodes = []
        while self.current_token.type !=TokenType.END and self.current_token.type != TokenType.EOF:
            if self.current_token.type==TokenType.NEWLINE:
                self.advance()
                continue
            stmt = self.statement()
            nodes.append(stmt)        
        self.expect('END')
        return nodes
    def statement(self):
        """Decide ce instructiune urmeaza"""
        #print?
        if self.current_token.type ==TokenType.PRINT:
            return self.parse_print()
        #if? facem direct pe loc
        if self.current_token.type == TokenType.DEF:
            return self.parse_function_def()
        if self.current_token.type == TokenType.RETURN:
            return self.parse_return()
        if self.current_token.type == TokenType.IF:
            return self.parse_if()
        if self.current_token.type == TokenType.WHILE:
            return self.parse_while()
        if self.current_token.type == TokenType.BEGIN:
            return self.compound_statement()
        if self.current_token.type == TokenType.FOR:
            return self.parse_for()
        if self.current_token.type == TokenType.IDENTIFIER: 
            next_token=self.peek()
            if next_token and next_token.type == TokenType.LPAREN:
                return self.parse_expression()
            else : 
                return self.parse_assignment()
        self.error(f"Instructiunea necunocuta{self.current_token.type}")
    def parse_print(self):
        """
         Gramatica PRINT LPAREN expression RPAREN
         ex: print("Salut")
        """
        self.expect(TokenType.PRINT) # citeste print
        self.expect(TokenType.LPAREN) #(
        expr= self.parse_expression() #parseaza ce e in paranteza
        self.expect (TokenType.RPAREN)#)
        return  Print(expr) #returneaza nodul ast
    def parse_assignment (self):
        """
        Gramatica: IDENTIFIER ASSIGN expression
        ex: x=10
        """
        #salvam numele variabilei
        name_token=self.expect(TokenType.IDENTIFIER)
        # =
        self.expect(TokenType.ASSIGN)
        #parsam valoarea
        value=self.parse_expression()
        return Assign(name_token.value,value)
    def parse_expression(self):
        return self.parse_comparison()
    def parse_term(self):
        """
        face + si -
        ex 5+2
        """
        left=self.parse_factor()
        while self.current_token and self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
           op_token=self.current_token
           self.advance()
           right=self.parse_factor()
           left=BinOp(left,op_token.value,right)
        return left
    def parse_factor(self):
        """
        face * si /
        """
        left =self.parse_primary()
        while self.current_token and self.current_token.type in [TokenType.MULTIPLY,TokenType.DIVIDE,TokenType.MODULO]:
            op_token=self.current_token
            self.advance()
            right=self.parse_primary()
            left=BinOp(left,op_token.value,right)
        return left
    def parse_list(self):
        self.expect(TokenType.LBRACKET)
        token = self.current_token
        elements = []
        if self.current_token.type != TokenType.RBRACKET:
            elements.append(self.parse_expression())
            while self.current_token.type == TokenType.COMMA:
                self.advance()
                elements.append(self.parse_expression())
        self.expect(TokenType.RBRACKET) 
        return ListNode(elements)
    def parse_primary(self):
        token = self.current_token
        if token.type == TokenType.LBRACKET:
            return self.parse_list()
        if token.type == TokenType.NUMBER:
            self.advance()
            return Number(token.value)
        elif token.type == TokenType.STRING:
            self.advance()
            return String(token.value)
        elif token.type == TokenType.IDENTIFIER:
            name = token.value
            self.advance()
            if self.current_token.type == TokenType.LPAREN:
                self.advance()
                args = []
                if self.current_token.type != TokenType.RPAREN:
                    args.append(self.parse_expression())
                    while self.current_token.type == TokenType.COMMA:
                        self.advance()
                        args.append(self.parse_expression())
                self.expect(TokenType.RPAREN)
                node = Call(name, args)
            else:
                node = Variable(name)
            if self.current_token.type == TokenType.LBRACKET:
                self.advance()
                index = self.parse_expression() 
                self.expect(TokenType.RBRACKET) 
                node = GetItem(node, index) 
            return node
        if token.type == TokenType.LEN:
            self.advance()
            self.expect(TokenType.LPAREN)
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return Len(expr)

        if token.type == TokenType.TO_INT:
            self.advance()
            self.expect(TokenType.LPAREN)
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return ToInt(expr)
            
        if token.type == TokenType.TO_STR:
            self.advance()
            self.expect(TokenType.LPAREN)
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return ToStr(expr)

        if token.type == TokenType.INPUT:
            self.advance()
            self.expect(TokenType.LPAREN)
            self.expect(TokenType.RPAREN)
            return Input()
        
        elif token.type == TokenType.LPAREN:
            self.advance() 
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN) 
            return expr
        self.error(f"Expresie invalida. Am gasit {token.type}")
    def parse_if(self):
        self.expect(TokenType.IF)
        condition=self.parse_expression()
        self.expect(TokenType.COLON)
        while self.current_token.type==TokenType.NEWLINE:
            self.advance()
        then_stmt=self.statement()
        else_branch=None
        while self.current_token.type ==TokenType.NEWLINE:
            self.advance()
        if self.current_token.type ==TokenType.ELSE:
            self.advance()
            self.expect(TokenType.COLON)
            while self.current_token.type == TokenType.NEWLINE:
                self.advance()

            else_stmt=self.statement()
            else_branch=[else_stmt]
        
        return If(condition,[then_stmt],else_branch)
    def parse_comparison(self):
        #daca urmeaza un operator de comparatie
        left=self.parse_term()
        if self.current_token and self.current_token.type in [TokenType.LESS, TokenType.GREATER, TokenType.EQUAL, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL, TokenType.NOT_EQUAL]:
            op=self.current_token
            self.advance()
            right=self.parse_term()
            return BinOp(left,op.value,right)
        return left
    def parse_while(self):
        self.expect(TokenType.WHILE)
        condition = self.parse_expression()
        self.expect(TokenType.COLON)
        while self.current_token.type == TokenType.NEWLINE:
            self.advance()
        body_stmt = self.statement()
        if isinstance(body_stmt,list):
            return While(condition,body_stmt)
        else:
            return While(condition, [body_stmt])
    def parse_for(self):
        self.expect(TokenType.FOR)#citim for
        #citim variabile
        var_token=self.expect(TokenType.IDENTIFIER)
        var_name=var_token.value
        #citim =
        self.expect(TokenType.ASSIGN)
        #citim valoarea de start
        start_value=self.parse_expression()
        #citim to
        self.expect(TokenType.TO)
        #citim valoare de final
        end_value=self.parse_expression()
        #citim do 
        self.expect(TokenType.COLON)
        #parsam corpul
        while self.current_token.type ==TokenType.NEWLINE:
            self.advance()
        body=self.statement()
        if not isinstance (body,list):
            body=[body]
        return For(var_name,start_value,end_value,body)
    def parse_expression(self):
        return self.parse_logic()
    def parse_logic(self):
        left=self.parse_comparison()
        while self.current_token.type in [TokenType.AND, TokenType.OR]:
            op_token=self.current_token
            self.advance()
            right=self.parse_comparison()
            left=BinOp(left,op_token.type,right)
        return left
    def parse_function_def(self):
        self.expect(TokenType.DEF)
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.LPAREN)
        params = []
        if self.current_token.type != TokenType.RPAREN:
            params.append(self.expect(TokenType.IDENTIFIER).value)
            while self.current_token.type == TokenType.COMMA:
                self.advance() # sarim peste virgula
                params.append(self.expect(TokenType.IDENTIFIER).value)
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.COLON)
        while self.current_token.type == TokenType.NEWLINE:
            self.advance()
        body = self.statement()
        if not isinstance(body, list):
            body = [body]
        return FunctionDef(name, params, body)
    def parse_return(self):
        self.expect(TokenType.RETURN)
        expr = self.parse_expression()
        return Return(expr)

    
        
    
