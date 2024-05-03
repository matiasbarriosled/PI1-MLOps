import ast
import gzip
import json
import pandas as pd

#-------------------------------------------------------------------------------------------------------------
def Cargar_a_Dataframe(ruta, modo_read):
    filas = []
    linea_json = json  
    if modo_read=='rt':      
        with gzip.open(ruta,modo_read,encoding='utf-8') as archivo:
            for linea in archivo:
                filas.append(linea_json.loads(linea)) 
        archivo.close()
    
    if modo_read=='rb':
        with gzip.open(ruta,modo_read) as archivo:
            for linea in archivo:
                filas.append(ast.literal_eval(linea.decode('utf-8')))
        archivo.close()

    df = pd.DataFrame(filas)
    return df
#-------------------------------------------------------------------------------------------------------------


def CalcularNulos(df):
    for columna in df:
        nulos = 100*(df[columna].isnull().sum()/df.shape[0])
        porcentaje = "{:.1f}".format(nulos)
        print("el porcentaje de datos nulos en la columna ",df[columna].name," es del ",porcentaje,"%")

    print('-------------------------------------------------------------------------------------------')
#-------------------------------------------------------------------------------------------------------------


def DesanidarColumnas(df,col_anidada,col_concat):
    df = df.explode(col_anidada).reset_index()

    col_clave = df.loc[0,col_anidada]
    claves = list(col_clave.keys())

    datos = pd.json_normalize(df[col_anidada])[claves]
    df = pd.concat([df[col_concat],datos],axis=1)

    return df
#-------------------------------------------------------------------------------------------------------------


def ExtraerAño(df,columna,nueva_columna):
    year_r = r"(\d{4})"
    df = df[df[columna].str.contains(year_r)]
    df[nueva_columna] = df[columna].str.extract(year_r)
    df = df.drop(columna, axis=1)
    
    return df
#-------------------------------------------------------------------------------------------------------------