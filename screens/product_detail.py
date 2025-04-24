import flet as ft
import requests
#Aun por arreglar
def ProductDetailView(page: ft.Page, product_id: int):
    contenido = ft.Column(scroll=ft.ScrollMode.AUTO)

    def cargar_detalle():
        try:
            response = requests.get(f"http://127.0.0.1:8000/productos/{product_id}")
            if response.status_code == 200:
                producto = response.json()

                contenido.controls.extend([
                    ft.Text(producto["nombre"], size=24, weight=ft.FontWeight.BOLD),
                    ft.Image(src=producto["imagen_path"], width=300, height=300),
                    ft.Text(f"Descripción: {producto['descripcion']}"),
                    ft.Text(f"Precio: ${producto['precio']:.2f}", color=ft.colors.CYAN_200),
                    ft.Text(f"Categoría: {producto['categoria']}"),
                    ft.Text(f"Stock disponible: {producto['stock']}"),
                ])

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
                contenido.controls.append(ft.Text("No se encontró el producto.", color=ft.colors.RED))
        except Exception as e:
            contenido.controls.append(ft.Text(f"Error al cargar producto: {e}", color=ft.colors.RED))

        page.update()

    cargar_detalle()

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
