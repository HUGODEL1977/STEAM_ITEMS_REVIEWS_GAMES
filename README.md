Proyecto_Individual_Steam

Proyecto: Machine Learning Operations (MLOps) 

DESCRIPCION

Este proyecto tiene como objetivo desarrollar el rol de Data Scientist y Data Engineer, se aplican técnicas de extracción, transformación y carga de datos (ETL), análisis exploratorio de datos (EDA) y creación de un sistema de recomendacion de precio de los juegos de steam basado en un modelo de machine learning.

Se utilizaran 3  set de datos de plataformas de steam, con el fin de explorar Y entender los patrones, tendencias y así generar consultas con base en los datos proporcionados.

La extracción de los datos la limpieza y transformacion son factores importantes a tener en cuenta para llegar a la implementación del sistema de recomendacion y las consultas en general.

Se documenta cada etapa del proceso en cada archivo para la realización del ETL, el EDA y el modelo de machine learning.

Se hara el despliegue de la API primero en local y luego de manera virtual en Render, esto otorgara el acceso a las consultas y sus respectivos resultados.

Es importante explorar de manera profunda y profesional el proceso y el desarrollo del sistema de recomendacion y sus consultas, se deben abordar herramientas que nos permitan hacer ingenieria y analisis de datos.

Se plantea hacer un trabajo agil como data engineer y tener un MVP (Minimum Viable Product), para el cierre del proyecto, realizando una API REST con 6 funciones:

def developer( desarrollador : str ): Cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora. 

def userdata( User_id : str ): Debe devolver cantidad de dinero gastado por el usuario, el porcentaje de recomendación en base a reviews.recommend y cantidad de items.

def UserForGenre( genero : str ): Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.

def best_developer_year( año : int ): Devuelve el top 3 de desarrolladores con juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos).

def developer_reviews_analysis( desarrolladora : str ): Según el desarrollador, se devuelve un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo.

def recomendacion_usuario( id de usuario ): Ingresando el id de un usuario, deberíamos recibir una lista con 5 juegos recomendados para dicho usuario.

Se debe crear un modelo de recomendacion, en el que con las variables elegidas (id_user y recommend), debería recomendar a un usuario, la lista de juegos recomendados para el.

ESTUCTURA DEL REPOSITORIO

README.md: Archivo principal con información del proyecto.

proyecto_steam_API.py : Se encuentra toda la informacion con las funciones de consulta y los respectivos endpoints para disponibilizar en la API, tambien esta el modelo de recomendacion de machine learning con su respectiva consulta.

proyecto_steam_ETL.py: Aqui se visualiza todo el proceso de extraccion, transformacion aunque no es requerido y cargue de los archivos, se hace limpieza y se pueden ver los comentarios en el archivo de todo el ETL, los archivos json se descargan y se transforman en tres data frames, despues de la limpieza se convierten a csv, luego se unifica con merged y queda un solo archivo csv, df_merged.csv.

proyecto_steam_EDA.ipynb: En este archivo se visualiza todo el analisis exploratorio de los datos y el modelo de machine learning, se comenta para hacer mas preciso el paso a paso.

output_steam_games_cleaned-csv: Este es el archivo resultante de la limpieza del df correspondiente a games.

australian_users_items_cleaned-csv: Este es el archivo resultante de la limpieza del df correspondiente a items.

australian_users_reviews_cleaned-csv: Este es el archivo resultante de la limpieza del df correspondiente a reviews.

df_merged.csv: Este es el archivo resultante de la union de los tres anteriores y sobre el que se deben hacer las consultas

requirements.txt: Archivo con las dependencias y librerías que se necesitan para estructurar el proyecto.

https://drive.google.com/drive/folders/1hZNtAB7T0i5pIZMM4IfQLtfG8YPqnXB4?usp=drive_link "Aca se encuentran los archivos json iniciales"

El proceso de ETL esta con código comentado en proyecto_steam_ETL.py y el EDA junto con el modelo de machine learning esta con codigo comentado en proyecto_steam_EDA.ipynb.

https://drive.google.com/file/d/1_TwlPi7vOO6__ePlxPeQTLj2HtmeFfoY/view?usp=drive_link "Este es el video del Deployment de la API en RENDER" 

https://proyecto-steam-vcf5.onrender.com/docs#/ " Deployment de la API en RENDER"

Tecnologia usada
Visual Studio Code, Jupyter Notebook, Python, NumPy, Pandas, Matplotlib, scikit-learn, FastAPI, Git GitHub, Markdown.

GITHUB HUGODEL1977

Correo electronico: hugohernandelgadoo@gmail.com

Hugo Hernan Delgado Osorio
