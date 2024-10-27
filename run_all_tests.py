import pandas as pd
from datetime import datetime
import re

# Ruta del archivo CSV
file_path = "O:\documentos\ventas.xlsx"

# Cargar el dataset
data = pd.read_csv(file_path)
data.columns = data.columns.str.strip()

print("Columnas disponibles*********************:", data.columns)

# CP01: Validar formato YYYY-MM-DD en fecha_venta
def validate_fecha_venta(data):
    """
    Verifica que 'fecha_venta' esté en formato 'YYYY-MM-DD'.
    Returns:
    - passed: Bool, True si todas las fechas tienen el formato correcto.
    - errors: Número de fechas con formato incorrecto.
    """
    errors = 0
    for fecha in data['fecha_venta']:
        if not isinstance(fecha, str) or not fecha:
            errors += 1
        else:
            try:
                datetime.strptime(fecha, '%Y-%m-%d')
            except ValueError:
                errors += 1
    return errors == 0, errors


# CP02: Validar unicidad e integridad de id_producto
def validate_id_producto(data):
    """
    Verifica que 'id_producto' sea único y numérico.
    Returns:
    - passed: Bool, True si todos los IDs son únicos y numéricos.
    - errors: Número de IDs duplicados o no numéricos.
    """
    errors = 0
    duplicados = data['id_producto'].duplicated().sum()
    errors += duplicados
    non_digit_ids = data[~data['id_producto'].apply(lambda x: str(x).isdigit())].shape[0]
    errors += non_digit_ids
    return errors == 0, errors

# CP03: Validar que precio es no negativo
def validate_precio(data):
    """
    Verifica que 'precio' sea no negativo y numérico.
    Returns:
    - passed: Bool, True si todos los precios son numéricos y no negativos.
    - errors: Número de precios negativos o no numéricos.
    """
    data['precio'] = pd.to_numeric(data['precio'], errors='coerce')
    precios_invalidos = data[(data['precio'] < 0) | (data['precio'].isna())].shape[0]
    return precios_invalidos == 0, precios_invalidos

# CP04: Validar que cantidad es un número entero positivo
def validate_cantidad(data):
    """
    Verifica que 'cantidad' sea un número entero positivo.
    Returns:
    - passed: Bool, True si todas las cantidades son enteros positivos.
    - errors: Número de cantidades negativas o no enteras.
    """
    if 'cantidad' not in data.columns:
        print("La columna 'cantidad' no está presente en el archivo.")
        return False, None
    
    # Continuar con la validación
    data['cantidad'] = pd.to_numeric(data['cantidad'], errors='coerce')
    cantidades_invalidas = data[(data['cantidad'] < 0) | (data['cantidad'].isna()) | (data['cantidad'] % 1 != 0)].shape[0]
    return cantidades_invalidas == 0, cantidades_invalidas

# CP05: Validar que nombre_producto no esté vacío
def validate_nombre_producto(data):
    """
    Verifica que 'nombre_producto' no esté vacío.
    Returns:
    - passed: Bool, True si todos los nombres de producto tienen valor.
    - errors: Número de registros con nombre de producto vacío o nulo.
    """
    errors = data['nombre_producto'].isnull().sum() + data[data['nombre_producto'] == ""].shape[0]
    return errors == 0, errors

# CP06: Validar que id_cliente sea numérico
def validate_id_cliente(data):
    """
    Verifica que 'id_cliente' sea numérico.
    Returns:
    - passed: Bool, True si todos los IDs de cliente son numéricos.
    - errors: Número de IDs de cliente no numéricos.
    """
    errors = data[~data['id_cliente'].apply(lambda x: str(x).isdigit())].shape[0]
    return errors == 0, errors

# CP07: Validar que nombre_cliente no esté vacío
def validate_nombre_cliente(data):
    """
    Verifica que 'nombre_cliente' no esté vacío.
    Returns:
    - passed: Bool, True si todos los nombres de cliente tienen valor.
    - errors: Número de registros con nombre de cliente vacío o nulo.
    """
    errors = data['nombre_cliente'].isnull().sum() + data[data['nombre_cliente'] == ""].shape[0]
    return errors == 0, errors

