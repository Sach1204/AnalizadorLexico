
# Analizador Léxico para Python

## Proyecto desarrolado por:

**Samuel Chaves Mora**

**Cristian Bello Cuesta**

Este proyecto consiste en el desarrollo de un analizador léxico en Python, basado en la construcción de autómatas finitos deterministas (AFD). El analizador tiene como finalidad identificar y clasificar los componentes léxicos de cadenas de entrada, determinando si cumplen con las reglas establecidas para el lenguaje definido.

## Características Principales

- **Procesamiento parcial**: Muestra todos los tokens válidos procesados antes de un error léxico
- **Manejo de errores mejorado**: Utiliza excepciones para control de flujo
- **Principio de subcadena más larga**: Reconoce operadores compuestos correctamente
- **Detección de números consecutivos**: Previene errores de parsing
- **Manejo completo de comentarios y espacios en blanco**

## 1. Encabezado e Imports

```python
import sys
```

Se usa para manejar los **argumentos de línea de comandos** (`sys.argv`) y terminar el programa en caso de error con `sys.exit(1)`.

## 2. Configuración de Tablas

### Palabras Reservadas (`KEYWORDS`)
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
Lista ordenada por longitud descendente que garantiza la detección del símbolo más largo primero (ejemplo: `>=` antes que `>`).

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

## 3. Manejo de Errores

### Clase de Excepción Personalizada
```python
class ErrorLexico(Exception):
    def __init__(self, linea, posicion):
        self.linea = linea
        self.posicion = posicion
```

Esta clase permite capturar errores léxicos sin detener inmediatamente el procesamiento, permitiendo mostrar tokens válidos antes del error.

## 4. Funciones Auxiliares

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
```

- `es_letra(c)`: Determina si un carácter puede iniciar un identificador (letra o `_`)
- `es_digito(c)`: Determina si un carácter es un dígito
- `es_alfanumerico(c)`: Combina letra o dígito para identificadores

## 5. Clase `AnalizadorLexico`

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
        self.ultimo_token_fue_numero = False
```

### Atributos Principales

- `texto`: Código fuente completo
- `posicion`, `linea`, `columna`: Control de ubicación actual
- `tokens`: Lista de tokens reconocidos
- `ultimo_token_fue_numero`: Previene números consecutivos sin operadores

### Métodos de Navegación

```python
def caracter_actual(self):
    """Obtiene el carácter en la posición actual"""

def mirar_adelante(self, offset=1):
    """Mira un carácter adelante sin avanzar posición"""

def avanzar(self):
    """Avanza una posición actualizando línea y columna"""
```

### Procesamiento de Elementos Especiales

#### Espacios y Comentarios
```python
def saltar_espacios_y_tabs(self):
    """Salta espacios y tabulaciones (no saltos de línea)"""

def procesar_comentario(self):
    """Procesa comentarios que inician con #"""
```

#### Lectura de Cadenas
```python
def leer_cadena(self):
    """Lee cadenas entre comillas simples o dobles"""
```
- Maneja escapes básicos con `\`
- Detecta cadenas sin cerrar
- Preserva las comillas en el lexema

#### Lectura de Números
```python
def leer_numero(self):
    """Lee números enteros con signo opcional"""
```
- Maneja signos pegados (`-42`, `+15`)
- Detecta números consecutivos como error léxico
- Distingue entre operadores y signos

#### Lectura de Identificadores
```python
def leer_identificador(self):
    """Lee identificadores y palabras reservadas"""
```
- Distingue entre palabras reservadas e identificadores
- Debe empezar con letra o `_`
- Puede contener letras, dígitos y `_`

#### Lectura de Operadores
```python
def leer_operador(self):
    """Lee operadores y símbolos aplicando subcadena más larga"""

def coincide_en_posicion(self, simbolo):
    """Verifica si el símbolo coincide en la posición actual"""
```
- Aplica el principio de subcadena más larga
- Reconoce operadores compuestos correctamente

### Análisis Principal

```python
def obtener_siguiente_token(self):
    """Obtiene el siguiente token del código fuente"""

def analizar(self):
    """Realiza el análisis léxico completo con manejo de errores"""
```

El método `analizar()` incluye manejo de excepciones que permite:
1. Procesar todos los tokens válidos
2. Mostrar tokens procesados antes del error
3. Reportar el error léxico en el formato especificado
4. Terminar la ejecución

## 6. Funciones de Salida

```python
def imprimir_tokens(tokens):
    """Imprime tokens según formato especificado"""
```

Formatea la salida según las especificaciones:
- **Palabras reservadas**: `<palabra,fila,columna>`
- **Identificadores**: `<id,lexema,fila,columna>`
- **Números**: `<tk_entero,lexema,fila,columna>`
- **Cadenas**: `<tk_cadena,lexema,fila,columna>`
- **Operadores y símbolos**: `<nombre_token,fila,columna>`

## 7. Programa Principal

```python
def main():
    """Función principal del analizador léxico"""
```

Maneja:
- Verificación de argumentos de línea de comandos
- Lectura del archivo fuente
- Creación del analizador léxico
- Procesamiento del código y muestra de tokens

## Uso del Programa

### Ejecución
```bash
python analizadorlexico.py archivo.py
```

### Ejemplo de Entrada y Salida 

**Ejemplo 1**
```txt
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

**Muestra de como sale en terminal**

<img width="1660" height="342" alt="image" src="https://github.com/user-attachments/assets/d1172f0d-a985-4361-96d5-81362ed555d3" />

**Ejemplo 2**

```txt
2.5598055while3!=88¬56.a
```
**Muestra de comos sale en terminal**

<img width="1660" height="182" alt="image" src="https://github.com/user-attachments/assets/069c2d11-554b-4717-8efe-213f399c81c7" />

**Ejemplo 3**

```txt
# Casos específicos basados en las notas del analizador léxico
# CASO 1: Número decimal 90.00.50 
# Debe generar: tk_entero(90), tk_punto, tk_entero(00), tk_punto, tk_entero(50)
valor = 90.00.50
# CASO 2: Error léxico con 1-23948998
# Debe detectar tk_entero(1) y luego ERROR en el guión (no pegado al número)
numero_problema = 123948998
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

**Mustra de como sale en terminal**
<img width="1660" height="965" alt="image" src="https://github.com/user-attachments/assets/977e2e5d-6069-4ef7-afb0-ce065dad72bf" />

**Ejemplo 4**

```python
#
```
**Muestra de como sale en terminal**
<img width="1660" height="61" alt="image" src="https://github.com/user-attachments/assets/68c38437-046e-4b2e-9f5f-ccdf5e397ce0" />




