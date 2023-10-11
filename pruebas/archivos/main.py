from typing import Annotated
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import os
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

upload_folder = "static"

@app.post("/uploadfiles/")
async def create_upload_files(
    files: Annotated[list[UploadFile], File(description="Multiple files as UploadFile")]
):
    saved_files = []
    for file in files:
        file_extension = file.filename.split(".")[-1]
        if file.content_type == "application/pdf":
            subfolder = "pdf"
            
        elif file.content_type.startswith("image/"):
            subfolder = "images"
            
        else:
            subfolder = "other"
        
        file_path = os.path.join(upload_folder, subfolder, file.filename)
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        
        saved_files.append(file.filename)


        localhost = 'https://8000-erickghz-apirestcontact-oqkax5z2oex.ws-us105.gitpod.io/static'
        ruta = f"{localhost}/{subfolder}/{file.filename}"
        
    return {"message": "Archivos guardados correctamente", "saved_files": ruta}

@app.get("/")
async def main():
    content = """
<body>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
