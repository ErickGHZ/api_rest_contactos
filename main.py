from fastapi import FastAPI
import csv
import json

app = FastAPI()



@app.get("/v1/contactos")
async def root():

    # TODO read contactos.csv
    # Crear una lista para almacenar los datos CSV
    datos_csv = []

    # Abre el archivo CSV en modo lectura
    with open('contactos.csv', 'r', newline='') as archivo_csv:
        lector_csv = csv.DictReader(archivo_csv)

    # TODO JSON encode contactos.csv
    # Itera sobre las filas del archivo CSV
    for fila in lector_csv:
        # Agrega cada fila como un diccionario a la lista
        datos_csv.append(fila)

    # TODO save in response
    response = json.dumps(datos_csv, indent=4)

    return response