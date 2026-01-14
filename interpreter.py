from nodes import *
from errors import RuntimeError
from envi import Environment
class ReturnException(Exception):
    def __init__(self, value):
        self.value = value
class Function:
    def __init__(self, name, params, body, closure):
        self.name = name
        self.params = params
        self.body = body
        self.closure = closure 

    def __repr__(self):
        return f"<function {self.name}>"
class Interpreter:
    def __init__(self):
        #retinem variabilele in memoria programului
        #ex 'x' : 11 
        self.global_env = Environment()
        self.env = self.global_env 
    def interpret(self,statements):
        """ primeste o lista de instructiuni si le executa pe rand"""
        if not statements:
            return
        for stmt in statements:
            self.execute(stmt)
    def visit_While(self, node):
        while self.evaluate(node.condition):
        # Verificam daca corpul buclei este o lista de instructiuni (bloc)
            if isinstance(node.body, list):
                for statement in node.body:
                    self.execute(statement)
        # Daca este o singura instructiune (nu e lista)
            else:
             self.execute(node.body)
    def visit_For(self,node):
        start=self.evaluate(node.start_value)
        end=self.evaluate(node.end_value)
        if not isinstance(start, (int, float)):
            raise RuntimeError(f"Valoarea de start a FOR trebuie sa fie numar, nu {type(start).__name__}")
        if not isinstance(end, (int, float)):
            raise RuntimeError(f"Valoarea de final a FOR trebuie sa fie numar, nu {type(end).__name__}")
        
        self.env.define(node.var_name, start)
        current_val = self.env.get(node.var_name)
        while current_val <= end:
            if isinstance(node.body, list):
                for stmt in node.body:
                    self.execute(stmt)
            else:
                self.execute(node.body)
            current_val = self.env.get(node.var_name)
            self.env.define(node.var_name, current_val + 1)
            current_val = self.env.get(node.var_name)
    
    def execute(self, stmt):
        """Executa o instructiune"""
        if isinstance(stmt, Print):
            value = self.evaluate(stmt.expr)
            print(value)
            
        elif isinstance(stmt, Assign):
            value = self.evaluate(stmt.expr)
            # Folosim define pentru a crea/actualiza variabila in scope-ul curent
            self.env.define(stmt.name, value)
            
        elif isinstance(stmt, If):
            cond_value = self.evaluate(stmt.condition)
            if cond_value:
                for s in stmt.then_branch:
                    self.execute(s)
            elif stmt.else_branch:
                for s in stmt.else_branch:
                    self.execute(s)
                    
        elif isinstance(stmt, While):
            while self.evaluate(stmt.condition):
                if isinstance(stmt.body, list):
                    for s in stmt.body:
                        self.execute(s)
                else:
                    self.execute(stmt.body)
        
        elif isinstance(stmt, Call):
            self.evaluate(stmt)

        elif isinstance(stmt, FunctionDef):
            func_obj = Function(stmt.name, stmt.params, stmt.body, self.env)
            self.env.define(stmt.name, func_obj)
        elif isinstance(stmt, Return):
            value = None
            if stmt.expr:
                value = self.evaluate(stmt.expr)
            raise ReturnException(value)
        
        elif isinstance(stmt, For):
            self.visit_For(stmt)

        else: 
            if isinstance(stmt, list):  # Pentru blocuri de cod
                for s in stmt:
                    self.execute(s)
                return
            raise RuntimeError(f"Instructiune necunoscuta la executie: {type(stmt).__name__}")
           
    def evaluate(self,expr):
        """Evalueaza o expresie si returneaza rezultatul"""   
        if isinstance(expr,Number):
            return expr.value
        elif isinstance(expr,String):
            return expr.value
        elif isinstance(expr, ListNode):
            return [self.evaluate(element) for element in expr.elements]
        elif isinstance(expr, GetItem):
            if isinstance(expr.var_node, Variable):
               list_val = self.env.get(expr.var_node.name)
            else:
                list_val = self.evaluate(expr.var_node)

            if not isinstance(list_val, list):
                raise RuntimeError(f"Nu poti indexa ceva ce nu este lista: {type(list_val).__name__}")
            index = self.evaluate(expr.index_node)
            if not isinstance(index, int):
                raise RuntimeError(f"Indexul trebuie sa fie un nr intreg, nu {type(index).__name__}")
            try:
                return list_val[index]
            except IndexError:
                raise RuntimeError(f"Index in afara limitelor: {index} (lungime lista: {len(list_val)})")
        elif isinstance(expr, Call):
             return self.call_function(expr)
        elif isinstance(expr,Variable):
            try:
                return self.env.get(expr.name)
            except Exception: # Prindem eroarea din envi.py
                 raise RuntimeError(f"Variabila '{expr.name}' nu este definita")
        if isinstance(expr, Len):
            val = self.evaluate(expr.expr)
            if isinstance(val, (str, list)):
                return len(val)
            raise RuntimeError(f"Functia LEN merge doar pe liste sau stringuri, nu pe {type(val).__name__}")

        if isinstance(expr, Input):
            return input() # Folosim input() din Python

        if isinstance(expr, ToInt):
            val = self.evaluate(expr.expr)
            try:
                return int(val)
            except ValueError:
                raise RuntimeError(f"Nu pot converti '{val}' la numar intreg")

        if isinstance(expr, ToStr):
            val = self.evaluate(expr.expr)
            return str(val)
        elif isinstance(expr, BinOp):
            left = self.evaluate(expr.left)
            right = self.evaluate(expr.right)
            if expr.op == '+':
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                    raise RuntimeError(f"Operatorul '+' necesita numere, am primit {type(left).__name__} si {type(right).__name__}")
                return left + right
            elif expr.op == '-':
                if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                    raise RuntimeError(f"Operatorul '-' necesita numere, am primit {type(left).__name__} si {type(right).__name__}")
                return left - right
            elif expr.op == '*':
                if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                    raise RuntimeError(f"Operatorul '*' necesita numere, am primit {type(left).__name__} si {type(right).__name__}")
                return left * right
            elif expr.op == '/':
                if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                    raise RuntimeError(f"Operatorul '/' necesita numere, am primit {type(left).__name__} si {type(right).__name__}")
                if right == 0:
                    raise RuntimeError("Eroare: Impartire la 0")
                return left / right
            elif expr.op == '%': 
                return left % right
            elif expr.op == 'AND': 
                return left and right
            elif expr.op == 'OR': 
                return left or right
            elif expr.op == '<': 
                return left < right
            elif expr.op == '>': 
                return left > right
            elif expr.op == '==': 
                return left == right
            elif expr.op == '<=': 
                return left <= right
            elif expr.op == '>=': 
                return left >= right
            elif expr.op == '!=': 
                return left != right
            else:
                raise RuntimeError(f"Operator necunoscut: {expr.op}")
        raise RuntimeError(f"Expresie necunoscuta: {type(expr).__name__}")
    def call_function(self, node):
        """Apeleaza o functie (definita de utilizator)"""
        try:
            func_obj = self.env.get(node.name)
        except Exception:
            raise RuntimeError(f"Functie nedefinita: '{node.name}'")
        if not isinstance(func_obj, Function):
            raise RuntimeError(f"Eroare Apel: '{node.name}' nu este o functie, este '{type(func_obj).__name__}'.")
        if len(node.args) != len(func_obj.params):
            raise RuntimeError(
                f"Argument Error: Functia '{func_obj.name}' cere {len(func_obj.params)} argumente, "
                f"dar a primit {len(node.args)}."
            )
        arg_values = [self.evaluate(arg) for arg in node.args]
        previous_env = self.env
        new_env = Environment(parent=func_obj.closure)
        for i, param in enumerate(func_obj.params):
            new_env.define(param, arg_values[i])
            
        self.env = new_env
        result = None
        try:
            if isinstance(func_obj.body, list):
                for stmt in func_obj.body:
                    self.execute(stmt)
            else:
                self.execute(func_obj.body)
        except ReturnException as e:
            result = e.value
        finally:
            self.env = previous_env      
        return result
