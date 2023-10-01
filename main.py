from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
import csv
import json
import shutil
import os

class Contacto(BaseModel):
    nombre: str 
    email: str

def cargar_guardar_contactos(contactos=None, ruta_csv: str = 'contactos.csv'):
    """
    Carga o guarda la lista de contactos al archivo CSV según sea necesario.
    """
    if contactos is None:
        # Cargar todos los contactos desde el archivo CSV a una lista
        contactos = []
        with open(ruta_csv, 'r', newline='') as archivo_csv:
            lector_csv = csv.DictReader(archivo_csv)
            for fila in lector_csv:
                contactos.append(fila)
        return contactos
    else:
        # Guardar la lista de contactos al archivo CSV
        with open(ruta_csv, 'w', newline='') as archivo_csv:
            encabezados = ["id_contacto", "nombre", "email"]
            escritor_csv = csv.DictWriter(archivo_csv, fieldnames=encabezados)
            escritor_csv.writeheader()
            escritor_csv.writerows(contactos)


def guardar_contacto_en_csv(contacto: Contacto, ruta_csv: str = 'contactos.csv'):
    # Abre el archivo CSV en modo de lectura para obtener el último id_contacto
    with open(ruta_csv, 'r', newline='') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        # Ignora la primera fila (encabezado)
        next(lector_csv, None)
        # Encuentra el último id_contacto existente
        ultimo_id_contacto = max([int(fila[0]) for fila in lector_csv], default=0)

    # Incrementa el id_contacto
    nuevo_id_contacto = ultimo_id_contacto + 1

    # Abre el archivo CSV en modo de escritura (append)
    with open(ruta_csv, 'a', newline='') as archivo_csv:
        # Crea un escritor CSV
        escritor_csv = csv.writer(archivo_csv)

        # Escribe la nueva fila en el archivo CSV
        escritor_csv.writerow([nuevo_id_contacto, contacto.nombre, contacto.email])

def eliminar_contacto_por_id(id_contacto: int, ruta_csv: str = 'contactos.csv'):
    """
    Elimina un contacto por su id del archivo CSV.
    """
    # Cargar todos los contactos
    contactos = cargar_guardar_contactos(ruta_csv=ruta_csv)

    # Verificar si el contacto existe
    contactos_filtrados = [contacto for contacto in contactos if contacto["id_contacto"] == str(id_contacto)]

    if not contactos_filtrados:
        raise HTTPException(status_code=404, detail=f"No se encontró el contacto con id {id_contacto}")

    # Filtrar los contactos que no coinciden con el id_contacto
    contactos = [contacto for contacto in contactos if contacto["id_contacto"] != str(id_contacto)]

    # Guardar la lista actualizada de contactos al archivo CSV
    cargar_guardar_contactos(contactos=contactos, ruta_csv=ruta_csv)

def modificar_contacto(id_contacto: int, nuevo_nombre: str, nuevo_email: str, ruta_csv: str = 'contactos.csv'):
    """
    Modifica un contacto por su id en el archivo CSV.
    """
    # Cargar todos los contactos
    contactos = cargar_guardar_contactos(ruta_csv=ruta_csv)

    # Verificar si el contacto existe
    contactos_filtrados = [contacto for contacto in contactos if contacto["id_contacto"] == str(id_contacto)]

    if not contactos_filtrados:
        print(f"No se encontró el contacto con id {id_contacto}")
        raise HTTPException(status_code=404, detail=f"No se encontró el contacto con id {id_contacto}")

    # Modificar el contacto
    for contacto in contactos:
        if contacto["id_contacto"] == str(id_contacto):
            contacto["nombre"] = nuevo_nombre
            contacto["email"] = nuevo_email

    # Guardar la lista actualizada de contactos al archivo CSV
    cargar_guardar_contactos(contactos=contactos, ruta_csv=ruta_csv)

    print(f"Contacto con id {id_contacto} modificado exitosamente")


app = FastAPI()

@app.get(
    "/", 
    status_code=status.HTTP_200_OK,
    summary="Endpoint Raiz"
    )
def root():
    """ 
    # Endpoint raiz
    ## Status codes
    * 289 - Codigo de confirmacion
    * 301 - Codigo de status
    """
    return {"message":"Holamundo"}

@app.get("/v1/contactos",
    status_code=status.HTTP_200_OK,
    summary="Endpoint todos los contactos")
def read_contactos():
    """
    # Endpoint para obtener todos los contactos
    ## Status codes
    * 289 - Codigo de confirmacion
    * 301 - Codigo de status
    """
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

    # Devuelve la lista de datos_csv como una respuesta JSON en bruto
    return datos_csv

@app.get("/v1/contactos/{nombre}",
    status_code=status.HTTP_200_OK,
    summary="Endpoint contactos obtener por nombre")
def read_contactos_nombre(nombre: str):
    """
    # Endpoint para obtener contactos por nombre
    ## Status codes
    * 289 - Codigo de confirmacion
    * 301 - Codigo de status
    """
    # Crear una lista para almacenar los datos CSV
    datos_csv = []

    # Abre el archivo CSV en modo lectura
    with open('contactos.csv', 'r', newline='') as archivo_csv:
        lector_csv = csv.DictReader(archivo_csv)

        # Itera sobre las filas del archivo CSV
        for fila in lector_csv:
            # Verifica si el valor en la columna 'nombre' contiene el valor proporcionado
            if nombre.lower() in fila['nombre'].lower():
                # Agrega la fila actual como un diccionario a la lista
                datos_csv.append(fila)

    # Verifica si se encontraron contactos
    if len(datos_csv) == 0:
        # Devuelve un mensaje de error o aviso
        raise HTTPException(status_code=429, detail="No se encontraron contactos con el nombre proporcionado")

    # Devuelve la lista de datos_csv
    return datos_csv


@app.post("/v1/contactos/",
    status_code=status.HTTP_200_OK,
    summary="Endpoint para crear contactos")
async def create_item(contacto: Contacto):
    # Guardar el contacto en el archivo CSV
    guardar_contacto_en_csv(contacto)
    return {"mensaje": "Contacto guardado exitosamente", "contacto_guardado": contacto.dict()}

@app.delete("/v1/contactos/{id_contacto}")
async def eliminar_contacto(id_contacto: int):
    
    # Intenta eliminar el contacto
    eliminar_contacto_por_id(id_contacto)
    return {"mensaje": f"Contacto con id {id_contacto} eliminado exitosamente"}

@app.put("/v1/contactos/{id_contacto}")
async def modificar_contacto_api(id_contacto: int, nuevo_nombre: str, nuevo_email: str):
    # Intenta modificar el contacto
    modificar_contacto(id_contacto, nuevo_nombre, nuevo_email)
    return {"mensaje": f"Contacto con id {id_contacto} modificado exitosamente"}

