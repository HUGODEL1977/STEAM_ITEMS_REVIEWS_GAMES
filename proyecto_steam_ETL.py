import pandas as pd # Importamos la biblioteca pandas para trabajar con DataFrames
import json # Importamos la biblioteca json para trabajar con archivos JSON
import ast # Importamos la biblioteca ast para manejar literales de estructuras de datos en Python

# STEAM_GAMES_JSON
ruta_json1 = 'output_steam_games.json' # Establecemos la ruta al archivo JSON.

with open(ruta_json1, 'r') as file:  # Abrimos el archivo JSON en modo lectura ('r') y lo cargamos en la variable 'data'.
    data = [json.loads(line) for line in file]
df1 = pd.DataFrame(data)

# Se convierten las listas anidadas en las columnas 'genres', 'tags' y 'specs' de un DataFrame en cadenas de texto, lo que simplifica 
# el manejo y procesamiento de los datos al representarlos como texto separado por comas.

df1['genres'] = df1['genres'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
df1['tags'] = df1['tags'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
df1['specs'] = df1['specs'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

# Divide las cadenas en listas utilizando la coma (',') como separador
df1['genres'] = df1['genres'].str.split(', ')
df1['tags'] = df1['tags'].str.split(', ')
df1['specs'] = df1['specs'].str.split(', ')

# Desanida las columnas anidadas
df1 = df1.explode('genres', ignore_index=True)
df1 = df1.explode('tags', ignore_index=True)
df1 = df1.explode('specs', ignore_index=True)

# Elimina filas con valores NaN en todas las columnas
df1 = df1.dropna()

# Elimina duplicados basados en la columna 'id'
df1 = df1.drop_duplicates(subset='id')

# Elimina las columnas que no son necesarias para las consultas
df1 = df1.drop(["app_name","reviews_url","publisher","url", "tags", "specs", "early_access"], axis=1)

# Convierte la columna 'release_date' del DataFrame en objetos de fecha y hora (datetime).
df1['release_date'] = pd.to_datetime(df1['release_date'], errors='coerce')

# Esta línea elimina todas las filas que tienen un valor nulo en la columna 'release_date'
df1.dropna(subset=['release_date'], inplace=True)

# Esta línea convierte la columna id' del DataFrame  en valores numéricos
df1['id'] = pd.to_numeric(df1['id'], errors='coerce')

# convierte la columna release_date al tipo de dato de fecha (datetime)
df1['release_date'] = pd.to_datetime(df1['release_date'])

# La opción 'coerce' convierte los valores no numéricos a NaN (valores nulos) en caso de que existan.
df1['price'] = pd.to_numeric(df1['price'], errors='coerce')

# Esto eliminará las filas que tienen NaN en la columna "price"
df1 = df1.dropna(subset=['price'])

# Elimina las filas duplicadas en el DF
df1 = df1.drop_duplicates()

df1 = df1.rename(columns={'id': 'item_id'})

df1['item_id'] = df1['item_id'].astype('int32')

# Se restablece el índice del DataFrame 
df1 = df1.reset_index(drop=True)

pd.set_option('display.expand_frame_repr', False)  # Evita que las columnas se ajusten automáticamente

print(df1.head(10))



#AUSTRALIAN_ITEMS_REVIEWS

from concurrent.futures import ThreadPoolExecutor # Importar ThreadPoolExecutor para procesamiento en paralelo

# Función para procesar cada registro y desanidar los items
def process_record(record):
    df_record = pd.json_normalize(ast.literal_eval(record)) #  Normalizar el registro JSON a un DataFrame utilizando pandas
    items_df = pd.json_normalize(df_record['items'][0])  # Normalizar la columna 'items' a un DataFrame separado
    df_record.drop('items', axis=1, inplace=True) #   # Eliminar la columna 'items' del DataFrame original
    return pd.concat([df_record, items_df], axis=1) # Concatenar el DataFrame original con el DataFrame de items

# Leer el archivo JSON
with open("australian_users_items.json", 'r', encoding="utf-8") as file: 
    data = file.readlines()

# Procesar los registros en paralelo
with ThreadPoolExecutor() as executor: # Usar el ThreadPoolExecutor para aplicar la función process_record a cada elemento en 'data'
    dfs = list(executor.map(process_record, data))

# Concatenar los DataFrames resultantes en uno solo
df2 = pd.concat(dfs, ignore_index=True)

# Eliminar las columnas especificadas
df2 = df2.drop(['steam_id', 'user_url', 'playtime_2weeks', 'items_count'], axis=1)

# Eliminar filas con valores NaN en "user_id"
df2 = df2.dropna(subset=['user_id'])

# Reemplazar NaN en "playtime_forever" con 0
df2['playtime_forever'].fillna(0, inplace=True)

# Eliminar valores negativos en "playtime_forever"
df2 = df2[df2['playtime_forever'] >= 0]

# Identifica filas que contengan valores no válidos en 'user_id' y 'item_id'
# Convierte los valores no válidos en NaN y luego usa dropna para eliminar esas filas.
df2['user_id'] = pd.to_numeric(df2['user_id'], errors='coerce')
df2['item_id'] = pd.to_numeric(df2['item_id'], errors='coerce')
df2 = df2.dropna()

# Se convierten las columnas a datos enteros.
df2['user_id'] = df2['user_id'].astype(float)
df2['user_id'] = df2['user_id'].astype('int64')
df2['item_id'] = df2['item_id'].astype(int)

# Elimina las filas duplicadas en el DataFrame
df2 = df2.drop_duplicates()

# Reindexar el DataFrame
df2 = df2.reset_index(drop=True)

print(df2.head(10))


# AUSTRALIAN_USER-REVIEWS_JSON

from textblob import TextBlob

# Leer el archivo json
with open("australian_user_reviews.json", 'r',encoding="utf-8") as file: 
    data = file.readlines()
    records = [ast.literal_eval(line.strip()) for line in data]

# Desanidar la columna 'reviews' y crear un DataFrame
df3 = pd.json_normalize(records, 'reviews', ['user_id', 'user_url'])

# Define una función para analizar el sentimiento
def analyze_sentiment(review):
    # Utiliza TextBlob para obtener la polaridad del sentimiento
    sentiment = TextBlob(review)
    # Asigna un valor numérico según la polaridad
    if sentiment.sentiment.polarity < 0:
        return 0  # Negativo
    elif sentiment.sentiment.polarity == 0:
        return 1  # Neutral
    else:
        return 2  # Positivo

# Aplica la función a la columna 'review' y crea la nueva columna 'sentiment_analysis'
df3['sentiment_analysis'] = df3['review'].apply(analyze_sentiment)

# Elimina la columna 'review' 
df3.drop('review', axis=1, inplace=True)

# Elimina las columnas 
columns_to_drop = ['last_edited', 'helpful', 'user_url']
df3.drop(columns=columns_to_drop, inplace=True)

# Eliminar las filas de "posted" que no cumplen con el formato
df3 = df3[df3['posted'].str.match(r'Posted [A-Z][a-z]+ \d{1,2}, \d{4}\.')]

# Identifica filas que contengan valores no válidos en 'user_id' y 'item_id'
# Convierte los valores no válidos en NaN y luego usa dropna para eliminar esas filas.
df3['user_id'] = pd.to_numeric(df3['user_id'], errors='coerce')
df3['item_id'] = pd.to_numeric(df3['item_id'], errors='coerce')
df3 = df3.dropna()

# Se convierten las columnas a datos enteros.
# Se convierten las columnas a datos enteros.
df3['user_id'] = df3['user_id'].astype(float)
df3['user_id'] = df3['user_id'].astype('int64')
df3['item_id'] = df3['item_id'].astype(int)

# Eliminar filas duplicadas
df3.drop_duplicates(inplace=True)

# Convertir la columna "posted" a un formato de fecha
df3['posted'] = pd.to_datetime(df3['posted'], format='Posted %B %d, %Y.')

# Reemplaza los valores en blanco o nulos en la columna 'funny' con NaN
df3['funny'].replace(['', 'NaN', 'nan', None], pd.NA, inplace=True)

# Elimina las filas con NaN en la columna 'funny'
df3 = df3.dropna(subset=['funny'])

# Genera el indice de nuevo
df3 = df3.reset_index(drop=True)

# Mostrar el DataFrame resultante

print(df3.head(10))


# df MERGED 

# Unir df1 y df2 usando 'item_id' como clave de unión
merged_df = pd.merge(df1, df2, on='item_id', how='inner')

# Luego, unir el resultado anterior con df3 usando 'user_id' como clave de unión
merged_df = pd.merge(merged_df, df3, on='user_id', how='inner')

# Eliminar filas con user_id no válidos (negativos o no numéricos)
merged_df = merged_df[merged_df['user_id'].astype(str).str.isnumeric()]
merged_df['user_id'] = merged_df['user_id'].astype(int)


merged_df = merged_df.reset_index(drop=True)
pd.set_option('display.max_rows', 100)  # Muestra hasta 20 filas


print(merged_df)

merged_df.to_csv("df_merged.csv")