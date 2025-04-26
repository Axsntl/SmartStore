from sqlalchemy import Column, Integer, String, Float, Text, Numeric, TIMESTAMP
from db import Base
#Una breve explicación de lo que es models es que models se refiere a los modelos de la base de datos, la manera en que se guardan los datos en la base de datos,
#Pues en la base de datos es de esa forma osea id=column se guardo como integrer, osea un entero.
class ProductModel(Base):
    # Primero se escribe a que tabla se va a enlazar, en este caso productos.
    __tablename__ = "productos"
    # Luego se definen los campos de la tabla, en este caso id, nombre, descripcion, precio, categoria, stock, imagen_path y video_path.
    # NOTA: Tener en cuenta que se deben de especificar que tipo de datos se deben subir y que deben los mismos que se encuentran en la base de datos o al menos que sean compatibles.
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    precio = Column(Numeric(10, 2), nullable=False)
    categoria = Column(String(50))
    stock = Column(Integer, default=0)
    imagen_path = Column(Text)
    video_path = Column(Text)
    fecha_publicacion = Column(TIMESTAMP)
    vendedor_id = Column(Integer)  # NOTA: Sin usar Aun
