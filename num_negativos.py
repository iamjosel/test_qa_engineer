import pandas as pd

file_path = r'O:\jose-test\ventas1.xlsx'  # Usar cadena sin formato para evitar caracteres de escape
df = pd.read_excel(file_path, engine='openpyxl')  # Especificar el motor

def analyze_sales_data(file_path):
    # Cargar el archivo de Excel
    df = pd.read_excel(file_path, engine='openpyxl')  # Especificar el motor

    # Convertir 'precio', 'cantidad_vendida' y 'total_venta' a numérico para detectar errores
    df['precio'] = pd.to_numeric(df['precio'].astype(str).str.replace('$', '').str.replace(',', ''), errors='coerce')
    df['cantidad_vendida'] = pd.to_numeric(df['cantidad_vendida'], errors='coerce')
    df['total_venta'] = pd.to_numeric(df['total_venta'].astype(str).str.replace('$', '').str.replace(',', ''), errors='coerce')

    # Detectar registros con valores negativos en 'precio', 'cantidad_vendida' y 'total_venta'
    negative_prices = df[df['precio'] < 0].shape[0]
    negative_quantity = df[df['cantidad_vendida'] < 0].shape[0]
    negative_total_sales = df[df['total_venta'] < 0].shape[0]

    # Detectar registros que contienen un '-' en 'precio', 'cantidad_vendida' y 'total_venta'
    contains_minus_prices = df['precio'].astype(str).str.contains('-', na=False).sum()
    contains_minus_quantity = df['cantidad_vendida'].astype(str).str.contains('-', na=False).sum()
    contains_minus_total_sales = df['total_venta'].astype(str).str.contains('-', na=False).sum()

    # Detectar registros que contienen '$-' en 'precio' y 'total_venta'
    contains_dollar_minus_prices = df['precio'].astype(str).str.contains(r'\$-', na=False).sum()
    contains_dollar_minus_total_sales = df['total_venta'].astype(str).str.contains(r'\$-', na=False).sum()

    # Detectar registros con valores no numéricos en 'total_venta'
    non_numeric_total_sales = df['total_venta'].isnull().sum()

    #Imprimir los resultados
    print("\nCantidad de registros negativos en la columna precios:", negative_prices)
    print("Cantidad de registros negativos en la columna total_venta:", negative_total_sales)
    print("Cantidad de registros con valores no numéricos en total_venta:", non_numeric_total_sales)

# Ejecutar la función con la ruta de tu archivo
analyze_sales_data(file_path)

