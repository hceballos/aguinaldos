from decimal import Decimal, InvalidOperation
import os


import re

import re
import os

def validar_rut(nombre_archivo):
    """
    Valida si el nombre de un archivo corresponde a un RUT válido (formato chileno).
    El nombre debe ser algo como "12345678-9" o "12345678-K".
    """
    # Eliminar la extensión del archivo y asegurarse de que el nombre del archivo esté limpio
    nombre_sin_extension = os.path.splitext(nombre_archivo)[0].strip()

    # Expresión regular para validar el formato del RUT (número seguido de guion y dígito verificador)
    rut_regex = r'^\d{1,8}-[\dkK]$'
    if not re.match(rut_regex, nombre_sin_extension):
        return False

    # Separar el número del dígito verificador
    rut_numero, rut_dv = nombre_sin_extension.split('-')

    # Validar el dígito verificador
    return validar_digito_verificador(rut_numero, rut_dv)

def validar_digito_verificador(rut_numero, rut_dv):
    """
    Valida el dígito verificador de un RUT chileno.
    """
    rut_numero = int(rut_numero)
    suma = 0
    multiplicador = 2

    while rut_numero > 0:
        suma += (rut_numero % 10) * multiplicador
        rut_numero //= 10
        multiplicador = 7 if multiplicador == 2 else multiplicador - 1

    resto = 11 - (suma % 11)
    if resto == 11:
        digito_calculado = '0'
    elif resto == 10:
        digito_calculado = 'K'
    else:
        digito_calculado = str(resto)

    return rut_dv.upper() == digito_calculado


def validar_precio(precio, fila, encabezado):
    """
    Valida que el precio sea un número decimal no negativo.
    """
    errores = []
    try:
        # Intentar convertir a Decimal
        precio_decimal = Decimal(str(precio).strip())  # Convertimos a cadena y eliminamos espacios en blanco
        if precio_decimal < 0:
            errores.append(f'Error en la fila {fila}: La columna "{encabezado}" no puede tener números negativos.')
    except (InvalidOperation, ValueError, TypeError):
        errores.append(f'Error en la fila {fila}: La columna "{encabezado}" debe contener un número decimal válido.')
    
    return errores

def validar_cantidad(cantidad, fila, encabezado):
    """
    Valida que la cantidad sea un número entero no negativo.
    """
    errores = []
    try:
        # Intentar convertir a un número entero
        cantidad_int = int(cantidad)
        if cantidad_int < 0:
            errores.append(f'Error en la fila {fila}: La columna "{encabezado}" no puede tener números negativos.')
    except (ValueError, TypeError):
        errores.append(f'Error en la fila {fila}: La columna "{encabezado}" debe contener un número entero válido.')
    
    return errores

def validar_si_no(valor, fila, encabezado):
    """
    Valida que el valor sea 'SI' o 'NO' (en mayúscula o minúscula).
    """
    errores = []
    
    # Verificar si el valor es None o vacío
    if valor is None or str(valor).strip() == '':
        errores.append(f'Error en la fila {fila}: La columna "{encabezado}" no puede estar vacía.')
    else:
        # Convertir el valor a cadena, eliminar espacios y convertir a minúsculas
        valor_limpio = str(valor).strip().lower()
    
        # Comprobar si el valor es "si" o "no"
        if valor_limpio not in ["si", "no"]:
            errores.append(f'Error en la fila {fila}: La columna "{encabezado}" debe contener "SI" o "NO". Valor actual: "{valor}".')

    return errores


