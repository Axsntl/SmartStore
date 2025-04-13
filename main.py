import flet as ft
import time
from threading import Timer

def main(page: ft.Page):
    page.title = "SmartStore"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.colors.WHITE

    # Logo placeholder
    logo = ft.Container(
        content=ft.Text("SmartStore", size=30, weight=ft.FontWeight.BOLD),
        alignment=ft.alignment.center,
        width=200,
        height=200,
        bgcolor=ft.colors.LIGHT_BLUE_100,
        border_radius=100,
    )

    # Loading icon
    loading_icon = ft.ProgressRing(width=50, height=50)

    # Start button (hidden initially)
    start_button = ft.ElevatedButton(
        text="Inicio",
        visible=False,
        on_click=lambda _: page.snack_bar.show("¡Bienvenido a SmartStore!"),
    )

    # Function to show the start button after 7 seconds
    def show_start_button():
        start_button.visible = True
        page.update()

    # Timer to delay the appearance of the start button
    Timer(7, show_start_button).start()

    # Add components to the page
    page.add(
        ft.Column(
            [
                logo,
                ft.Container(height=20),  # Spacer
                loading_icon,
                ft.Container(height=20),  # Spacer
                start_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)