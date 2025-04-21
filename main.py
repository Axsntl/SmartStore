import flet as ft
#Aqui se importan las pantallas del programa
from screens.splash import SplashScreen
from screens.login import LoginScreen
from screens.register import RegisterScreen
from screens.home import HomeView
from screens.productupload import ProductUploadView

def main(page: ft.Page):
    page.title = "SmartStore"
    page.window_full_screen = True  # Deshabilitar pantalla completa para usar resolución fija
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.window_frameless = True
    page.window_always_on_top = True
    # Controlador de navegación
    def route_change(e):
        page.views.clear()

        if page.route == "/":
            page.views.append(SplashScreen(page))
        elif page.route == "/login":
            page.views.append(LoginScreen(page))
        elif page.route == "/register":
            page.views.append(RegisterScreen(page))
        elif page.route == "/home":
            page.views.append(HomeView(page))
        elif page.route == "/sell":
            page.views.append(ProductUploadView(page))

        page.update()

    page.on_route_change = route_change
    page.go("/")  # inicia con splash screen

ft.app(target=main)