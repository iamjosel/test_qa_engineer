import pandas as pd

'''@uthor: José Luis García Quinayás
City: Popayán - Cauca
Date: 26/Oct/2024'''

# Cargar el archivo ventas1.xlsx
file_path = r'O:\jose-test\ventas1.xlsx'  # Usar cadena sin formato para evitar caracteres de escape
df = pd.read_excel(file_path, engine='openpyxl')  # Especificar el motor

# Información detallada del DataFrame
print("\nInformación general del DataFrame:")
print(df.info())

# Información detallada
print("\nLa hoja de datos en ventas1.xlsx tiene {} filas y {} columnas.".format(df.shape[0], df.shape[1]))

column_descriptions = {
    'fecha_venta': 'Fecha de la venta (algunos valores nulos).',
    'id_producto': 'Identificación del producto (sin valores nulos).',
    'nombre_producto': 'Nombre del producto (algunos valores nulos).',
    'categoria': 'Categoría del producto (algunos valores nulos).',
    'precio': 'Precio del producto, con algunos datos negativos (algunos valores nulos).',
    'cantidad_vendida': 'Cantidad de producto vendido (sin valores nulos).',
    'total_venta': 'Monto total de la venta, en algunos casos inconsistentes con el precio y cantidad.',
    'nombre_cliente': 'Nombre del cliente (algunos valores nulos).',
    'region': 'Región de la venta (algunos valores nulos).',
    'metodo_pago': 'Método de pago usado (algunos valores nulos).'
}

print("\nLas columnas en el archivo son:")
for col, desc in column_descriptions.items():
    if col in df.columns:
        print(f"{col}: {desc}")
    else:
        print(f"{col}: Columna no encontrada en el archivo.")