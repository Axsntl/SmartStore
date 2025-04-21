# ===================================================================================================================================================
# Esto es para el servidor FastAPI asi bien maquiavelico por q no se como hacer un servidor de FastAPI en el mismo archivo pero tengo libre albedrio
# ===================================================================================================================================================

from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import psycopg2
import os
from uuid import uuid4

app = FastAPI()

# =========================
# Configuración de archivos
# =========================
UPLOAD_DIR = "media"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/media", StaticFiles(directory=UPLOAD_DIR), name="media")

# =========================
# Modelo del producto
# =========================
class Product(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    stock: int
    categoria: str
    imagen: str
    video: Optional[str] = None

# =========================
# Conexión a la base de datos
# =========================
def get_db_connection():
    conn = psycopg2.connect(
        dbname="SmartStore",
        user="postgres",
        password="1406",
        host="localhost",
        port=5432
    )
    return conn

# =========================
# Subida de archivos
# =========================
@app.post("/upload/")
async def subir_archivo(archivo: UploadFile = File(...)):
    ext = archivo.filename.split('.')[-1]
    nuevo_nombre = f"{uuid4()}.{ext}"
    archivo_path = os.path.join(UPLOAD_DIR, nuevo_nombre)

    with open(archivo_path, "wb") as f:
        content = await archivo.read()
        f.write(content)

    return {"archivo_url": f"/media/{nuevo_nombre}"}

# =========================
# Agregar producto
# =========================
@app.post("/productos/")
async def agregar_producto(producto: Product):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO productos (nombre, descripcion, precio, stock, categoria, imagen, video)
        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
    ''', (
        producto.nombre,
        producto.descripcion,
        producto.precio,
        producto.stock,
        producto.categoria,
        producto.imagen,
        producto.video
    ))

    producto_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()

    return {"mensaje": "Producto agregado con éxito", "producto_id": producto_id, "producto": producto.dict()}
