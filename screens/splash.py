import flet as ft
import time
import threading

def SplashScreen(page):
    def cargar_datos():
        time.sleep(5)  # Simulación de carga de datos
        page.go("/login")

    # Ejecutar la carga en segundo plano
    threading.Thread(target=cargar_datos).start()

    return ft.View(
        route="/",
        controls=[
            ft.Container(
                ft.Column([
                    ft.Image(src="core/assets/icons/SSICON.png", width=400, height=400),
                    ft.Text("Cargando...", size=20, weight="bold"),
                    ft.ProgressRing(),
                ],
                alignment="center",
                horizontal_alignment="center",
                expand=True),
            alignment=ft.alignment.center,
            expand=True,
            )
        ]
    )
