import pandas as pd
import re

'''@uthor: José Luis García Quinayás
City: Popayán - Cauca
Date: 27/Oct/2024'''

# ubicación del archivo ventas
file_path = "O:\\jose-test\\ventas1.xlsx"

# Cargar el archivo Excel
data = pd.read_excel(file_path)

# Convertir las columnas 'precio' y 'cantidad_vendida' a números
data['precio'] = pd.to_numeric(data['precio'], errors='coerce')
data['cantidad_vendida'] = pd.to_numeric(data['cantidad_vendida'], errors='coerce')

# Caracteres especiales
special_characters_pattern = r'[^a-zA-Z0-9\s]'

# funciones de los reportes

# 1. Reporte de campos nulos o vacíos en columnas específicas
def report_missing_fields(data, column_name):
    """Genera reporte para registros con valores nulos o vacíos en una columna específica."""
    missing_data = data[data[column_name].isna() | (data[column_name] == '')]
    missing_data.to_excel(f"O:\\jose-test\\reporte_missing_{column_name}.xlsx", index=False)
    print(f"Reporte generado: Registros con {column_name} vacío o nulo - {missing_data.shape[0]} registros")
    return missing_data.shape[0]

# 2. Reporte de precios negativos
def report_negative_precio(data):
    """Genera reporte para precios negativos en la columna 'precio'."""
    negative_precio = data[data['precio'] < 0]
    negative_precio.to_excel("O:\\jose-test\\reporte_negative_precio.xlsx", index=False)
    print(f"Reporte generado: Registros con precios negativos - {negative_precio.shape[0]} registros")
    return negative_precio.shape[0]

# 3. Reporte de cantidades negativas en 'cantidad_vendida'
def report_negative_cantidad_vendida(data):
    """Genera reporte para registros con cantidad_vendida negativa."""
    negative_cantidad = data[data['cantidad_vendida'] < 0]
    negative_cantidad.to_excel("O:\\jose-test\\reporte_negative_cantidad_vendida.xlsx", index=False)
    print(f"Reporte generado: Registros con cantidad_vendida negativa - {negative_cantidad.shape[0]} registros")
    return negative_cantidad.shape[0]

# 4. Reporte de total_venta inconsistente
def report_inconsistent_total_venta(data):
    """Verifica que total_venta coincida con precio * cantidad_vendida y guarda un reporte en Excel."""
    inconsistent_total = data[data['total_venta'] != data['precio'] * data['cantidad_vendida']]
    inconsistent_total.to_excel("O:\\jose-test\\reporte_inconsistent_total_venta.xlsx", index=False)
    print(f"Reporte generado: Registros con total_venta inconsistente - {inconsistent_total.shape[0]} registros")
    return inconsistent_total.shape[0]

# 5. Reporte de caracteres especiales en columnas específicas (incluye guion)
def report_special_characters(data, column_name):
    """Genera reporte para registros con y sin caracteres especiales en una columna de texto."""
    special_chars = data[column_name].str.contains(special_characters_pattern, regex=True, na=False)
    with_special = data[special_chars]
    without_special = data[~special_chars]
    with_special.to_excel(f"O:\\jose-test\\reporte_{column_name}_con_especiales.xlsx", index=False)
    without_special.to_excel(f"O:\\jose-test\\reporte_{column_name}_sin_especiales.xlsx", index=False)
    print(f"Reporte generado: {column_name} - {with_special.shape[0]} con caracteres especiales, {without_special.shape[0]} sin caracteres especiales")
    return with_special.shape[0], without_special.shape[0]

# 6. Reporte de valores válidos en 'categoria'
def report_invalid_categoria(data):
    """Genera reporte para registros en la columna 'categoria' con valores no especiales, vacíos o nulos."""
    special_characters = data['categoria'].str.contains(special_characters_pattern, regex=True, na=False)
    invalid_categoria = data[~special_characters | data['categoria'].isna() | (data['categoria'] == '')]
    invalid_categoria.to_excel("O:\\jose-test\\reporte_categoria_invalidos.xlsx", index=False)
    print(f"Reporte generado: Categoría no especial, vacía o nula - {invalid_categoria.shape[0]} registros")
    return invalid_categoria.shape[0]

def report_valid_categoria(data, valid_categories):
    """Verifica que las categorías pertenezcan a una lista válida y guarda un reporte en Excel."""
    invalid_categoria = data[~data['categoria'].isin(valid_categories)]
    invalid_categoria.to_excel("O:\\jose-test\\reporte_categoria_no_valida.xlsx", index=False)
    print(f"Reporte generado: Categorías no válidas - {invalid_categoria.shape[0]} registros")
    return invalid_categoria.shape[0]

#supuestas
valid_categories = ['Electrónica', 'Ropa', 'Alimentos']

def report_special_characters_metodo_pago(data):
    """Genera reporte para registros con y sin caracteres especiales en la columna 'metodo_pago'."""
    special_chars = data['metodo_pago'].str.contains(special_characters_pattern, regex=True, na=False)
    with_special = data[special_chars]
    without_special = data[~special_chars]
    with_special.to_excel("O:\\jose-test\\reporte_metodo_pago_con_especiales.xlsx", index=False)
    without_special.to_excel("O:\\jose-test\\reporte_metodo_pago_sin_especiales.xlsx", index=False)
    print(f"Reporte generado: método de pago - {with_special.shape[0]} con caracteres especiales, {without_special.shape[0]} sin caracteres especiales")
    return with_special.shape[0], without_special.shape[0]

# Ejecutar los reportes y almacenar los conteos
missing_fecha_venta = report_missing_fields(data, 'fecha_venta')
missing_id_producto = report_missing_fields(data, 'id_producto')
missing_nombre_producto = report_missing_fields(data, 'nombre_producto')
missing_categoria = report_missing_fields(data, 'categoria')
negative_precio = report_negative_precio(data)
negative_cantidad_vendida = report_negative_cantidad_vendida(data)
inconsistent_total_venta = report_inconsistent_total_venta(data)
nombre_producto_con, nombre_producto_sin = report_special_characters(data, 'nombre_producto')
nombre_cliente_con, nombre_cliente_sin = report_special_characters(data, 'nombre_cliente')
invalid_categoria = report_valid_categoria(data, valid_categories)
invalid_categoria_report = report_invalid_categoria(data)
metodo_pago_con, metodo_pago_sin = report_special_characters_metodo_pago(data)

# Resumen de criterios de cada reporte:
criterios_reporte = {
    "fecha_venta vacío o nulo": missing_fecha_venta,
    "id_producto vacío o nulo": missing_id_producto,
    "nombre_producto vacío o nulo": missing_nombre_producto,
    "categoria vacío o nulo": missing_categoria,
    "precio negativo": negative_precio,
    "cantidad_vendida negativa": negative_cantidad_vendida,
    "total_venta inconsistente": inconsistent_total_venta,
    "nombre_producto con caracteres especiales": nombre_producto_con,
    "nombre_producto sin caracteres especiales": nombre_producto_sin,
    "nombre_cliente con caracteres especiales": nombre_cliente_con,
    "nombre_cliente sin caracteres especiales": nombre_cliente_sin,
    "categorías no válidas": invalid_categoria,
    "categoría no especial, vacía o nula": invalid_categoria_report,
    "metodo_pago con caracteres especiales": metodo_pago_con,
    "metodo_pago sin caracteres especiales": metodo_pago_sin
}

print("Criterios y conteos de cada reporte:", criterios_reporte)