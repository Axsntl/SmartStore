import flet as ft
from db import verificar_usuario, obtener_usuario_por_email
from screens.auth import set_usuario_activo

def LoginScreen(page: ft.Page):
    email = ft.TextField(label="Correo electrónico", width=300)
    password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    error_text = ft.Text(value="", color="red")
    registro_link = ft.TextButton(
        "¿No tienes cuenta? Regístrate aquí",
        on_click=lambda e: page.go("/register")
    )

    def iniciar_sesion(e):
        # Validación de campos
        if not email.value or not password.value:
            error_text.value = "Todos los campos son obligatorios."
            page.update()
            return

        # Verificar credenciales
        usuario = verificar_usuario(email.value, password.value)
        if usuario:
            # usuario es un dict {'id':..., 'nombre':...}
            set_usuario_activo({
                "id": usuario["id"],
                "nombre": usuario["nombre"]
            })
            page.go("/home")
        else:
            error_text.value = "Usuario o contraseña incorrectos."
        
        page.update()

    return ft.View(
        route="/login",
        controls=[
            ft.Container(
                ft.Column(
                    [
                        ft.Image(src="core/assets/icons/SSICON.png", width=100, height=100),
                        ft.Text("Iniciar Sesión", size=24, weight="bold"),
                        email,
                        password,
                        ft.ElevatedButton("Entrar", on_click=iniciar_sesion),
                        error_text,
                        registro_link
                    ],
                    alignment="center",
                    horizontal_alignment="center",
                    expand=True
                ),
                alignment=ft.alignment.center,
                expand=True
            )
        ]
    )
