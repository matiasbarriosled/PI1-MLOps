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
<body>
  
  <div class="footer-text"><a href="https://www.soyhenry.com" target="_blank"> #SoyHenry </a></div>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
</body>
</html>


        """    
    return principal

@app.get('/PlayTimeGenre/{genero}')
def PlayTimeGenre(genero: str):  
  'columnas necesaria: items --> item_id, playtime_forever | games --> id'
