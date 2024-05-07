from fastapi import FastAPI
from fastapi.responses import HTMLResponse 
import pandas as pd

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def index():
    principal= """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Steam</title>
    <style>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    </style>
</head>
<style>

  body{
    background-color:yellow
  }

  .centro{
    width:400px,
    height:560px,
    background-color:white
  }

</style>
<body>
  
  <div class="centro"><a href="https://www.soyhenry.com" target="_blank"> #SoyHenry </a></div>
  <br>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
</body>
</html>


        """    
    return principal

@app.get('/PlayTimeGenre/{genero}')
def PlayTimeGenre(genero: str):
    items_games = pd.read_parquet("consultas/playtime_genre.parquet")
    #filtramos los datos que cumplan con la busqueda
    df_genre = items_games[items_games['genres']==genero]
    #del filtro solo nos quedamos con la fila que tiene la mayor acumulacion de playtime_forever
    resultado = df_genre[df_genre['playtime_forever']==df_genre['playtime_forever'].max()]
    #por ultimo extraemos el dato que nos interesa de toda la fila que es el año
    resultado = resultado['release_year']
    
    texto = f'ano de lanzamiento con mas horas jugadas para el Género de {genero}: '+resultado.iloc[0]
    return texto



@app.get('/UserForGenre/{genero}')
def UserForGenre(anio: int):
    user_genre = pd.read_parquet('consultas/user_for_genre.parquet')
    usuario = user_genre[user_genre['genres'].apply(lambda x: genero in x)]

    usuario.drop(['genres','release_year'], axis=1, inplace=True)

    usuario = usuario.groupby(['user_id']).sum().reset_index()

    usuario = usuario[usuario['playtime_forever']==usuario['playtime_forever'].max()]
    return usuario['user_id'].iloc[0]



@app.get('/UsersRecommend/{anio}')
def UsersRecommend(anio: int):
    review = pd.read_parquet('consultas/users_recommend.parquet')
    #con groupby() podemos realizar la suma, agrupando primero el año, despues el conjunto de title
    # y realizar una suma en la columna restante que es sentiment analysis esta nos servira para 
    #  contar cuantas veces aparece el juego recomendado
    review = review.groupby(['year_posted','title']).sum().reset_index()
    review = review[review['year_posted']==anio]
    review = review.sort_values('recommend',ascending=False)
    
    texto = f'JUEGOS MAS RECOMENDADOS -->  PUESTO N°1: '+review.iloc[0]['title']+f' ||  PUESTO N°2: '+ review.iloc[1]['title']+f' ||  PUESTO N°3: '+ review.iloc[2]['title']
    return texto



@app.get('/UsersNotRecommend/{anio}')
def UsersNotRecommend(anio: int):
    review = pd.read_parquet('consultas/users_not_recommend.parquet')
    review = review.groupby(['year_posted','title']).sum().reset_index()
    review = review[review['year_posted']==anio]
    review = review.sort_values('not_recommend',ascending=False)
    
    texto = f'JUEGOS MENOS RECOMENDADOS -->  PUESTO N°1: '+review.iloc[0]['title']+f' ||  PUESTO N°2: '+ review.iloc[1]['title']+f' ||  PUESTO N°3: '+ review.iloc[2]['title']
    return texto



@app.get('/SentimentAnalysis/{anio}')
def SentimentAnalysis(anio: int):
    sentiment = pd.read_parquet('consultas/sentiment_analysis.parquet')
    sentiment = sentiment.groupby(['year_posted','sentiment_analysis']).sum().reset_index()
    sentiment = sentiment[sentiment['year_posted']==anio]
    
    sentiment['sentiment_analysis']=sentiment['sentiment_analysis'].replace(0,'negativo')
    sentiment['sentiment_analysis']=sentiment['sentiment_analysis'].replace(1,'neutral')
    sentiment['sentiment_analysis']=sentiment['sentiment_analysis'].replace(2,'positivo')

    indice=3
    texto = ''

    while indice>0:
        texto+=f'{sentiment.iloc[indice-1][1]}:{sentiment.iloc[indice-1][2]}'
        if indice>1:
            texto+=', '
        indice-=1

    return texto



