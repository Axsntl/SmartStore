import flet as ft
import requests

def CategoriesView(page: ft.Page, categoria: str):
    productos_container = ft.Column(spacing=20, scroll=ft.ScrollMode.AUTO)

    def ver_detalle(e, prod_id):
        page.go(f"/producto/{prod_id}")

    def volver(e):
        page.go("/home")

    def cargar_productos():
        try:
            response = requests.get("http://127.0.0.1:8000/productos/")
            if response.status_code == 200:
                data = response.json()
                filtrados = [p for p in data if p.get("categoria") == categoria]
                if not filtrados:
                    productos_container.controls.append(ft.Text("No hay productos en esta categoría.", color=ft.Colors.RED))
                for producto in filtrados:
                    tarjeta = ft.Container(
                        bgcolor=ft.Colors.BLUE_900,
                        border_radius=12,
                        padding=12,
                        content=ft.Column(
                            spacing=10,
                            controls=[
                                ft.Row(
                                    spacing=20,
                                    vertical_alignment=ft.CrossAxisAlignment.START,
                                    controls=[
                                        ft.Image(
                                            src=producto.get("imagen_path", ""),
                                            width=120,
                                            height=120,
                                            fit=ft.ImageFit.CONTAIN
                                        ),
                                        ft.Column(
                                            spacing=4,
                                            controls=[
                                                ft.Text(producto.get("nombre", "Sin nombre"), size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                                ft.Text(producto.get("descripcion", "Sin descripción"), size=14, color=ft.Colors.WHITE70),
                                                ft.Text(f"Precio: ${producto.get('precio', 0):.2f}", color=ft.Colors.CYAN_200),
                                                ft.Text(f"Categoría: {producto.get('categoria', 'Sin categoría')}", color=ft.Colors.BLUE_200),
                                                ft.Text(f"Stock: {producto.get('stock', 0)}", color=ft.Colors.BLUE_100),
                                            ]
                                        )
                                    ]
                                ),
                                ft.Row(
                                    spacing=10,
                                    controls=[
                                        ft.ElevatedButton(
                                            "Ver más",
                                            icon=ft.Icons.PREVIEW,
                                            on_click=lambda e, id=producto["id"]: ver_detalle(e, id),
                                            style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600)
                                        ),
                                    ]
                                )
                            ]
                        )
                    )
                    productos_container.controls.append(tarjeta)
            else:
                productos_container.controls.append(ft.Text(f"No se pudieron cargar los productos. Código de estado: {response.status_code}", color=ft.Colors.RED))
        except Exception as e:
            productos_container.controls.append(ft.Text(f"Error al conectar con el servidor: {e}", color=ft.Colors.RED))

    cargar_productos()

    return ft.View(
        route=f"/categories/{categoria}",
        controls=[
            ft.Container(
                bgcolor=ft.Colors.BLACK,
                expand=True,
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Row([
                            ft.ElevatedButton(
                                "Volver",
                                icon=ft.Icons.ARROW_BACK,
                                on_click=volver,
                                style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_700)
                            ),
                            ft.Text(
                                f"Categoría: {categoria}",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.CYAN_200
                            ),
                        ], alignment=ft.MainAxisAlignment.START, spacing=20),
                        ft.Container(
                            content=productos_container,
                            padding=20,
                            expand=True,
                            bgcolor=ft.Colors.BLACK
                        )
                    ]
                )
            )
        ]
    )