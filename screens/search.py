import flet as ft
import requests
from screens.cart import agregar_al_carrito
from screens.home import mostrar_snackbar

def SearchView(page: ft.Page, query: str):
    productos_container = ft.Column(spacing=20, scroll=ft.ScrollMode.AUTO)

    def cargar_resultados():
        try:
            response = requests.get("http://127.0.0.1:8000/productos/")
            if response.status_code == 200:
                data = response.json()
                resultados = [
                    p for p in data if query.lower() in p.get("nombre", "").lower() or query.lower() in p.get("descripcion", "").lower()
                ]
                if not resultados:
                    productos_container.controls.append(ft.Text("No se encontraron productos.", color=ft.Colors.RED))
                for producto in resultados:
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
                                                ft.Text(producto.get("nombre", "Sin nombre"), size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                                                ft.Text(producto.get("descripcion", "Sin descripción"), size=14, color=ft.colors.WHITE70),
                                                ft.Text(f"Precio: ${producto.get('precio', 0):.2f}", color=ft.Colors.CYAN_200),
                                                ft.Text(f"Categoría: {producto.get('categoria', 'Sin categoría')}", color=ft.colors.BLUE_200),
                                                ft.Text(f"Stock: {producto.get('stock', 0)}", color=ft.colors.BLUE_100),
                                            ]
                                        )
                                    ]
                                ),
                                ft.Row(
                                    spacing=10,
                                    controls=[
                                        ft.ElevatedButton(
                                            "Agregar al carrito",
                                            icon=ft.icons.ADD_SHOPPING_CART,
                                            on_click=lambda e, p=producto: (
                                                agregar_al_carrito(p),
                                                mostrar_snackbar(page, f"{p['nombre']} agregado al carrito.")
                                            ),
                                            style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_GREY_600)
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                    productos_container.controls.append(tarjeta)
            else:
                productos_container.controls.append(ft.Text("No se pudieron cargar los productos.", color=ft.Colors.RED))
        except Exception as e:
            productos_container.controls.append(ft.Text(f"Error al conectar con el servidor: {e}", color=ft.Colors.RED))

    cargar_resultados()

    return ft.View(
        route=f"/search/{query}",
        controls=[
            ft.Container(
                bgcolor=ft.Colors.BLACK,
                expand=True,
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Text(f"Resultados para: '{query}'", size=20, color=ft.Colors.WHITE),
                                    ft.ElevatedButton(
                                        "Volver al inicio",
                                        icon=ft.Icons.ARROW_BACK,
                                        on_click=lambda e: page.go("/home"),
                                        style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE)
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            padding=ft.padding.symmetric(horizontal=12, vertical=10),
                            bgcolor=ft.Colors.BLACK,
                        ),
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