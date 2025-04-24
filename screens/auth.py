# screens/auth.py
usuario_actual = None

def iniciar_sesion(usuario_id, nombre):
    global usuario_actual
    usuario_actual = {"id": usuario_id, "nombre": nombre}