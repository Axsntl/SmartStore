# ===================================================================================================================================================
# Esto es para el servidor FastAPI asi bien maquiavelico por q no se como hacer un servidor de FastAPI en el mismo archivo pero tengo libre albedrio
# ===================================================================================================================================================

#Aparentemente no se puede hacer un servidor FastAPI en el mismo archivo que el de Flet, por lo que se hace un servidor FastAPI independiente
#Ademas, se tienen que definir el get y el post, si no no se puede hacer el post de los productos, y tampoco se puede hacer el get de los productos. Un poco evidende, pero bueno.
# No era tan dificil hacer el servidor
# NOTA: uvicorn no se menciona pero es necesario para correr el servidor FastAPI. Se usa uvicorn para correr el servidor FastAPI, y se usa el comando uvicorn server:app --reload para correr el servidor. El --reload es para que se recargue automaticamente cuando se hacen cambios en el codigo. Se puede cambiar por --host
# Para cerrar el servidor, se puede usar Ctrl + C en la terminal donde se esta ejecutando el servidor.
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
    allow_origins=["*"],  # Cambiar esto para restringir por seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carpeta para archivos multimedia
UPLOAD_DIR = "media" # Cambiar a la ruta deseada, pero dentro de la carpeta del proyecto, osea solo se crea otra carpeta y se cambia media por el nombre de la carpeta deseada.
os.makedirs(UPLOAD_DIR, exist_ok=True)# Crear la carpeta si no existe

# Servir archivos estáticos desde /media/
app.mount("/media", StaticFiles(directory=UPLOAD_DIR), name="media")

# --------------------------- #
# *CLASE* DE PRODUCTO :00000  #
# --------------------------- #
class Product(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    categoria: str
    stock: int
    imagen: str
    video: str | None = None
    vendedor_id: int

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
        video_path=producto.video,
        vendedor_id=producto.vendedor_id  # <-- AGREGADO
    )
    # Guardar el producto en la base de datos
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
#NOTA: En Requests existen funciones como GET, POST, PUT, DELETE, PATCH, OPTIONS y HEAD. GET es para obtener datos, POST es para enviar datos, PUT es para actualizar datos, DELETE es para eliminar datos, PATCH es para actualizar parcialmente datos, OPTIONS es para obtener las opciones de un recurso y HEAD es para obtener los encabezados de una respuesta sin el cuerpo.
# En este caso, se usan GET y POST para obtener y enviar datos respectivamente.
#Tener en cuenta el Delete para mas adelante, ya que se puede usar para eliminar productos de la base de datos.
# Por si acaso, ENDPOINT se refiere a un punto de acceso a la API, y en este caso se usan los endpoints /upload/ y /productos/ para subir y obtener productos respectivamente.

class StockUpdate(BaseModel):
    delta: int

@app.patch("/productos/{producto_id}/stock")
def actualizar_stock(producto_id: int, data: StockUpdate, db: Session = Depends(get_db)):
    """
    Recibe {"delta": -1} o {"delta": 1} para restar o sumar al stock.
    """
    delta = data.delta
    # Busca el producto
    producto = db.query(ProductModel).filter(ProductModel.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    # Ajusta stock
    nuevo_stock = producto.stock + delta
    if nuevo_stock < 0:
        raise HTTPException(status_code=400, detail="Stock insuficiente")
    producto.stock = nuevo_stock
    db.commit()
    return {"id": producto_id, "stock": producto.stock}
#Si esto es solo en python, no me imagino el dolor de cabeza que tiene que ser en otros lenguajes.

#Damn, con esto ya va el get, el post y el patch, ahora solo falta el delete y ya esta.

#Ahora se hara para finalizar el CRUD de productos, se hara el DELETE para eliminar productos de la base de datos.
#Con esto se puede hacer un CRUD completo de productos, y se puede usar para crear una tienda online completa, o al menos una parte de ella.
#El flujo de datos esta completo.
# ---------------------------- #
# ENDPOINT PARA ELIMINAR PRODUCTOS #
# ---------------------------- #
@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    """
    Elimina un producto de la base de datos.
    """
    # Busca el producto
    producto = db.query(ProductModel).filter(ProductModel.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    # Elimina el producto
    db.delete(producto)
    db.commit()
    return {"mensaje": "Producto eliminado correctamente"}
# ---------------------------- #
# ENDPOINT: OBTENER PRODUCTOS DE UN VENDEDOR #
# ---------------------------- #
@app.get("/mis_productos/{vendedor_id}")
def obtener_mis_productos(vendedor_id: int, db: Session = Depends(get_db)):
    productos = db.query(ProductModel).filter(ProductModel.vendedor_id == vendedor_id).all()
    return [
        {
            "id": p.id,
            "nombre": p.nombre,
            "descripcion": p.descripcion,
            "precio": float(p.precio),
            "stock": p.stock,
            "categoria": p.categoria,
            "imagen_path": p.imagen_path,
            "video_path": p.video_path,
            "vendedor_id": p.vendedor_id,
        }
        for p in productos
    ]
    # La parte agregada es para obtener los productos del vendedor logueado. Se supone que half life 3 saldra pronto, espero que sea cierto.
    #Ya se agregaron mas lineas, mas de lo que esperaba, pero bueno, al menos ya esta el CRUD completo de productos.

from pydantic import BaseModel

class DescripcionUpdate(BaseModel):
    descripcion: str

@app.patch("/productos/{producto_id}/descripcion")
def actualizar_descripcion(producto_id: int, data: DescripcionUpdate, db: Session = Depends(get_db)):
    """
    Actualiza la descripción de un producto.
    """
    producto = db.query(ProductModel).filter(ProductModel.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    producto.descripcion = data.descripcion
    db.commit()
    return {"id": producto_id, "descripcion": producto.descripcion}

class PrecioUpdate(BaseModel):
    precio: float

@app.patch("/productos/{producto_id}/precio")
def actualizar_precio(producto_id: int, data: PrecioUpdate, db: Session = Depends(get_db)):
    """
    Actualiza el precio de un producto.
    """
    producto = db.query(ProductModel).filter(ProductModel.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    producto.precio = data.precio
    db.commit()
    return {"id": producto_id, "precio": float(producto.precio)}

@app.get("/productos/{producto_id}")
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(ProductModel).filter(ProductModel.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {
        "id": producto.id,
        "nombre": producto.nombre,
        "descripcion": producto.descripcion,
        "precio": float(producto.precio),
        "stock": producto.stock,
        "categoria": producto.categoria,
        "imagen_path": producto.imagen_path,
        "video_path": producto.video_path,
        "vendedor_id": producto.vendedor_id,
    }