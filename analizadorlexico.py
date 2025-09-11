import sys

# Palabras reservadas de Python según especificaciones
KEYWORDS = {
    "False", "None", "True", "__init__", "and", "as", "assert", "break", 
    "class", "continue", "def", "del", "elif", "else", "except", "finally", 
    "for", "from", "global", "if", "import", "in", "is", "lambda", "nonlocal", 
    "not", "or", "pass", "raise", "return", "try", "while", "with", "yield",
    "print", "bool", "int", "float", "str", "list", "dict", "tuple", "set",
    "object", "self"
}

# Operadores y símbolos especiales (ordenados por longitud descendente)
SYMBOLS = [
    # Operadores de dos caracteres (más largos primero)
    ("!=", "tk_distinto"),
    ("==", "tk_igual"), 
    ("<=", "tk_menor_igual"),
    (">=", "tk_mayor_igual"),
    ("+=", "tk_mas_igual"),
    ("-=", "tk_menos_igual"),
    ("*=", "tk_por_igual"),
    ("/=", "tk_div_igual"),
    ("//", "tk_div_entera"),
    ("**", "tk_pot"),
    ("->", "tk_ejecuta"),
    
    # Operadores de un carácter
    ("+", "tk_suma"),
    ("-", "tk_resta"),
    ("*", "tk_mult"),
    ("/", "tk_div"),
    ("%", "tk_mod"),
    ("=", "tk_asig"),
    ("<", "tk_menor"),
    (">", "tk_mayor"),
    
    # Delimitadores
    ("(", "tk_par_izq"),
    (")", "tk_par_der"),
    ("[", "tk_cor_izq"),
    ("]", "tk_cor_der"),
    ("{", "tk_llave_izq"),
    ("}", "tk_llave_der"),
    
    # Puntuación
    (",", "tk_coma"),
    (":", "tk_dos_puntos"),
    (";", "tk_punto_y_coma"),
    (".", "tk_punto"),
    
    # Otros símbolos
    ("@", "tk_arroba"),
    ("&", "tk_and_bit"),
    ("|", "tk_or_bit"),
    ("^", "tk_xor"),
    ("~", "tk_not_bit"),
    ("?", "tk_interrogacion")
]

# Clase para manejar errores léxicos
class ErrorLexico(Exception):
    def __init__(self, linea, posicion):
        self.linea = linea
        self.posicion = posicion
        super().__init__(f"Error léxico en línea {linea}, posición {posicion}")

# Funciones auxiliares

def es_letra(c):
    """Verifica si un carácter es una letra o guión bajo"""
    return c.isalpha() or c == '_'

def es_digito(c):
    """Verifica si un carácter es un dígito"""
    return c.isdigit()

def es_alfanumerico(c):
    """Verifica si un carácter es alfanumérico o guión bajo"""
    return es_letra(c) or es_digito(c)

