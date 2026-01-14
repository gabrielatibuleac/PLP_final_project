from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from errors import Error
import sys
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREY = '\033[90m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
def print_category(name):
    """Afiseaza un header pentru categorii"""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}>>> {name.upper()} <<<{Colors.RESET}")
    print(f"{Colors.GREY}{'-' * 40}{Colors.RESET}")
def run_test(description, code, should_fail=False):
    """Helper pentru a rula teste cu formatare vizuala"""

    print(f"\n{Colors.BOLD}{Colors.CYAN}[TEST] {description}{Colors.RESET}")

    print(f"{Colors.GREY}   Cod:{Colors.RESET}")
    for line in code.strip().split('\n'):
        print(f"{Colors.GREY}     | {line.strip()}{Colors.RESET}")
    print(f"   {Colors.BOLD}Output:{Colors.RESET}", end=" ")
    
    try:
        sys.stdout.flush() 
        
        lex = Lexer(code)
        tokens = lex.tokenize()
        pars = Parser(tokens)
        ast = pars.parse()
        inter = Interpreter()

        inter.interpret(ast) 

        if should_fail:
            print(f"\n   {Colors.BOLD}{Colors.RED} FAILED:{Colors.RESET} Codul ar fi trebuit sa dea eroare!")
        else:
            print(f"\n   {Colors.BOLD}{Colors.GREEN} SUCCESS{Colors.RESET}")
    
    except Error as e:
        if should_fail:
            print(f"\n   {Colors.BOLD}{Colors.GREEN} SUCCESS (Eroare Asteptata):{Colors.RESET} {e.as_string()}")
        else:
            print(f"\n   {Colors.BOLD}{Colors.RED} FAILED:{Colors.RESET} {e.as_string()}")
    
    except Exception as e:
        print(f"\n   {Colors.BOLD}{Colors.RED} UNEXPECTED ERROR:{Colors.RESET} {e}")
print_category("Sintaxa de baza si Operatii")

run_test(
    "1. Concatenare string + numar",
    'x = "Rezultat: " + 10\nPRINT(x)'
)

run_test(
    "2. Operatii aritmetice cu validare de tip",
    "a = 10 b = 5 c = a + b * 2 PRINT(c)"
)


print_category("Control Flow (If, Loops)")

run_test(
    "3. If-else statement",
    """
    x = 10
    if x > 5:
        PRINT(100)
    else:
        PRINT(0)
    """
)

run_test(
    "4. FOR loop simplu",
    "for i = 1 to 5:\n    PRINT(i)"
)

run_test(
    "5. While loop cu bloc BEGIN/END",
    """
    i = 0
    while i < 3: BEGIN
        PRINT(i)
        i = i + 1
    END
    """
)


print_category("Structuri de Date (Liste)")

run_test(
    "6. Liste si indexare",
    "x = [10, 20, 30]\nPRINT(x[0])\nPRINT(x[1])\nPRINT(x[2])"
)


print_category("Functii si Recursivitate")

run_test(
    "7. Definire si apel functie",
    "def suma(a, b):\n    return a + b\nrezultat = suma(5, 3)\nPRINT(rezultat)"
)

run_test(
    "8. Recursivitate - factorial",
    """
    def factorial(n): BEGIN
        if n <= 1: 
            return 1
        else: 
            return n * factorial(n - 1)
    END
    PRINT(factorial(5))
    """
)


print_category("Functii Native (Built-ins)")

run_test(
    "9. Built-in: LEN() function",
    """
    lista = [10, 20, 30, 40]
    txt = "Hello World"
    PRINT(LEN(lista))
    PRINT(LEN(txt))
    """
)

run_test(
    "10. Built-in: TO_STR() casting",
    """
    varsta = 25
    mesaj = "Am varsta de " + TO_STR(varsta) + " ani."
    PRINT(mesaj)
    """
)

run_test(
    "11. Built-in: TO_INT() casting",
    """
    numar_txt = "100"
    calcul = TO_INT(numar_txt) + 50
    PRINT(calcul)
    """
)


print_category("Algoritmi Complecsi")

run_test(
    "12. Algoritm: Fibonacci Iterativ",
    """
    n = 10
    a = 0
    b = 1
    i = 0
    
    PRINT("Primele 10 nr Fibonacci:")
    
    while i < n: BEGIN
        PRINT(a)
        temp = a + b
        a = b
        b = temp
        i = i + 1
    END
    """
)

run_test(
    "13. Algoritm: Suma elementelor din lista",
    """
    def suma_lista(lst): BEGIN
        total = 0
        i = 0
        lungime = LEN(lst)
        
        while i < lungime: BEGIN
            # Accesam elementul de la indexul i
            valoare = lst[i]
            total = total + valoare
            i = i + 1
        END
        
        return total
    END

    numere = [10, 20, 30, 40, 50]
    rezultat = suma_lista(numere)
    
    PRINT("Lista este: [10, 20, 30, 40, 50]")
    PRINT("Suma calculata:")
    PRINT(rezultat)
    """
)

