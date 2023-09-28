# Desing Document: API REST CONTACTOS

## 1. Descripcion
Ejemplo de una API REST para gestionar contactos en una DB utilizando FastAPI.

## 2. Objetivo
Realizar un ejemplo de diseño de una API REST de tipo CRUD y su posterior codificación utilizando el framework [FastAPI](https://fastapi.tiangolo.com/).

## 3. Diseño de la BD
Para este ejemplo se utilizará el gestor de base de datos [SQLite3](https://www.sqlite.org/) con las siguientes tablas:

### 3.1 Tabla: contactos
Diseño de tabla para almacenar contactos

|No.|Campo|Tipo|Restricciones|Descripción|
|--|--|--|--|--|
|1|id_contacto|int|PRYMARY KEY|Llave primaria de la tabla|
|2|nombre|varchar(100)|Not Null|Nombre del contacto|
|3|primer_apellido|varchar(50)|Not Null|Primer Apellido del contacto|
|4|segundo_apellido|varchar(50)|Not Null|Segundo Apellido del contacto|
|5|email|varchar(100)|Not Null|Email del contacto|
|6|telefono|varchar(13)|Not Null|Telefono del contacto|

### 3.2 Script
Script para realizar tabla de contactos en [SQLite3](https://www.sqlite.org/)

CREATE TABLE IF NOT EXISTS contactos (
    id_contacto INTEGER PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    primer_apellido VARCHAR(50) NOT NULL,
    segundo_apellido VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    telefono VARCHAR(13) NOT NULL
);

## 4. Diseño del Endpoint
Diseño del end para el recurso contactos

### 4.1 Mostrar todos los contactos
Endpoint para obtener todos los contactos

|No.|Propiedad|Detalle|
|--|--|--|
|1|Description|Endpoint para obtener todos los contactos|
|2|Summary|Enpoint todos los contactos|
|3|Method|GET|
|4|Endpoint|http://localhost:8000/contactos|
|5|Query Param|?limit=10&offset=10|
|6|Path Param|NA|
|7|Data|NA|
|8|Version|v1|
|9|Status Code|200|
|10|Response type|application/json|
|11|Response|[{"id_contacto":int,"nombre":string,"apellido_paterno":string,"apellido_materno":string,"email":string,"telefono":string},{"id_contacto":int,"nombre":string,"apellido_paterno":string,"apellido_materno":string,"email":string,"telefono":string}]|
|12|Curl|curl -X "GET" "http://localhost:8000/contactos?limit=10&offset=10" -H "accept":"aplication/json"|
|13|Status Code (error)|NA|
|14|Response Type (error)|NA|
|15|Response (error)|NA|

### 4.2 Buscar contactos por nombre 
Endpoint para obtener todos los contactos por nombre

|No.|Propiedad|Detalle|
|--|--|--|
|1|Description|Endpoint para obtener contactos por nombre|
|2|Summary|Enpoint contactos por nombre|
|3|Method|GET|
|4|Endpoint|http://localhost:8000/contactos|
|5|Query Param|?limit=10&offset=10&nombre={nombre}|
|6|Path Param|NA|
|7|Data|NA|
|8|Version|v1|
|9|Status Code|202|
|10|Response type|application/json|
|11|Response|[{"id_contacto":int,"nombre":string,"apellido_paterno":string,"apellido_materno":string,"email":string,"telefono":string},{"id_contacto":int,"nombre":string,"apellido_paterno":string,"apellido_materno":string,"email":string,"telefono":string}]|
|12|Curl|curl -X "GET" "http://localhost:8000/contactos?limit=10&offset=10&nombre={nombre}" -H "accept":"aplication/json"|
|13|Status Code (error)|430|
|14|Response Type (error)|application/json|
|15|Response (error)|{"message":"Contacto no encontrado"}|
|16|Status Code (error)|432|
|17|Response Type (error)|application/json|
|18|Response (error)|{"message":"Parametro vacio"}|





