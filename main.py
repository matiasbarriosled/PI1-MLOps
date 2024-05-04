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

@app.get('/playtimegenre/{genero}')
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

@app.get('/userforgenre/{genero}')
def UserForGenre(genero: str):
    ''