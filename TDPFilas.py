import flet as ft

def main(page: ft.Page):
    page.title = "Resumen de como hacer filas y columnas en Flet"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
     # Se escriben las lineas de texto
    texto1 = ft.Text("Texto 1", size=20, color=ft.colors.RED)
    texto2 = ft.Text("Ejemplo de filas y columnas en Flet", size=20, color=ft.colors.RED)
    texto3 = ft.Text("Ejemplo de filas y columnas en Flet", size=20, color=ft.colors.RED)
    texto4 = ft.Text("Ejemplo de filas y columnas en Flet", size=20, color=ft.colors.RED)
    
    # Se crea el codigo para hacer las filas y columnas
    fila1 = ft.Row(
        # Se agregan los elementos a la fila
        [texto1, texto2],
        #alignment sirve para centrar los elementos en la fila
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=50
        )
    page.add(fila1)
ft.app(target=main)