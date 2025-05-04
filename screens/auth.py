# screens/auth.py
"""
Módulo para manejar estado de autenticación en memoria.
Contiene variable global 'usuario_actual' y función para actualizarla.
"""
usuario_actual = None


def set_usuario_activo(usuario):
    """
    Establece el usuario actualmente autenticado y deposita en usuario_actual.

    usuario: dict con llaves 'id' y 'nombre'.
    """
    global usuario_actual
    usuario_actual = usuario
    # DEBUG: Imprimir para verificar que se guardó
    print(f"DEBUG: usuario_actual seteado en auth: {usuario_actual}")

# Alias para compatibilidad
iniciar_sesion = set_usuario_activo
