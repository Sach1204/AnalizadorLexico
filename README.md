# AnalizadorLexico

Este proyecto consiste en el desarrollo de un analizador léxico en Python, basado en la construcción de autómatas finitos deterministas (AFD). El analizador tiene como finalidad identificar y clasificar los componentes léxicos de cadenas de entrada, determinando si cumplen con las reglas establecidas para el lenguaje definido.

Para la validación de su funcionamiento se implementaron cinco casos de prueba, que abarcan tanto ejemplos correctos como incorrectos. Estos resultados permiten comprobar el correcto reconocimiento de los tokens, así como evidenciar los escenarios en los que la cadena no es aceptada por el autómata.

El Proyecto fue elaborado por:

**Samuel Chaves Mora**

**Cristian leonardo Bello Cuesta**

# Analizador Léxico Python codigo explicado por secciones

## 1. Encabezado e imports

```python
import sys
```

• Se usa para manejar los **argumentos de línea de comandos** (`sys.argv`) y terminar el programa en caso de error con `sys.exit(1)`.

## 2. Configuración de Tablas

### Palabras reservadas (`KEYWORDS`)
Contiene las palabras clave que el analizador reconocerá como tokens de tipo `KEYWORD`.

```python
KEYWORDS = {
    "False", "None", "True", "__init__", "and", "as", "assert", "break", 
    "class", "continue", "def", "del", "elif", "else", "except", "finally", 
    "for", "from", "global", "if", "import", "in", "is", "lambda", "nonlocal", 
    "not", "or", "pass", "raise", "return", "try", "while", "with", "yield",
    "print", "bool", "int", "float", "str", "list", "dict", "tuple", "set",
    "object", "self"
}
```

### Símbolos (`SYMBOLS`)
Es una lista ordenada por longitud descendente. Esto garantiza que se detecte primero el símbolo más largo (ejemplo: `>=` antes que `>`).  
Cada símbolo está asociado a un nombre de token como `tk_suma`, `tk_asig`, etc.

```python
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
```

## 3. Funciones Auxiliares

```python
def es_letra(c):
    """Verifica si un carácter es una letra o guión bajo"""
    return c.isalpha() or c == '_'

def es_digito(c):
    """Verifica si un carácter es un dígito"""
    return c.isdigit()

def es_alfanumerico(c):
    """Verifica si un carácter es alfanumérico o guión bajo"""
    return es_letra(c) or es_digito(c)

def error_lexico(linea, posicion):
    """Reporta error léxico según formato especificado"""
    print(f">>> Error léxico(linea:{linea},posicion:{posicion})")
    sys.exit(1)
```

• `es_letra(s)`: determina si un carácter puede iniciar un identificador (letra o `_`).

• `es_digito(c)`: determina si un carácter es un dígito.

• `es_alfanumerico(c)`: combina letra o dígito.

• `error_lexico(linea, posicion)`: imprime un error léxico en el formato

```
>>> Error lexico(linea:X,posicion:Y)
```

y termina la ejecución.

## 4. Clase `AnalizadorLexico`

Encapsula el estado y la lógica del escaneo del código fuente.

```python
class AnalizadorLexico:
    def __init__(self, texto):
        self.texto = texto
        self.longitud = len(texto)
        self.posicion = 0
        self.linea = 1
        self.columna = 1
        self.tokens = []
        self.ultimo_token_fue_numero = False  # Para detectar números consecutivos
```

### Atributos principales

• `texto`: código fuente completo.

• `posicion`, `linea`, `columna`: controlan la ubicación actual en el texto.

• `tokens`: lista de tokens reconocidos.

• `ultimo_token_fue_numero`: evita que dos números aparezcan consecutivos sin un operador entre ellos.

### Métodos útiles

#### Navegación y control de posición

```python
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
```

• `caracter_actual()` / `mirar_adelante(offset)`: permiten localización y consumir caracteres (útil para decidir si un `=` es signo o operador).

• `avanzar()`: incrementa `posicion` y actualiza `linea` y `columna` (respeta columna +1 en salto de línea).

#### Procesamiento de espacios y comentarios

```python
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
```

• `saltar_espacios_y_tabs()`: consume espacios y tabuladores para no alterar de línea (estos se tratan aparte).

• `procesar_comentario()`: si encuentra `#`, consume hasta el final de la línea y descarta el comentario (no genera token).

#### Lectura de cadenas

```python
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
            error_lexico(linea_inicio, col_inicio)
        
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
    error_lexico(linea_inicio, col_inicio)
```

• `leer_cadena()`: lee cadenas delimitadas por `"` o `'`. Guarda la posición inicial (línea/columna) para el token o error. Maneja escapes simples: cuando ve `\`, consume el `\` y el siguiente carácter como parte de la cadena literal. Si encuentra un `\n` sin cerrar, comete a `error_lexico`.

• `devolver ("tk_cadena", lexema, linea_inicio, col_inicio)` donde `lexema` incluye las comillas y escapes tal como aparecen en el fuente.

#### Lectura de números

```python
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
                error_lexico(self.linea, self.columna)
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
        error_lexico(self.linea, self.columna)
    
    # Leer todos los dígitos
    while self.caracter_actual() and es_digito(self.caracter_actual()):
        lexema += self.caracter_actual()
        self.avanzar()
    
    return ('tk_entero', lexema, linea_inicio, col_inicio)