run_test(
    "14. Algoritm: Verificare Numar Prim",
    """
    def este_prim(n): BEGIN
        if n < 2:
            return 0  # False
        
        d = 2
        # Verificam pana la n/2 (aproximativ)
        while d * d <= n: BEGIN
            rest = n % d
            if rest == 0:
                return 0 # Am gasit divizor
            d = d + 1
        END
        
        return 1 # E prim
    END

    x = 17
    y = 20
    
    if este_prim(x) == 1:
        PRINT(TO_STR(x) + " este PRIM")
    else:
        PRINT(TO_STR(x) + " NU este prim")
        
    if este_prim(y) == 1:
        PRINT(TO_STR(y) + " este PRIM")
    else:
        PRINT(TO_STR(y) + " NU este prim")
    """
)


print_category("Teste de Eroare (Negative Testing)")

run_test(
    "15. Type error: impartire string",
    'x = "text" / 5\nPRINT(x)',
    should_fail=True
)

run_test(
    "16. Runtime error: impartire la 0",
    "x = 10 / 0\nPRINT(x)",
    should_fail=True
)

run_test(
    "17. Runtime error: index lista invalid",
    "lista = [1, 2, 3]\nPRINT(lista[10])",
    should_fail=True
)

run_test(
    "18. Runtime error: variabila nedefinita",
    "PRINT(variabila_inexistenta)",
    should_fail=True
)

run_test(
    "19. Runtime error: functie nedefinita",
    "rezultat = functie_inexistenta(5)\nPRINT(rezultat)",
    should_fail=True
)

run_test(
    "20. Runtime error: numar gresit de argumente",
    "def suma(a, b):\n    return a + b\nrezultat = suma(5)\nPRINT(rezultat)",
    should_fail=True
)

run_test(
    "21. Lexer error: caracter ilegal (@)",
    "x = 5 @ 3\nPRINT(x)",
    should_fail=True
)

run_test(
    "22. FOR cu valoare non-numerica",
    'for i = "start" to "end":\n    PRINT(i)',
    should_fail=True
)

run_test(
    "23. Eroare: LEN() pe integer",
    "x = LEN(12345) PRINT(x)",
    should_fail=True
)


print_category("Advanced Features ")

run_test(
    "26. Higher-Order Functions & Closures",
    """
    # 1. Functie care returneaza o alta functie (Closure)
    def make_adder(x): BEGIN
        def inner(y):
            return x + y
        return inner
    END

    add_10 = make_adder(10)
    res1 = add_10(5)
    PRINT("Rezultat Closure (10+5):")
    PRINT(res1)

    # 2. Functie transmisa ca parametru
    def apply_func(f, val):
        return f(val)

    def square(n):
        return n * n

    res2 = apply_func(square, 6)
    PRINT("Rezultat Parametru (6*6):")
    PRINT(res2)
    """
)


print_category("INTERACTIVITATE (INPUT)")

# TEST 25: INPUT() Interactiv
print(f"\n{Colors.BOLD}{Colors.CYAN}[TEST] 25. INPUT() Interactiv{Colors.RESET}")
print(f"{Colors.YELLOW}   >>> ATENTIE: Introdu valori de la tastatura cand ti se cere! <<<{Colors.RESET}")

cod_input = """
    PRINT("Scrie numele tau:")
    nume = INPUT()
    PRINT("Salut " + nume + "!")
    
    PRINT("Scrie anul nasterii:")
    an_str = INPUT()
    an = TO_INT(an_str)
    varsta = 2025 - an
    PRINT("Ai aproximativ " + TO_STR(varsta) + " ani.")
"""

try:
    print(f"{Colors.GREY}   Cod:{Colors.RESET}")
    for line in cod_input.strip().split('\n'):
        print(f"{Colors.GREY}     | {line.strip()}{Colors.RESET}")
    print(f"   {Colors.BOLD}Output:{Colors.RESET}")
    
    lex = Lexer(cod_input)
    tokens = lex.tokenize()
    pars = Parser(tokens)
    ast = pars.parse()
    inter = Interpreter()
    inter.interpret(ast)
    print(f"\n   {Colors.BOLD}{Colors.GREEN} SUCCESS{Colors.RESET}")

except Exception as e:
    print(f"\n   {Colors.BOLD}{Colors.RED} FAILED:{Colors.RESET} {e}")

print(f"\n{Colors.BOLD}{Colors.GREEN}>>> TOATE TESTELE AU FOST EXECUTATE! <<<{Colors.RESET}\n")