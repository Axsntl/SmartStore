import psycopg2

# Conexión a la base de datos PostgreSQL
def conectar():
    return psycopg2.connect(
        dbname="SmartStore",
        user="postgres",        # Reemplaza por tu usuario de PostgreSQL
        password="1406", # Reemplaza por tu contraseña
        host="localhost",         # O la IP del servidor si está en red
        port=5432
    )

# Función para registrar un nuevo usuario
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

# Función para verificar el login
def verificar_usuario(email, contraseña):
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT * FROM usuarios WHERE email = %s AND contraseña = %s",
            (email, contraseña)
        )
        return cur.fetchone() is not None
    except Exception as e:
        print("Error al verificar:", e)
        return False
    finally:
        cur.close()
        conn.close()