```

• `leer_numero()`: lee enteros con signo pegado (ej: `-34`) solo si el signo está inmediatamente junto a los dígitos. Regla: ignora signos separados. `5 + -7` está presente y el siguiente carácter no dígito, el signo se incorpora. Evita números consecutivos: si el scanner anterior fue un número y detecta otro número (o signo que empieza número) sin operador, llama a `error_lexico`.

#### Lectura de identificadores

```python
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
```

• `leer_identificador()`: si empieza con letra o `_`, consume letras/dígitos/`_` y devuelve (`"KEYWORD"`, lexema, ...) si lexema está en `KEYWORDS` o (`"ID"`, lexema, ...) si en otro caso.

#### Lectura de operadores

```python
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
```

• `leer_operador()` y `coincide_en_posicion(simbolo)`: recorre `SYMBOLS` aplicando la subcadena más larga y la considera; consume el símbolo y devuelve (`token_name`, símbolo, línea_inicial, col_inicial`).

#### Análisis principal

```python
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
        error_lexico(self.linea, self.columna)
    
    return None

def analizar(self):
    """Realiza el análisis léxico completo"""
    while self.posicion < self.longitud:
        token = self.obtener_siguiente_token()
        if token:
            self.tokens.append(token)
        else:
            break
    
    return self.tokens
```

• `obtener_siguiente_token()`: lógica central de decisión:
  1. Salta espacios/tabs.
  2. Maneja saltos de línea (resetea `ultimo_token_fue_numero`).
  3. Salta comentarios `#`.
  4. Si ve comilla: `leer_cadena()`.
  5. Intenta `leer_numero()` → si crea marca `ultimo_token_fue_numero = True`.
  6. Intenta `leer_identificador()` → si crea marca `ultimo_token_fue_numero = False`.
  7. Intenta `leer_operador()` → si crea marca `ultimo_token_fue_numero = False`.
  8. Si nada coincide → `error_lexico`.

• `analizar()`: bucle que llama repetidamente a `obtener_siguiente_token()` y va almacenando tokens hasta EOF; devuelve la lista de tokens.

## 5. Funciones de Salida

```python
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
```

Formatea la salida según las especificaciones:
- **Palabras reservadas**: `<palabra,fila,columna>`
- **Identificadores**: `<id,lexema,fila,columna>`
- **Números**: `<tk_entero,lexema,fila,columna>`
- **Cadenas**: `<tk_cadena,lexema,fila,columna>`
- **Operadores y símbolos**: `<nombre_token,fila,columna>`

## 6. Programa Principal

```python
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
    
    # Mostrar resultados
    imprimir_tokens(tokens)

if __name__ == '__main__':
    main()
```

Maneja la entrada del programa:
- Verifica argumentos de línea de comandos
- Lee el archivo fuente
- Crea el analizador léxico
- Procesa el código y muestra los tokens generados

### Salida en terminal con varios ejemplos
**Ejemplo 1**
```python
# Casos específicos basados en las notas del analizador léxico
# CASO 1: Número decimal 90.00.50 
# Debe generar: tk_entero(90), tk_punto, tk_entero(00), tk_punto, tk_entero(50)
valor = 90.00.50
# CASO 2: Error léxico con 1-23948998
# Debe detectar tk_entero(1) y luego ERROR en el guión (no pegado al número)
numero_problema = 1-23948998
# CASO 3: Palabra reservada "print"
# Debe aparecer como <print,fila,columna>
print("Mensaje de prueba")
# CASO 4: Principio de subcadena más larga
# Operadores compuestos deben reconocerse completos
# Comparaciones (subcadena más larga)
resultado1 = a == b    # tk_igual (no tk_asig + tk_asig)
resultado2 = x != y    # tk_distinto (no tk_not + tk_asig)  
resultado3 = m <= n    # tk_menor_igual (no tk_menor + tk_asig)
resultado4 = p >= q    # tk_mayor_igual (no tk_mayor + tk_asig)
# Asignaciones compuestas (subcadena más larga)
contador += 1         # tk_mas_igual (no tk_suma + tk_asig)
total -= 5           # tk_menos_igual (no tk_resta + tk_asig)
producto *= 2        # tk_por_igual (no tk_mult + tk_asig)
division /= 3        # tk_div_igual (no tk_div + tk_asig)
# División entera y potencia (subcadena más larga)
cociente = 100 // 7  # tk_div_entera (no tk_div + tk_div)
potencia = 2 ** 8    # tk_pot (no tk_mult + tk_mult)
# Números con signo pegado vs separado
negativo_pegado = -42    # tk_entero(-42)
positivo_pegado = +15    # tk_entero(+15) 
resta_normal = 10 - 5    # tk_entero(10) tk_resta tk_entero(5)
suma_normal = 20 + 3     # tk_entero(20) tk_suma tk_entero(3)
```
**Muestra de error en terminal en la linea 7**
<img width="1596" height="282" alt="image" src="https://github.com/user-attachments/assets/09a21297-fd79-4f51-884d-4c0f26fe5093" />

