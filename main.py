from fastapi import FastAPI

app = FastAPI()

import json
import pandas as pd
import numpy as np

df = pd.read_csv('POBLACION.csv')

#limpieza de datos
df = df.rename(columns={'Valor':'Porcentaje'})
df = df.rename(columns={'año':'Ano'})
df = df.rename(columns={'Dominio geográfico':'DominioGeografico'})

df.to_json("archivo.json", orient="records", date_format="epoch", double_precision=10, force_ascii=True, date_unit="ms", default_handler=None)

@app.get("/")
def index():
    return {"message": "¡Bienvenido a mi API!"}

@app.get("/items/{year}")
async def read_items(year: int):
    # Realiza el filtrado por el Ano recibido en la variable 'year'
    df_filtrado = df[df['Ano'] == year]
    return {"year": year, "data": df_filtrado.to_dict(orient='records')}

@app.get("/antioquia-data")
def get_antioquia_data():
    try:
        df_antioquia = df[(df['DominioGeografico'] == 'Antioquia') & (df['Ano'] >= 2008) & (df['Ano'] <= 2019)]
        return df_antioquia.to_dict(orient='records')
    except Exception as e:
        return {"error": str(e)}