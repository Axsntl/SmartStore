# ===================================================================================================================================================
# Esto es para el servidor FastAPI asi bien maquiavelico por q no se como hacer un servidor de FastAPI en el mismo archivo pero tengo libre albedrio
# ===================================================================================================================================================

from fastapi import FastAPI, UploadFile, File, Form, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import shutil, os

from db import get_db
from models import ProductModel
from pydantic import BaseModel

app = FastAPI()

# Middleware CORS (necesario para conexión desde Flet u otros)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto si quieres restringir por seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carpeta para archivos multimedia
UPLOAD_DIR = "media"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Servir archivos estáticos desde /media/
app.mount("/media", StaticFiles(directory=UPLOAD_DIR), name="media")

# -------------------- #
# MODELO DE PRODUCTO   #
# -------------------- #
class Product(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    categoria: str
    stock: int
    imagen: str
    video: str | None = None

# ------------------------ #
# ENDPOINT: SUBIR ARCHIVO #
# ------------------------ #
@app.post("/upload/")
async def upload_file(archivo: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, archivo.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(archivo.file, f)
    archivo_url = f"http://127.0.0.1:8000/media/{archivo.filename}"
    return {"archivo_url": archivo_url}

# ---------------------------- #
# ENDPOINT: PUBLICAR PRODUCTO #
# ---------------------------- #
@app.post("/productos/")
async def crear_producto(producto: Product, db: Session = Depends(get_db)):
    nuevo_producto = ProductModel(
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio=producto.precio,
        categoria=producto.categoria,
        stock=producto.stock,
        imagen_path=producto.imagen,
        video_path=producto.video
    )
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return JSONResponse(status_code=200, content={"mensaje": "Producto publicado correctamente"})
