#La función main() es el punto de entrada de la aplicación. Aquí se inicializa la página y se configuran las rutas.
#Dicho de otra forma, es el corazón de la aplicación. En este caso, se utiliza la librería Flet para crear una interfaz gráfica de usuario (GUI) en Python.
import flet as ft
#Aqui se importan las pantallas del programa
from screens.splash import SplashScreen
from screens.login import LoginScreen
from screens.register import RegisterScreen
from screens.home import HomeView
from screens.productupload import ProductUploadView
from screens.product_detail import ProductDetailView
from screens.cart import VistaCarrito
def main(page: ft.Page):
    page.title = "SmartStore"
    page.window_full_screen = True  # Deshabilitar pantalla completa para usar resolución fija. Nota: Se supone que eso haria pero a la hora de ejecutar el programa no afecta nada. Quiza sea cosa de mi computadora.
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.window_frameless = True
    page.window_always_on_top = True
    # Controlador de navegación. Aqui se manejan las rutas de la aplicación. 
    # Cada vez que se cambia la ruta, se actualiza la vista correspondiente con la función route_change.
    def route_change(e):
        page.views.clear()
        # Aquí se agregan las pantallas de la interfaz gráica según la ruta seleccionada.
        # Para añadir una nueva pantalla, solo hay que agregar un nuevo elif page.route == "/ruta" y page.views.append(NombreDeLaPantalla(page))
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
        elif page.route.startswith("/producto/"):
            product_id = int(page.route.split("/")[-1])
            from screens.product_detail import ProductDetailView
            page.views.append(ProductDetailView(page, product_id))
        elif page.route == "/cartview":
            page.views.append(VistaCarrito(page))
            
        #para que la vista se vea bien al cambiar de ruta, se actualiza la página con page.update()
        page.update()
    # Se asigna la función de cambio de ruta al evento on_route_change de la página.
    page.on_route_change = route_change
    page.go("/")  # Y con esta linea se inicia la aplicación en la ruta "/".
# Esta linea ejecuta la función main() y lanza la aplicación.
ft.app(target=main)