from fastapi import FastAPI      # Importar FastAPI para crear una API web
import pandas as pd              # Importar pandas para análisis de datos


# Cargar el DataFrame con los datos
df = pd.read_csv("df_merged.csv")

app = FastAPI ()


# Convierte la columna 'release_date' a tipo datetime
df['release_date'] = pd.to_datetime(df['release_date'])

df.drop('Unnamed: 0', axis=1, inplace=True)

print(df)

# Muestra la columna relase date
release_date_unique = df['release_date'].unique()
print(release_date_unique)

# Definir una función que calcule la cantidad de ítems y el contenido gratuito por año para un desarrollador específico
def developer_items_and_free_content(developer_name):
    developer_data = df[df['developer'] == developer_name]
    
    items_by_year = developer_data.groupby(developer_data['release_date'].dt.year).agg(
        {'item_id_x': 'count', 'price': lambda x: (x == 0).sum() / len(x)}
    )
    
    items_by_year.rename(columns={'item_id_x': 'Cantidad de Items', 'price': 'Contenido Free'}, inplace=True)
    items_by_year['Contenido Free'] = items_by_year['Contenido Free'].apply(lambda x: f"{x:.0%}")
    items_by_year.reset_index(inplace=True)
    items_by_year.rename(columns={'release_date': 'Año'}, inplace=True)
    
    return items_by_year

# Crear un endpoint para consultar la información de un desarrollador
@app.get("/developer/{developer_name}")
def get_developer_info(developer_name: str):
    result = developer_items_and_free_content(developer_name)
    return result.to_dict(orient='records')



# Validación del user_id en el decorador
@app.get("/userdata/{user_id}")
def userdata(user_id: str):
    # Validar el formato del user_id
    try:
        user_id = int(user_id)  # Intentar convertir a entero
        if user_id < 0:
            return {"error": "ID de usuario inválido"}
    except ValueError:
        return {"error": "ID de usuario no es un número válido"}

    user_info = get_user_data(user_id)

    if user_info.get("error"):
        return user_info  # Si hay un error en el ID, retornar el error
    else:
        return user_info  # Si no hay error, retornar los datos del usuario

# Definir una función que obtenga los datos del usuario
def get_user_data(user_id):
    user_data = df[df['user_id'] == user_id]

    if user_data.empty:
        return {"error": "Usuario no encontrado"}

    money_spent = float(user_data['price'].sum())  # Convertir a float
    total_items = int(user_data['item_id_x'].count())  # Convertir a int
    recommend_percentage = float(user_data['recommend'].mean() * 100)  # Convertir a float

    user_info = {
        "Usuario X": user_id,
        "Dinero gastado": f"${money_spent:.2f}",
        "% de recomendación": f"{recommend_percentage:.0f}%",
        "Cantidad de items": total_items
    }
    return user_info


@app.get("/user-for-genre/{genre}")
async def UserForGenre(genre: str):
    # Filtra el DataFrame por el género dado.
    df_filtered = df[df['genres'] == genre]

    if df_filtered.empty:
        return {"message": f"No hay datos disponibles para el género {genre}"}

    # Encuentra al usuario con más horas jugadas.
    usuario_mas_horas = df_filtered.loc[df_filtered['playtime_forever'].idxmax()]['user_id']

    # Agrupa los datos por año de lanzamiento y suma las horas jugadas.
    horas_por_anio = df_filtered.groupby(df_filtered['release_date'].dt.year)['playtime_forever'].sum()

    # Convierte las columnas con objetos `numpy.int64` en tipos nativos de Python.
    horas_por_anio = horas_por_anio.astype(int)

    # Convierte el resultado en una lista de diccionarios.
    lista_horas_por_anio = [{"Año": anio, "Horas": int(horas)} for anio, horas in horas_por_anio.items()]

    # Crea el resultado final.
    resultado = {
        "Usuario con más horas jugadas para Género X": int(usuario_mas_horas),
        "Horas jugadas por año": lista_horas_por_anio
    }

    return resultado


@app.get("/best-developer-year/{year}")
async def best_developer_year(year: int):
    # Filtra el DataFrame por el año dado.
    df_filtered = df[df['release_date'].dt.year == year]

    # Filtra los juegos recomendados con comentarios positivos
    df_filtered = df_filtered[(df_filtered['recommend'] == True) & (df_filtered['sentiment_analysis'] > 0)]

    # Agrupa los datos por desarrollador y cuenta el número de juegos recomendados y la suma de comentarios positivos
    developers = df_filtered.groupby('developer').agg({'title': 'count', 'funny': 'sum'}).reset_index()
    developers.columns = ['developer', 'total_recommended_games', 'total_positive_funny']

    # Encuentra los 3 desarrolladores con más juegos recomendados
    top_developers = developers.nlargest(3, 'total_recommended_games')

    return top_developers.to_dict(orient='records')



@app.get("/developer-reviews-analysis/{developer}")
async def developer_reviews_analysis(developer: str):
    # Filtra el DataFrame por el desarrollador especificado.
    df_filtered = df[df['developer'] == developer]

    # Filtra las reseñas con sentimiento positivo y negativo.
    positive_reviews = df_filtered[df_filtered['sentiment_analysis'] > 0]
    negative_reviews = df_filtered[df_filtered['sentiment_analysis'] < 0]

    # Crea una lista con los resultados.
    results = []

    # Agrega la cantidad total de reseñas positivas.
    results.append({
        "developer": developer,
        "sentiment": "positive",
        "total_reviews": len(positive_reviews)
    })

    # Agrega la cantidad total de reseñas negativas.
    results.append({
        "developer": developer,
        "sentiment": "negative",
        "total_reviews": len(negative_reviews)
    })

    return results



