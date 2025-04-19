import flet as ft

def LoginScreen(page):
    email = ft.TextField(label="Correo electrónico", width=300)
    password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    error_text = ft.Text(value="", color="red")
    registro_link = ft.TextButton("¿No tienes cuenta? Regístrate aquí", on_click=lambda e: page.go("/register"))

    def iniciar_sesion(e):
        if not email.value or not password.value:
            error_text.value = "Todos los campos son obligatorios."
        else:
            error_text.value = ""
            # Aquí puedes agregar autenticación real
            print("Iniciando sesión con:", email.value)
            # page.go("/home") luego

        page.update()

    return ft.View(
        route="/login",
        controls=[
            ft.Container(
                ft.Column([
                    ft.Image(src="core/assets/icons/SSICON.png", width=100, height=100),
                    ft.Text("Iniciar Sesión", size=24, weight="bold"),
                    email,
                    password,
                    ft.ElevatedButton("Entrar", on_click=iniciar_sesion),
                    error_text,
                    ft.ElevatedButton("Regístrate", on_click=lambda e: page.go("/register")),
                    registro_link
                ],
                alignment="center",
                horizontal_alignment="center",
                expand=True),
            alignment=ft.alignment.center,
            expand=True                
            )
        ]
    )
