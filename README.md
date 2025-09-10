# AnalizadorLexico

Este proyecto consiste en el desarrollo de un analizador léxico en Python, basado en la construcción de autómatas finitos deterministas (AFD). El analizador tiene como finalidad identificar y clasificar los componentes léxicos de cadenas de entrada, determinando si cumplen con las reglas establecidas para el lenguaje definido.

Para la validación de su funcionamiento se implementaron cinco casos de prueba, que abarcan tanto ejemplos correctos como incorrectos. Estos resultados permiten comprobar el correcto reconocimiento de los tokens, así como evidenciar los escenarios en los que la cadena no es aceptada por el autómata.

El Proyecto fue elaborado por:

**Samuel Chaves Mora**
**Cristian leonardo Bello Cuesta**

## 1. Encabezado e imports

```python
import sys
```

• Se usa para manejar los **argumentos de línea de comandos** (`sys.argv`) y terminar el programa en caso de error con `sys.exit(1)`.

## 2. Configuración de Tablas

• **Palabras reservadas** (`KEYWORDS`)  
  Contiene las palabras clave que el analizador reconocerá como tokens de tipo `KEYWORD`.

• **Símbolos** (`SYMBOLS`)  
  Es una lista ordenada por longitud descendente. Esto garantiza que se detecte primero el símbolo más largo (ejemplo: `>=` antes que `>`).  
  Cada símbolo está asociado a un nombre de token como `tk_suma`, `tk_asig`, etc.

## 3. Funciones Auxiliares

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

**Atributos principales**

• `texto`: código fuente completo.

• `posicion`, `linea`, `columna`: controlan la ubicación actual en el texto.

• `tokens`: lista de tokens reconocidos.

• `ultimo_token_fue_numero`: evita que dos números aparezcan consecutivos sin un operador entre ellos.
