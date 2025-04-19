import flet as ft
import time
import threading

def SplashScreen(page):
    def cargar_datos():
        time.sleep(2)  # Simulación de carga de datos
        page.go("/login")

    # Ejecutar la carga en segundo plano
    threading.Thread(target=cargar_datos).start()

    return ft.View(
        route="/",
        controls=[
            ft.Column([
                ft.Text("Mi App Mercado", size=30, weight="bold"),
                ft.ProgressRing(),
            ],
            alignment="center",
            horizontal_alignment="center",
            expand=True)
        ]
    )
