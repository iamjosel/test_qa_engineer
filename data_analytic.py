import pandas as pd

'''@uthor: José Luis García Quinayás
City: Popayán - Cauca
Date: 26/Oct/2024'''

# Cargar el archivo ventas1.xlsx para consultar el contenido y validar los nombres, títulos, encabezados de las columnas
file_path = r'O:\jose-test\ventas1.xlsx'  # Usar cadena sin formato para evitar caracteres de escape
df = pd.read_excel(file_path, engine='openpyxl')  # Especificar el motor

# 1. Identificar el conteo de valores nulos en cada columna
'''null_counts = df.isnull().sum()
print("Conteo de valores nulos por columna:")
print(null_counts)'''

df['precio'] = pd.to_numeric(df['precio'].astype(str).str.replace('$', '').str.replace(',', ''), errors='coerce')
df['total_venta'] = pd.to_numeric(df['total_venta'].astype(str).str.replace('$', '').str.replace(',', ''), errors='coerce')

# Identificar el conteo de valores nulos en cada columna
null_counts = df.isnull().sum()
print("Conteo de valores errados por columna:")
print(null_counts)

# 2. Contar registros con precios negativos
# Función para limpiar el texto y convertirlo en número
def parse_price(price):
    # Eliminar el símbolo de dólar y convertir a número
    if isinstance(price, str):
        price = price.replace('$', '').replace(',', '')
    return pd.to_numeric(price, errors='coerce')

'''
Valores nulos:

fecha_venta: 47 nulos
id_producto: 0 nulos
nombre_producto: 30 nulos
categoria: 36 nulos
precio: 36 nulos
cantidad_vendida: 0 nulos
nombre_cliente: 43 nulos
region: 41 nulos
metodo_pago: 38 nulos
Precios negativos: 507 registros contienen valores negativos en la columna precio.
Precios negativos: 507 registros contienen valores negativos en la columna total_venta.
Cantidad de registros con valores no numéricos en total_venta: 36
'''