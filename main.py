import flet as ft
#Aqui se importan las pantallas del programa
from screens.splash import SplashScreen
from screens.login import LoginScreen
from screens.register import RegisterScreen

def main(page: ft.Page):
    page.title = "Mi App Mercado"
    page.window_width = 400
    page.window_height = 700
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    # Controlador de navegación
    def route_change(e):
        page.views.clear()

        if page.route == "/":
            page.views.append(SplashScreen(page))
        elif page.route == "/login":
            page.views.append(LoginScreen(page))
        elif page.route == "/register":
            page.views.append(RegisterScreen(page))

        page.update()

    page.on_route_change = route_change
    page.go("/")  # inicia con splash screen

ft.app(target=main)