# CP08: Validar que email_cliente tenga formato de email
def validate_email_cliente(data):
    """
    Verifica que 'email_cliente' esté en formato de correo electrónico.
    Returns:
    - passed: Bool, True si todos los emails tienen formato válido.
    - errors: Número de emails con formato inválido.
    """
    errors = data[~data['email_cliente'].apply(lambda x: bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', str(x))))].shape[0]
    return errors == 0, errors

# CP09: Validar que telefono_cliente tenga entre 7 y 10 dígitos
def validate_telefono_cliente(data):
    """
    Verifica que 'telefono_cliente' tenga entre 7 y 10 dígitos.
    Returns:
    - passed: Bool, True si todos los teléfonos cumplen con la longitud especificada.
    - errors: Número de teléfonos con longitud incorrecta.
    """
    errors = data[~data['telefono_cliente'].apply(lambda x: len(str(x)) in range(7, 11) and str(x).isdigit())].shape[0]
    return errors == 0, errors

# CP10: Validar que direccion_cliente no esté vacío
def validate_direccion_cliente(data):
    """
    Verifica que 'direccion_cliente' no esté vacío.
    Returns:
    - passed: Bool, True si todas las direcciones tienen valor.
    - errors: Número de direcciones vacías o nulas.
    """
    errors = data['direccion_cliente'].isnull().sum() + data[data['direccion_cliente'] == ""].shape[0]
    return errors == 0, errors

# CP11: Validar que fecha_registro sea un datetime
def validate_fecha_registro(data):
    """
    Verifica que 'fecha_registro' esté en formato 'YYYY-MM-DD'.
    Returns:
    - passed: Bool, True si todas las fechas están en formato correcto.
    - errors: Número de fechas con formato incorrecto.
    """
    errors = 0
    for fecha in data['fecha_registro']:
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
        except ValueError:
            errors += 1
    return errors == 0, errors

# CP12: Validar que total_venta = precio * cantidad
def validate_total_venta(data):
    """
    Verifica que 'total_venta' sea igual a 'precio' * 'cantidad'.
    Returns:
    - passed: Bool, True si todos los totales de venta son correctos.
    - errors: Número de registros donde el total de venta es incorrecto.
    """
    errors = data[data['total_venta'] != data['precio'] * data['cantidad']].shape[0]
    return errors == 0, errors

# Ejecución de todas las pruebas
def run_all_tests(data):
    tests = [
        ("CP01", "Validar formato de 'fecha_venta' YYYY-MM-DD", validate_fecha_venta),
        ("CP02", "Validar unicidad e integridad de 'id_producto'", validate_id_producto),
        ("CP03", "Validar que 'precio' es no negativo", validate_precio),
        ("CP04", "Validar que 'cantidad' es un número entero positivo", validate_cantidad),
        ("CP05", "Validar que 'nombre_producto' no esté vacío", validate_nombre_producto),
        ("CP06", "Validar que 'id_cliente' sea numérico", validate_id_cliente),
        ("CP07", "Validar que 'nombre_cliente' no esté vacío", validate_nombre_cliente),
        ("CP08", "Validar formato de 'email_cliente'", validate_email_cliente),
        ("CP09", "Validar que 'telefono_cliente' tenga entre 7 y 10 dígitos", validate_telefono_cliente),
        ("CP10", "Validar que 'direccion_cliente' no esté vacío", validate_direccion_cliente),
        ("CP11", "Validar que 'fecha_registro' sea un datetime", validate_fecha_registro),
        ("CP12", "Validar que 'total_venta' = 'precio' * 'cantidad'", validate_total_venta)
    ]
    
    results = []
    for test_id, description, test_func in tests:
        passed, errors = test_func(data)
        result = {
            "Test ID": test_id,
            "Descripción": description,
            "Resultado": "Aprobado" if passed else "Fallido",
            "Descripción del Resultado": "" if passed else f"{errors} errores encontrados",
            "Número de Incidencias": errors,
            "Comentarios": ""
        }
        results.append(result)
    return results

# Ejecutar todas las pruebas y almacenar los resultados
test_results = run_all_tests(data)

# Convertir los resultados a un DataFrame
results_df = pd.DataFrame(test_results)

# Exportar a Excel
results_df.to_excel("test_results.xlsx", index=False)  # exporta a archivo Excel

# Exportar a CSV
results_df.to_csv("test_results.csv", index=False)  # exporta a archivo CSV
