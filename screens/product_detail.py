import flet as ft
import requests
from screens.cart import agregar_al_carrito

def ProductDetailView(page: ft.Page, product_id: int):
    contenido = ft.Column(scroll=ft.ScrollMode.AUTO)
    producto_data = {}

    def cargar_detalle():
        nonlocal producto_data
        try:
            response = requests.get(f"http://127.0.0.1:8000/productos/{product_id}")
            if response.status_code == 200:
                producto = response.json()
                producto_data = producto  # Guarda para los botones
                contenido.controls.append(
                    ft.Text(producto.get("nombre", "Sin nombre"), size=24, weight=ft.FontWeight.BOLD)
                )

                if producto.get("imagen_path"):
                    contenido.controls.append(
                        ft.Image(src=producto["imagen_path"], width=300, height=300)
                    )

                contenido.controls.append(
                    ft.Text(f"Descripción: {producto.get('descripcion', '')}")
                )
                contenido.controls.append(
                    ft.Text(f"Precio: ${float(producto.get('precio', 0)):.2f}", color=ft.Colors.CYAN_200)
                )
                contenido.controls.append(
                    ft.Text(f"Categoría: {producto.get('categoria', '')}")
                )
                contenido.controls.append(
                    ft.Text(f"Stock disponible: {producto.get('stock', 0)}")
                )

                if producto.get("video_path"):
                    contenido.controls.extend([
                        ft.Text("Video del producto:"),
                        ft.Video(
                            src=producto["video_path"],
                            width=400,
                            autoplay=False,
                            controls=True
                        )
                    ])
            else:
                contenido.controls.append(ft.Text("No se encontró el producto.", color=ft.Colors.RED))
        except Exception as e:
            contenido.controls.append(ft.Text(f"Error al cargar producto: {e}", color=ft.Colors.RED))

        page.update()

    def handle_comprar_ahora(e):
        if producto_data:
            agregar_al_carrito(producto_data)
            page.go("/cart")

    def handle_agregar_carrito(e):
        if producto_data:
            agregar_al_carrito(producto_data)
            page.snack_bar = ft.SnackBar(ft.Text("Producto agregado al carrito"), bgcolor=ft.Colors.GREEN)
            page.snack_bar.open = True
            page.update()

    def handle_volver(e):
        page.go("/home")

    cargar_detalle()

    # Agrega los botones al final
    contenido.controls.append(
        ft.Row(
            controls=[
                ft.ElevatedButton("Comprar ahora", icon=ft.Icons.SHOPPING_CART, on_click=handle_comprar_ahora),
                ft.ElevatedButton("Agregar al carrito", icon=ft.Icons.ADD_SHOPPING_CART, on_click=handle_agregar_carrito),
                ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=handle_volver),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

    return ft.View(
        route=f"/producto/{product_id}",
        controls=[
            ft.Container(
                content=contenido,
                padding=20,
                expand=True
            )
        ]
    )
