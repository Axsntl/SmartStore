# db.py
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ----------------------------------------
# Configuración para psycopg2 (registro/login)
# ----------------------------------------
def conectar():
    """Establece y devuelve conexión psycopg2."""
    return psycopg2.connect(
        dbname="SmartStore",
        user="postgres",
        password="1406",
        host="localhost",
        port=5432
    )


def registrar_usuario(nombre, email, contraseña):
    """Inserta un nuevo usuario en la tabla 'usuarios'. Retorna True si tuvo éxito."""
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
        print("Error al registrar usuario:", e)
        return False
    finally:
        cur.close()
        conn.close()


def verificar_usuario(email, contraseña):
    """Verifica credenciales. Devuelve un dict {'id':..., 'nombre':...} si existen, o None."""
    conn = conectar()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(
            "SELECT id, nombre FROM usuarios WHERE email = %s AND contraseña = %s",
            (email, contraseña)
        )
        return cur.fetchone()
    except Exception as e:
        print("Error al verificar usuario:", e)
        return None
    finally:
        cur.close()
        conn.close()


def obtener_usuario_por_email(email):
    """Devuelve dict {'id', 'nombre'} o None para el usuario dado su email."""
    conn = conectar()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(
            "SELECT id, nombre FROM usuarios WHERE email = %s",
            (email,)
        )
        return cur.fetchone()
    except Exception as e:
        print("Error al obtener usuario por email:", e)
        return None
    finally:
        cur.close()
        conn.close()

# ----------------------------------------
# Configuración para SQLAlchemy (FastAPI)
# ----------------------------------------
DATABASE_URL = "postgresql://postgres:1406@localhost:5432/SmartStore"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db():
    """Generador de sesión para FastAPI Dependency Injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
