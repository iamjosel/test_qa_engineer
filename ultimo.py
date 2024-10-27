import pandas as pd
import re

# Load the data
file_path = r'O:\jose-test\ventas1.xlsx'  # Usar cadena sin formato para evitar caracteres de escape
df = pd.read_excel(file_path, engine='openpyxl')  # Especificar el motor
# Analysis Results
results = {}

# 1. Null Values Analysis
null_summary = df.isnull().sum()
null_columns = null_summary[null_summary > 0]
null_columns_dict = null_columns.to_dict()  # For reporting null values by column

# 2. Negative Price Analysis
# Distinguish between values with '-' and '$-'
negative_price_dash = df[df['precio'].astype(str).str.startswith('-')]
negative_price_dollar_dash = df[df['precio'].astype(str).str.startswith('$-')]
negative_price_counts = {
    'Total Negative Prices': len(negative_price_dash) + len(negative_price_dollar_dash),
    'Negative Prices with -': len(negative_price_dash),
    'Negative Prices with $-': len(negative_price_dollar_dash)
}

# 3. Inconsistent total_venta Analysis
# Expected total_venta = precio * cantidad_vendida
df['expected_total_venta'] = df['precio'] * df['cantidad_vendida']
inconsistent_total_venta = df[df['total_venta'] != df['expected_total_venta']]
inconsistent_total_venta_count = len(inconsistent_total_venta)

# 4. Special Characters Analysis
# Define regex for special characters detection
special_chars_regex = r'[^a-zA-Z0-9\s]'
special_char_columns = ['nombre_producto', 'categoria', 'nombre_cliente', 'metodo_pago']
special_char_counts = {}

# Count occurrences of special characters in each specified column
for column in special_char_columns:
    contains_special_chars = df[column].astype(str).str.contains(special_chars_regex)
    special_char_counts[column] = {
        'With Special Characters': contains_special_chars.sum(),
        'Without Special Characters': (~contains_special_chars).sum()
    }

# Store results in the dictionary
results['Null Values'] = null_columns_dict
results['Negative Prices'] = negative_price_counts
results['Inconsistent Total Venta'] = inconsistent_total_venta_count
results['Special Character Counts'] = special_char_counts

print("datos con valores nulos",null_columns_dict)
print()
print("datos con precios negativos",negative_price_counts)
print()
print("datos con inconsistencia de valores",inconsistent_total_venta_count)
print()
print("datos con caracteres especiales",special_char_counts)
