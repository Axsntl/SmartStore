from sqlalchemy import Column, Integer, String, Float, Text, Numeric, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

#Una breve explicación de lo que es models es que models se refiere a los modelos de la base de datos, la manera en que se guardan los datos en la base de datos,
#Pues en la base de datos es de esa forma osea id=column se guardo como integrer, osea un entero.
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    contraseña = Column(String(100), nullable=False)
    productos = relationship("ProductModel", back_populates="vendedor")

class ProductModel(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    precio = Column(Numeric(10, 2), nullable=False)
    categoria = Column(String(50))
    stock = Column(Integer, default=0)
    imagen_path = Column(Text)
    video_path = Column(Text)
    fecha_publicacion = Column(TIMESTAMP)
    vendedor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    vendedor = relationship("Usuario", back_populates="productos")
