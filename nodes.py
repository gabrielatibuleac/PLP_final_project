#clasa de baza
class ASTnode:
    """Orice nod din arbore """
    pass
class Expr(ASTnode):
    """Expresii 5,2+3,x"""
    pass
class Stmt(ASTnode):
    """Instructiuni x=5, print(x),if"""
    pass
#Expresii
class Number(Expr):
    def __init__(self,value):
        self.value=value
    def __repr__(self):
        return f"Number({self.value})"
class String(Expr):
    def __init__(self,value):
        self.value=value
    def __repr__(self):
        return f"String({self.value!r})"
class Variable(Expr):
    def __init__(self,name):
        self.name=name
    def __repr__(self):
        return f"Variable({self.name})"
#Operatii
class BinOp(Expr):
    """Ex: 1+2, x>10"""
    def __init__(self,left,op,right):
        self.left=left
        self.op=op
        self.right=right
    def __repr__(self):
        return f"BinOp({self.left},{self.op},{self.right})"
#Atribuiri
class Assign(Stmt):
    """Atribuire: x=5"""
    def __init__(self,name,expr):
        self.name=name #str numele variabilei 
        self.expr=expr # valoarea nod expr
    def __repr__(self):
        return f"Assign({self.name},{self.expr})"

#print
class Print(Stmt):
    """Print : print(x)"""
    def __init__(self,expr):
        self.expr=expr
    def __repr__(self):
        return f"Print({self.expr})"

class If(Stmt):
    """
    If statement: 
    if condition:
        then_branch
    else:
        else_branch
    """
    def __init__(self,condition,then_branch,else_branch=None):
        self.condition=condition
        self.then_branch=then_branch #lista de instructiuni pentru adv
        self.else_branch=else_branch#lista de instructiuni pt false
    def __repr__(self):
        return f"If({self.condition},{self.then_branch},{self.else_branch})"
class While(Stmt):
    """
    While loop:
    while condition:
        body
    """
    def __init__(self,condition,body):
        self.condition=condition
        self.body =body#lista de instructiuni
    def __repr__ (self):
        return f"While({self.condition})"
class For(Stmt):
    """
    For loop:
    FOR i = 0 TO 10 DO
        ...
    """
    def __init__(self, var_name, start_value, end_value, body):
        self.var_name = var_name       # Numele variabilei (ex: 'i')
        self.start_value = start_value # Expresie start (ex: 0)
        self.end_value = end_value     # Expresie stop (ex: 10)
        self.body = body               # Lista de instructiuni
        
    def __repr__(self):
        return f"For({self.var_name}, {self.start_value} -> {self.end_value})"
class FunctionDef(Stmt):
    def __init__(self,name,params,body):
        self.name = name       # String (numele functiei)
        self.params = params   # Lista de string-uri (numele parametrilor)
        self.body = body       # Lista de instructiuni (corpul functiei)
    def __repr__(self):
        return f"Def({self.name},{self.params})"
class Call(Expr):
    def __init__(self, name, args):
        self.name = name     # Numele functiei apelate
        self.args = args     # Lista de expresii (argumentele date)
    def __repr__(self):
        return f"Call({self.name},{self.args})"
class Return(Stmt):
    def __init__(self,expr):
        self.expr=expr
    def __repr(self):
        return f"Return({self.expr})"
class ListNode(Expr):
    def __init__(self,elements):
        self.elements=elements
    def __repr__(self):
        return f"List({self.elements})"
class GetItem(Expr):
    def __init__(self,var_node,index_node):
        self.var_node=var_node
        self.index_node=index_node
    def __repr__(self):
        return f"GetItem({self.var_node},{self.index_node})"
class Len(Expr):
    def __init__(self, expr):
        self.expr = expr
    def __repr__(self):
        return f"Len({self.expr})"

class Input(Expr):
    def __init__(self):
        pass
    def __repr__(self):
        return "Input()"

class ToInt(Expr):
    def __init__(self, expr):
        self.expr = expr
    def __repr__(self):
        return f"ToInt({self.expr})"

class ToStr(Expr):
    def __init__(self, expr):
        self.expr = expr
    def __repr__(self):
        return f"ToStr({self.expr})"     
        