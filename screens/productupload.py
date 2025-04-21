import flet as ft
from flet import dropdown
import requests
import os

def ProductUploadView(page: ft.Page):
    # Controles
    nombre_ctrl = ft.TextField(label="Nombre del producto", width=400)
    descripcion_ctrl = ft.TextField(label="Descripción", multiline=True, width=400)
    precio_ctrl = ft.TextField(
        label="Precio",
        width=200,
        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9.]")
    )
    categoria_ctrl = ft.Dropdown(
        label="Categoría",
        options=[
            dropdown.Option("Comidas"),
            dropdown.Option("Bebidas"),
            dropdown.Option("Postres"),
            dropdown.Option("Otros"),
        ],
        width=300
    )
    stock_ctrl = ft.TextField(
        label="Stock disponible",
        width=150,
        input_filter=ft.InputFilter(allow=True, regex_string=r"\d")
    )

    imagen_picker = ft.FilePicker()
    video_picker = ft.FilePicker()

    imagen_path = ft.Text(value="", visible=False)
    video_path = ft.Text(value="", visible=False)

    def pick_imagen(e):
        imagen_picker.pick_files(allow_multiple=False, allowed_extensions=["png", "jpg", "jpeg"])

    def pick_video(e):
        video_picker.pick_files(allow_multiple=False, allowed_extensions=["mp4", "mov"])

    def on_imagen_picked(e: ft.FilePickerResultEvent):
        if e.files:
            imagen_path.value = e.files[0].path
            show_snackbar(f"Imagen seleccionada: {imagen_path.value}")

    def on_video_picked(e: ft.FilePickerResultEvent):
        if e.files:
            video_path.value = e.files[0].path
            show_snackbar(f"Video seleccionado: {video_path.value}")

    def show_snackbar(message, color=ft.colors.BLUE):
        page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor=color)
        page.snack_bar.open = True
        page.update()

    imagen_picker.on_result = on_imagen_picked
    video_picker.on_result = on_video_picked

    # Subida al backend
    def upload_file(file_path):
        try:
            with open(file_path, "rb") as f:
                files = {"archivo": (os.path.basename(file_path), f)}
                r = requests.post("http://127.0.0.1:8000/upload/", files=files)
                if r.status_code == 200:
                    return r.json()["archivo_url"]
        except Exception as ex:
            show_snackbar(f"Error subiendo archivo: {ex}", color=ft.colors.RED)
        return None

    def publicar_producto(e):
        nombre = nombre_ctrl.value.strip()
        descripcion = descripcion_ctrl.value.strip()
        precio = precio_ctrl.value.strip()
        categoria = categoria_ctrl.value
        stock = stock_ctrl.value.strip()
        imagen = imagen_path.value
        video = video_path.value or None

        if not all([nombre, descripcion, precio, categoria, stock, imagen]):
            show_snackbar("Faltan campos obligatorios", color=ft.colors.RED)
            return

        # Subir archivos
        imagen_url = upload_file(imagen)
        video_url = upload_file(video) if video else None

        if not imagen_url:
            show_snackbar("No se pudo subir la imagen", color=ft.colors.RED)
            return

        try:
            producto_data = {
                "nombre": nombre,
                "descripcion": descripcion,
                "precio": float(precio),
                "stock": int(stock),
                "categoria": categoria,
                "imagen": imagen_url,
                "video": video_url
            }

            response = requests.post("http://127.0.0.1:8000/productos/", json=producto_data)

            if response.status_code == 200:
                show_snackbar("Producto publicado correctamente", color=ft.colors.GREEN)
            else:
                show_snackbar("Error al publicar producto", color=ft.colors.RED)
                print(response.text)
        except Exception as ex:
            show_snackbar(f"Error de conexión: {ex}", color=ft.colors.RED)

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
                            ft.ElevatedButton("Seleccionar imagen", on_click=pick_imagen, icon=ft.icons.IMAGE),
                            ft.ElevatedButton("Seleccionar video", on_click=pick_video, icon=ft.icons.VIDEO_FILE),
                        ]),
                        ft.ElevatedButton("Publicar producto", on_click=publicar_producto, icon=ft.icons.UPLOAD),
                    ],
                    spacing=15,
                ),
                padding=30,
                alignment=ft.alignment.center,
            )
        ]
    )
