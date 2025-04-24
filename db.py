# db.py
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Configuración para psycopg2 (registro, login)
def conectar():
    return psycopg2.connect(
        dbname="SmartStore",
        user="postgres",
        password="1406",
        host="localhost",
        port=5432
    )

# Funciones con psycopg2
def registrar_usuario(nombre, email, contraseña):
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO usuarios (nombre, email, contraseña) VALUES (%s, %s, %s)",
            (nombre, email, contraseña)
        )
        conn.commit()
        return True
    except Exception as e:
        print("Error al registrar:", e)
        return False
    finally:
        cur.close()
        conn.close()

def verificar_usuario(email, contraseña):
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, nombre FROM usuarios WHERE email = %s AND contraseña = %s",#Se cambio el codigo para que solo seleccione lo necesario.
            (email, contraseña)
        )
        resultado = cur.fetchone()
        if resultado:
            return resultado  # Devuelve un tuple con (id, nombre)
        return None  # Devuelve None si no se encuentra el usuario
    except Exception as e:
        print("Error al verificar:", e)
        return False
    finally:
        cur.close()
        conn.close()

# Configuración para SQLAlchemy (uso en FastAPI)
DATABASE_URL = "postgresql://postgres:1406@localhost:5432/SmartStore"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ✅ Esta función ahora sí puede ser importada por server.py
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    