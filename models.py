from sqlalchemy import Column, Integer, String, Float, Text, Numeric, TIMESTAMP
from db import Base

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
    vendedor_id = Column(Integer)  # Esto lo puedes enlazar a usuarios después