# Analizador Léxico
class AnalizadorLexico:
    def __init__(self, texto):
        self.texto = texto
        self.longitud = len(texto)
        self.posicion = 0
        self.linea = 1
        self.columna = 1
        self.tokens = []
        self.ultimo_token_fue_numero = False  # Para detectar números consecutivos
    
    def caracter_actual(self):
        """Obtiene el carácter en la posición actual"""
        if self.posicion >= self.longitud:
            return None
        return self.texto[self.posicion]
    
    def mirar_adelante(self, offset=1):
        """Mira un carácter adelante sin avanzar posición"""
        pos = self.posicion + offset
        if pos >= self.longitud:
            return None
        return self.texto[pos]
    
    def avanzar(self):
        """Avanza una posición actualizando línea y columna"""
        if self.posicion < self.longitud:
            if self.texto[self.posicion] == '\n':
                self.linea += 1
                self.columna = 1
            else:
                self.columna += 1
            self.posicion += 1
    
    def saltar_espacios_y_tabs(self):
        """Salta espacios y tabulaciones (no saltos de línea)"""
        while self.caracter_actual() and self.caracter_actual() in ' \t':
            self.avanzar()
    
    def procesar_comentario(self):
        """Procesa comentarios que inician con #"""
        if self.caracter_actual() == '#':
            while self.caracter_actual() and self.caracter_actual() != '\n':
                self.avanzar()
            return True
        return False
    
    def leer_cadena(self):
        """Lee cadenas entre comillas simples o dobles"""
        linea_inicio = self.linea
        col_inicio = self.columna
        
        comilla = self.caracter_actual()  # ' o "
        lexema = comilla
        self.avanzar()
        
        while self.caracter_actual():
            char = self.caracter_actual()
            
            if char == '\n':
                raise ErrorLexico(linea_inicio, col_inicio)
            
            lexema += char
            
            if char == comilla:
                self.avanzar()
                return ('tk_cadena', lexema, linea_inicio, col_inicio)
            
            # Manejar escape básico
            if char == '\\' and self.mirar_adelante():
                self.avanzar()
                if self.caracter_actual():
                    lexema += self.caracter_actual()
                    self.avanzar()
                continue
            
            self.avanzar()
        
        # Cadena sin cerrar
        raise ErrorLexico(linea_inicio, col_inicio)
    
    def leer_numero(self):
        """Lee números enteros con signo opcional"""
        linea_inicio = self.linea
        col_inicio = self.columna
        
        lexema = ""
        
        # Verificar signo solo si está pegado al número Y no hay un número previo
        if self.caracter_actual() in '+-':
            siguiente = self.mirar_adelante()
            if siguiente and es_digito(siguiente):
                # Si el último token fue un número, esto indica un error léxico
                if self.ultimo_token_fue_numero:
                    raise ErrorLexico(self.linea, self.columna)
                lexema += self.caracter_actual()
                self.avanzar()
            else:
                # No es parte del número
                return None
        
        # Debe haber al menos un dígito después del posible signo
        if not es_digito(self.caracter_actual()):
            return None
        
        # Si el último token fue un número y encontramos otro número directamente, es error
        if self.ultimo_token_fue_numero and not lexema:  # No hay signo, es número directo
            raise ErrorLexico(self.linea, self.columna)
        
        # Leer todos los dígitos
        while self.caracter_actual() and es_digito(self.caracter_actual()):
            lexema += self.caracter_actual()
            self.avanzar()
        
        return ('tk_entero', lexema, linea_inicio, col_inicio)
    
    def leer_identificador(self):
        """Lee identificadores y palabras reservadas"""
        linea_inicio = self.linea
        col_inicio = self.columna
        
        lexema = ""
        
        # Debe empezar con letra o _
        if not es_letra(self.caracter_actual()):
            return None
        
        # Leer caracteres alfanuméricos
        while self.caracter_actual() and es_alfanumerico(self.caracter_actual()):
            lexema += self.caracter_actual()
            self.avanzar()
        
        # Verificar si es palabra reservada
        if lexema in KEYWORDS:
            return ('KEYWORD', lexema, linea_inicio, col_inicio)
        else:
            return ('id', lexema, linea_inicio, col_inicio)
    
    def leer_operador(self):
        """Lee operadores y símbolos aplicando subcadena más larga"""
        linea_inicio = self.linea
        col_inicio = self.columna
        
        # Aplicar principio de subcadena más larga
        for simbolo, token_name in SYMBOLS:
            if self.coincide_en_posicion(simbolo):
                # Avanzar por la longitud del símbolo
                for _ in range(len(simbolo)):
                    self.avanzar()
                return (token_name, simbolo, linea_inicio, col_inicio)
        
        return None
    
    def coincide_en_posicion(self, simbolo):
        """Verifica si el símbolo coincide en la posición actual"""
        for i, char in enumerate(simbolo):
            if (self.posicion + i >= self.longitud or 
                self.texto[self.posicion + i] != char):
                return False
        return True
    
    def obtener_siguiente_token(self):
        """Obtiene el siguiente token del código fuente"""
        while self.posicion < self.longitud:
            # Saltar espacios y tabs
            self.saltar_espacios_y_tabs()
            
            char = self.caracter_actual()
            if not char:
                break
            
            # Manejar saltos de línea
            if char == '\n':
                self.ultimo_token_fue_numero = False  # Reset en nueva línea
                self.avanzar()
                continue
            
            # Manejar comentarios
            if self.procesar_comentario():
                continue
            
            # Intentar leer cadena
            if char in '"\'':
                self.ultimo_token_fue_numero = False
                return self.leer_cadena()
            
            # Intentar leer número
            token_numero = self.leer_numero()
            if token_numero:
                self.ultimo_token_fue_numero = True
                return token_numero
            
            # Intentar leer identificador
            token_id = self.leer_identificador()
            if token_id:
                self.ultimo_token_fue_numero = False
                return token_id
            
            # Intentar leer operador/símbolo
            token_op = self.leer_operador()
            if token_op:
                self.ultimo_token_fue_numero = False
                return token_op
            
            # Carácter no reconocido - error léxico
            raise ErrorLexico(self.linea, self.columna)
        
        return None
    
    def analizar(self):
        """Realiza el análisis léxico completo"""
        try:
            while self.posicion < self.longitud:
                token = self.obtener_siguiente_token()
                if token:
                    self.tokens.append(token)
                else:
                    break
        except ErrorLexico as e:
            # Mostrar tokens procesados hasta el error
            imprimir_tokens(self.tokens)
            # Luego mostrar el error
            print(f">>> Error léxico(linea:{e.linea},posicion:{e.posicion})")
            sys.exit(1)
        
        return self.tokens

# Funciones de salida
def imprimir_tokens(tokens):
    """Imprime tokens según formato especificado"""
    for token in tokens:
        tipo = token[0]
        lexema = token[1] 
        linea = token[2]
        columna = token[3]
        
        if tipo == 'KEYWORD':
            # Palabras reservadas: <palabra,fila,columna>
            print(f"<{lexema},{linea},{columna}>")
        elif tipo == 'id':
            # Identificadores: <id,lexema,fila,columna>
            print(f"<id,{lexema},{linea},{columna}>")
        elif tipo == 'tk_entero':
            # Números: <tk_entero,lexema,fila,columna>
            print(f"<tk_entero,{lexema},{linea},{columna}>")
        elif tipo == 'tk_cadena':
            # Cadenas: <tk_cadena,lexema,fila,columna>
            print(f"<tk_cadena,{lexema},{linea},{columna}>")
        else:
            # Operadores y símbolos: <nombre_token,fila,columna>
            print(f"<{tipo},{linea},{columna}>")

# Programa principal
def main():
    """Función principal del analizador léxico"""
    if len(sys.argv) != 2:
        print("Uso: python analizador_lexico.py archivo.py")
        sys.exit(1)
    
    archivo_entrada = sys.argv[1]
    
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            codigo_fuente = f.read()
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{archivo_entrada}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        sys.exit(1)
    
    # Crear analizador y procesar código
    analizador = AnalizadorLexico(codigo_fuente)
    tokens = analizador.analizar()
    
    # Si llegamos aquí, no hubo errores - mostrar todos los tokens
    imprimir_tokens(tokens)

if __name__ == '__main__':
    main()
      
