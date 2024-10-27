import pandas as pd
import re
from datetime import datetime

'''@uthor: José Luis García Quinayás
City: Popayán - Cauca
Date: 26/Oct/2024'''

# Ruta del archivo de datos de ventas
file_path = "O:\\documentos\\ventas.xlsx"
data = pd.read_excel(file_path)

# Definición de funciones de prueba con descripciones detalladas en español
def validate_fecha_venta(df):
    """
    Valida que la columna 'fecha_venta' tenga el formato YYYY-MM-DD.
    """
    errors = df['fecha_venta'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d', errors='coerce')).isnull().sum()
    return errors == 0, errors

def validate_id_producto(df):
    """
    Verifica que cada 'id_producto' sea único.
    """
    errors = df['id_producto'].duplicated().sum()
    return errors == 0, errors

def validate_precio(df):
    """
    Asegura que 'precio' contenga solo valores numéricos positivos mayores a cero.
    """
    errors = df['precio'].apply(lambda x: not isinstance(x, (int, float)) or x <= 0).sum()
    return errors == 0, errors

def validate_cantidad(df):
    """
    Valida que 'cantidad_vendida' tenga solo valores enteros positivos.
    """
    errors = df['cantidad_vendida'].apply(lambda x: not isinstance(x, int) or x <= 0).sum()
    return errors == 0, errors

def validate_total_venta(df):
    """
    Valida que 'total_venta' sea igual a 'precio' * 'cantidad_vendida'.
    """
    errors = (df['total_venta'] != df['precio'] * df['cantidad_vendida']).sum()
    return errors == 0, errors

# Función para verificar que 'nombre_cliente' no esté vacío
def validate_nombre_cliente(df):
    """
    Verifica que 'nombre_cliente' no esté vacío en ninguna fila.
    """
    errors = df['nombre_cliente'].isna().sum()
    return errors == 0, errors

# Función para validar que 'categoria' tiene solo valores específicos válidos
def validate_categoria(df):
    """
    Asegura que 'categoria' contiene solo las categorías válidas especificadas.
    """
    valid_categories = {'Electrónica', 'Ropa', 'Hogar', 'Juguetería'}
    errors = ~df['categoria'].isin(valid_categories).sum()
    return errors == 0, errors

# Función para asegurar que 'region' tiene solo los valores permitidos
def validate_region(df):
    """
    Verifica que 'region' contenga solo valores de la lista permitida.
    """
    allowed_regions = {'Norte', 'Sur', 'Este', 'Oeste'}
    errors = ~df['region'].isin(allowed_regions).sum()
    return errors == 0, errors

# Función para validar que 'metodo_pago' contiene solo valores válidos
def validate_metodo_pago(df):
    """
    Asegura que 'metodo_pago' contenga solo los métodos de pago válidos especificados.
    """
    valid_payment_methods = {'Efectivo', 'Tarjeta', 'Transferencia'}
    errors = ~df['metodo_pago'].isin(valid_payment_methods).sum()
    return errors == 0, errors

# Función para verificar que no haya filas duplicadas en todas las columnas
def validate_no_duplicate_rows(df):
    """
    Verifica que no existan filas duplicadas en todas las columnas.
    """
    errors = df.duplicated().sum()
    return errors == 0, errors

def validate_fecha_venta_future(df):
    """ Valida que 'fecha_venta' no está en el futuro."""
    errors = df['fecha_venta'].apply(lambda x: pd.to_datetime(str(x), errors='coerce') > pd.Timestamp.now()).sum()
    return errors == 0, errors, "La columna 'fecha_venta' no contiene fechas en el futuro."

def validate_nombre_cliente_no_numerico(df):
    """ Verifica que 'nombre_cliente' no contenga números ni caracteres especiales."""
    errors = df['nombre_cliente'].apply(lambda x: bool(re.search(r'[^a-zA-Z\s]', str(x)))).sum()
    return errors == 0, errors, "Los valores en 'nombre_cliente' solo contienen letras y espacios."

def validate_id_producto_formato(df):
    """ Verifica que 'id_producto' tenga un formato alfanumérico específico."""
    errors = df['id_producto'].apply(lambda x: not bool(re.match(r'^[a-zA-Z0-9]+$', str(x)))).sum()
    return errors == 0, errors, "El 'id_producto' es alfanumérico."

def validate_precio_rango(df, max_price=10000):
    """ Verifica que 'precio' no exceda un valor máximo razonable."""
    # Intentar convertir los valores de 'precio' a números, errores se convierten en NaN
    df['precio_numeric'] = pd.to_numeric(df['precio'], errors='coerce')
    # Contar errores donde el precio es NaN o mayor que max_price
    errors = df['precio_numeric'].isna().sum() + (df['precio_numeric'] > max_price).sum()
    # Retornar resultado con una descripción
    return errors == 0, errors, f"'precio' no excede el límite de {max_price}."

def validate_cantidad_maxima(df, max_cantidad=1000):
    """ Asegura que 'cantidad_vendida' no sea excesiva."""
    errors = df['cantidad_vendida'].apply(lambda x: x > max_cantidad).sum()
    return errors == 0, errors, f"'cantidad_vendida' es menor que {max_cantidad}."

def validate_total_venta_promedio(df, multiplier_threshold=10):
    """ Verifica que 'total_venta' no sea demasiado alto en comparación con el promedio."""
    avg_total = df['total_venta'].mean()
    errors = df['total_venta'].apply(lambda x: x > avg_total * multiplier_threshold).sum()
    return errors == 0, errors, f"'total_venta' es razonable comparado con el promedio."

def validate_nombre_producto(data):
    """
    Verifica que 'nombre_producto' no esté vacío ni sea nulo.
    Returns:
    - passed: Bool, True si todos los nombres de productos están presentes.
    - errors: Número de nombres de productos vacíos o nulos.
    """
    errors = data['nombre_producto'].isnull().sum() + data[data['nombre_producto'] == ""].shape[0]
    return errors == 0, errors

# Ejecutar todas las pruebas con descomposición flexible de resultados
def run_all_tests(df):
    """
    Ejecuta todas las funciones de prueba y almacena los resultados en una lista de diccionarios.
    """
    tests = [
        ("CP01", "Validar formato de 'fecha_venta' YYYY-MM-DD", validate_fecha_venta),
        ("CP02", "Validar unicidad de 'id_producto'", validate_id_producto),
        ("CP03", "Validar que 'precio' es un número positivo", validate_precio),
        ("CP04", "Validar que 'cantidad_vendida' es un entero positivo", validate_cantidad),
        ("CP05", "Asegura que 'total_venta' coincide con 'precio' * 'cantidad_vendida'", validate_total_venta),
        ("CP06", "Verifica que 'nombre_cliente' no esté vacío", validate_nombre_cliente),
        ("CP07", "Asegura que 'categoria' contiene solo categorías válidas", validate_categoria),
        ("CP08", "Verifica que 'region' contenga valores permitidos", validate_region),
        ("CP09", "Asegura que 'metodo_pago' contiene métodos válidos", validate_metodo_pago),
        ("CP10", "Verifica que no existan filas duplicadas", validate_no_duplicate_rows),
        ("CP11", "Validar que 'fecha_venta' no está en el futuro", validate_fecha_venta_future),
        ("CP12", "Verificar que 'nombre_cliente' no contenga números ni caracteres especiales", validate_nombre_cliente_no_numerico),
        ("CP13", "Verificar que el 'id_producto' tiene formato alfanumérico", validate_id_producto_formato),
        ("CP14", "Validar que 'precio' no excede un valor razonable", lambda df: validate_precio_rango(df, 10000)),
        ("CP15", "Validar que 'cantidad_vendida' no excede una cantidad máxima lógica", lambda df: validate_cantidad_maxima(df, 1000)),
        ("CP16", "Validar que 'cantidad_vendida' no excede una cantidad máxima lógica", lambda df: validate_cantidad_maxima(df, 10)),
        ("CP17", "Validar que 'nombre_producto' no esté vacío", validate_nombre_producto),
    ]

    results = []
    for test_id, description, test_func in tests:
        result = {
            "Test ID": test_id,
            "Descripción": description,
            "Resultado": "",
            "Descripción del Resultado": "",
            "Número de Incidencias": "",
            "Comentarios": ""
        }
        
        # Ejecuta la prueba y descompone según el número de valores devueltos
        test_output = test_func(df)
        
        if len(test_output) == 2:
            passed, errors = test_output
            result["Resultado"] = "Aprobado" if passed else "Fallido"
            result["Descripción del Resultado"] = "" if passed else f"{errors} errores encontrados"
            result["Número de Incidencias"] = errors
        elif len(test_output) == 3:
            passed, errors, message = test_output
            result["Resultado"] = "Aprobado" if passed else "Fallido"
            result["Descripción del Resultado"] = message if passed else f"{errors} errores encontrados"
            result["Número de Incidencias"] = errors
            result["Comentarios"] = message if not passed else ""
        
        results.append(result)

    return results

# Ejecutar todas las pruebas y almacenar los resultados
test_results = run_all_tests(data)

# Convertir los resultados a un DataFrame
results_df = pd.DataFrame(test_results)

# Exportar resultados a archivos Excel y CSV
results_df.to_excel("test_results.xlsx", index=False)  # exporta a archivo Excel
results_df.to_csv("test_results.csv", index=False)     # exporta a archivo CSV

print("Pruebas completadas. Resultados exportados a 'test_results.xlsx' y 'test_results.csv'.")
