# ===================================================================================================================================================
# Esto es para el servidor FastAPI asi bien maquiavelico por q no se como hacer un servidor de FastAPI en el mismo archivo pero tengo libre albedrio
# ===================================================================================================================================================

#Aparentemente no se puede hacer un servidor FastAPI en el mismo archivo que el de Flet, por lo que se hace un servidor FastAPI independiente
#Ademas, se tienen que definir el get y el post, si no no se puede hacer el post de los productos, y tampoco se puede hacer el get de los productos. Un poco evidende, pero bueno.
from fastapi import FastAPI, UploadFile, File, Form, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import shutil, os

from db import get_db
from models import ProductModel
#Models se refiere a los modelos de la base de datos, y db se refiere a la base de datos en si. En este caso, se usa SQLAlchemy para la base de datos, y psycopg2 para la conexion a la base de datos.
from pydantic import BaseModel
#pydantic se refiere a la libreria para validar los modelos de la base de datos, y BaseModel se refiere a la clase base para los modelos de la base de datos.
# Esta es la configuración de FastAPI para el servidor para la subida de archivos y descarga de archivos. Con APP=FastAPI() se crea el servidor FastAPI, y con app.add_middleware se añade el middleware CORS para permitir conexiones desde otros dominios. Con app.mount se monta la carpeta media para servir archivos estáticos desde /media/. Se hizo largo el texto pero creo que sera mejor dejarlo asi solo por que se me ocurrio.
from fastapi import HTTPException
#HTTPException se refiere a la excepcion de HTTP, y se usa para manejar errores en la aplicacion.
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

# --------------------- #
# CLASE DE PRODUCTO :0  #
# --------------------- #
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

#Me falto el GET
# ---------------------------- #
#ENDPOINT PARA OBTENER PRODUCTOS#
# ---------------------------- #
@app.get("/productos/")
def obtener_productos(db: Session = Depends(get_db)):
    productos = db.query(ProductModel).all()
    return [
        {
            "id": p.id,  # Agregar el campo id
            "nombre": p.nombre,
            "descripcion": p.descripcion,
            "precio": float(p.precio),
            "stock": p.stock,
            "categoria": p.categoria,
            "imagen_path": p.imagen_path,
            "video_path": p.video_path,
        }
        for p in productos
    ]
#FASTAPI fue creado por Sebastian Ramirez un Colombiano