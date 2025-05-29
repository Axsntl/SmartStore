import flet as ft
import requests
import os
import screens.auth as auth
def ProductUploadView(page: ft.Page):
    # Controles
    nombre_ctrl = ft.TextField(label="Nombre del producto", width=400)
    descripcion_ctrl = ft.TextField(label="Descripción", multiline=True, width=400)
    precio_ctrl = ft.TextField(label="Precio", width=200)
    stock_ctrl = ft.TextField(label="Stock disponible", width=200)
    categoria_ctrl = ft.Dropdown(
        label="Categoría",
        options=[
            ft.dropdown.Option("Comidas"),
            ft.dropdown.Option("Bebidas"),
            ft.dropdown.Option("Postres"),
            ft.dropdown.Option("Otros"),
        ],
        width=300,
    )

    imagen_picker = ft.FilePicker()
    video_picker = ft.FilePicker()
    imagen_path = ft.Text(value="", visible=False)
    video_path = ft.Text(value="", visible=False)

    def show_snackbar(msg, color=ft.Colors.BLUE):
        page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=color)
        page.snack_bar.open = True
        page.update()

    def pick_imagen(e):
        imagen_picker.pick_files(allow_multiple=False, allowed_extensions=["jpg", "jpeg", "png"])

    def pick_video(e):
        video_picker.pick_files(allow_multiple=False, allowed_extensions=["mp4", "mov"])

    def on_imagen_picked(e: ft.FilePickerResultEvent):
        if e.files:
            imagen_path.value = e.files[0].path
            show_snackbar("Imagen seleccionada")

    def on_video_picked(e: ft.FilePickerResultEvent):
        if e.files:
            video_path.value = e.files[0].path
            show_snackbar("Video seleccionado")

    imagen_picker.on_result = on_imagen_picked
    video_picker.on_result = on_video_picked

    def subir_archivo(local_path):
        """Sube un archivo a /upload/ y retorna la URL."""
        try:
            with open(local_path, "rb") as f:
                response = requests.post(
                    "http://127.0.0.1:8000/upload/",
                    files={"archivo": f}
                )
                if response.status_code == 200:
                    return response.json()["archivo_url"]
        except Exception as e:
            show_snackbar(f"Error al subir archivo: {e}", color=ft.Colors.RED)
        return None

    def publicar_producto(e):
        # Validación
        if not all([
            nombre_ctrl.value, descripcion_ctrl.value,
            precio_ctrl.value, stock_ctrl.value,
            categoria_ctrl.value, imagen_path.value
        ]):
            show_snackbar("Todos los campos excepto el video son obligatorios", color=ft.Colors.RED)
            return

        # Subir imagen y video
        imagen_url = subir_archivo(imagen_path.value)
        video_url = subir_archivo(video_path.value) if video_path.value else None

        if not imagen_url:
            show_snackbar("Error al subir imagen", color=ft.Colors.RED)
            return

        # Crear el producto
        producto = {
            "nombre": nombre_ctrl.value,
            "descripcion": descripcion_ctrl.value,
            "precio": float(precio_ctrl.value),
            "stock": int(stock_ctrl.value),
            "categoria": categoria_ctrl.value,
            "imagen": imagen_url,
            "video": video_url,
            "vendedor_id": auth.usuario_actual["id"]  # Enlace con el usuario
        }

        try:
            response = requests.post("http://127.0.0.1:8000/productos/", json=producto)
            if response.status_code == 200:
                show_snackbar("Producto publicado correctamente", color=ft.Colors.GREEN)
            else:
                show_snackbar("Error al registrar el producto", color=ft.Colors.RED)
        except Exception as ex:
            show_snackbar(f"Error de conexión: {ex}", color=ft.Colors.RED)

    return ft.View(
        route="/sell",
        controls=[
            imagen_picker,
            video_picker,
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Publicar nuevo producto", size=24, weight=ft.FontWeight.BOLD),
                        nombre_ctrl,
                        descripcion_ctrl,
                        ft.Row([precio_ctrl, stock_ctrl]),
                        categoria_ctrl,
                        ft.Row([
                            ft.ElevatedButton("Seleccionar imagen", on_click=pick_imagen, icon=ft.Icons.IMAGE),
                            ft.ElevatedButton("Seleccionar video", on_click=pick_video, icon=ft.Icons.VIDEO_FILE),
                        ]),
                        ft.ElevatedButton("Publicar producto", on_click=publicar_producto, icon=ft.Icons.UPLOAD),
                        ft.ElevatedButton("Volver", on_click=lambda _: page.go("/home"), icon=ft.Icons.ARROW_BACK)
                    ],
                    spacing=15,
                ),
                padding=30,
                alignment=ft.alignment.center,
            )
        ]
    )