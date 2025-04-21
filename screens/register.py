import flet as ft
from db import registrar_usuario

def RegisterScreen(page):
    nombre = ft.TextField(label="Nombre completo", width=300)
    email = ft.TextField(label="Correo electrónico", width=300)
    password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    confirmar = ft.TextField(label="Confirmar contraseña", password=True, can_reveal_password=True, width=300)
    error_text = ft.Text(value="", color="red")

    def crear_cuenta(e):
        if not nombre.value or not email.value or not password.value or not confirmar.value:
            error_text.value = "Por favor, completa todos los campos."
        elif password.value != confirmar.value:
            error_text.value = "Las contraseñas no coinciden."
        else:
            error_text.value = ""
            # Aquí se conectará con la base de datos más adelante
            if registrar_usuario(nombre.value, email.value, password.value):
                page.go("/login")
            else:
                error_text.value = "No se pudo registrar. ¿Correo ya en uso?"    

        page.update()

    return ft.View(
        route="/register",
        controls=[
            ft.Container(
                ft.Column([
                    ft.Image(src="core/assets/icons/SSICON.png", width=100, height=100),
                    ft.Text("Crear Cuenta", size=24, weight="bold"),
                    nombre,
                    email,
                    password,
                    confirmar,
                    ft.ElevatedButton("Registrarse", on_click=crear_cuenta),
                    error_text,
                ],
                alignment="center",
                horizontal_alignment="center",
                expand=True),
                alignment=ft.alignment.center,
                expand=True,
            )
        ]
    )
