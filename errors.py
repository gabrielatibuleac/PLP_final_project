class Error(Exception):
    """Clasa de baza pentru toate erorile din limbaj"""
    def __init__(self, error_name, details, line=None, column=None):
        self.error_name = error_name
        self.details = details
        self.line = line
        self.column = column
        super().__init__(self.as_string())
    
    def as_string(self):
        """Returneaza mesajul de eroare formatat"""
        RED = '\033[91m'
        RESET = '\033[0m'
        location = ""
        if self.line is not None:
            location = f" [Linia {self.line}"
            if self.column is not None:
                location += f", Coloana {self.column}"
            location += "]"
        return f"{RED}{self.error_name}{location}: {self.details}{RESET}"


class IllegalCharError(Error):
    """Eroare pentru caractere ilegale in cod"""
    def __init__(self, details, line=None, column=None):
        super().__init__('Caracter Ilegal', details, line, column)


class InvalidSyntaxError(Error):
    """Eroare de sintaxa in parsing"""
    def __init__(self, details='', line=None, column=None):
        super().__init__('Eroare de sintaxa', details, line, column)


class RuntimeError(Error):
    """Eroare in timpul executiei programului"""
    def __init__(self, details, line=None, column=None):
        super().__init__('Eroare Runtime', details, line, column)


class TypeError(Error):
    """Eroare de tip (type mismatch)"""
    def __init__(self, details, line=None, column=None):
        super().__init__('Eroare de Tip', details, line, column)


class NameError(Error):
    """Eroare pentru variabile/functii nedefinite"""
    def __init__(self, details, line=None, column=None):
        super().__init__('Eroare de Nume', details, line, column)


class IndexError(Error):
    """Eroare pentru indexare in afara limitelor"""
    def __init__(self, details, line=None, column=None):
        super().__init__('Eroare de Index', details, line, column)