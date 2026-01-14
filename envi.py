class Environment:
    def __init__(self, parent=None):
        self.vars = {}  # Dictionar pentru variabile
        self.parent = parent  # Referinta la mediul parinte
    
    def define(self, name, value):
        self.vars[name] = value
    
    def get(self, name):
        """
        Obtine valoarea unei variabile.
        Cauta mai intai in scope-ul curent, apoi in parinti.
        
        Args:
            name: Numele variabilei
            
        Returns:
            Valoarea variabilei
            
        Raises:
            NameError: Daca variabila nu exista
        """
        if name in self.vars:
            return self.vars[name]
        
        if self.parent is not None:
            return self.parent.get(name)
        
        raise NameError(f"Variabila '{name}' nu este definita")
    
    def set(self, name, value):
        """
        Args:
            name: Numele variabilei
            value: Noua valoare
        Raises:
            NameError: Daca variabila nu exista
        """
        if name in self.vars:
            self.vars[name] = value
            return
        if self.parent is not None:
            self.parent.set(name, value)
            return
        raise NameError(f"Variabila '{name}' nu este definita")
    def exists(self, name):
        """
        Verifica daca o variabila exista in acest scope sau in parinti
        Args:
            name: Numele variabilei
        Returns:
            True daca exista, False altfel
        """
        if name in self.vars:
            return True
        
        if self.parent is not None:
            return self.parent.exists(name)
        return False
    def __repr__(self):
        """Reprezentare string pentru debugging"""
        return f"Environment(vars={list(self.vars.keys())}, has_parent={self.parent is not None})"
class FunctionEnvironment(Environment):

    def __init__(self, parent=None, global_env=None):
        super().__init__(parent)
        self.global_env = global_env
    def get_function(self, name):
        """
        Cauta o functie in mediul global
        Args:
            name: Numele functiei
        Returns:
            Definitia functiei
        Raises:
            NameError: Daca functia nu exista
        """
        if self.global_env and hasattr(self.global_env, 'functions'):
            if name in self.global_env.functions:
                return self.global_env.functions[name]
        raise NameError(f"Functia '{name}' nu este definita")