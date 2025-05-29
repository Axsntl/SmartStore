import flet as ft
import requests
from screens.auth import usuario_actual
from screens.cart import agregar_al_carrito

def mostrar_snackbar(page, mensaje):
    page.snack_bar = ft.SnackBar(ft.Text(mensaje), bgcolor=ft.colors.GREEN)
    page.snack_bar.open = True
    page.update()

def HomeView(page: ft.Page):
    
    def crear_boton(texto, icono, ruta=None):
        def on_click(e):
            if ruta:
                page.go(ruta)
            e.control.bgcolor = ft.colors.BLUE_800
            e.control.update()

        def on_hover(e):
            e.control.bgcolor = ft.colors.BLUE_700 if e.data == "true" else ft.colors.BLUE_900
            e.control.update()

        return ft.Container(
            content=ft.TextButton(
                icon=icono,
                text=texto,
                style=ft.ButtonStyle(
                    color=ft.colors.WHITE,
                    overlay_color=ft.colors.BLUE_100,
                ),
                on_click=on_click,
                on_hover=on_hover
            ),
            bgcolor=ft.colors.BLUE_900,
            border_radius=8,
            width=150,
            padding=8
        )

    search_bar = ft.TextField(
        hint_text="Buscar en SmartStore",
        expand=True,
        border_radius=10,
        height=40,
        content_padding=10,
        bgcolor=ft.colors.WHITE,
        text_style=ft.TextStyle(color=ft.colors.BLACK)
    )

    botones = [
        crear_boton("Inicio", ft.icons.HOME, "/home"),
        crear_boton("Categorías", ft.icons.CATEGORY, "/categories"),
        crear_boton("Tiendas", ft.icons.STORE, "/stores"),
        crear_boton("Vender", ft.icons.ADD_BOX, "/sell"),
        crear_boton("Perfil", ft.icons.ACCOUNT_CIRCLE, "/profile"),
        crear_boton("Compras", ft.icons.SHOPPING_BAG, "/purchases"),
        crear_boton("Notificaciones", ft.icons.NOTIFICATIONS, "/notifications"),
        crear_boton("Carrito", ft.icons.SHOPPING_CART, "/cart"),
    ]

    # Contenedor donde se insertarán los productos desde la API
    productos_container = ft.Column(spacing=20, scroll=ft.ScrollMode.AUTO)

    def ver_detalle(e, prod_id):
        page.go(f"/producto/{prod_id}")

        def agregar_al_carrito(e, producto):
            # Aquí podrías guardar el producto en una variable global o base local
            page.snack_bar = ft.SnackBar(ft.Text(f"{producto['nombre']} agregado al carrito."), bgcolor=ft.colors.GREEN)
            page.snack_bar.open = True
            page.update()
    
    def cargar_productos():
        try:
            response = requests.get("http://127.0.0.1:8000/productos/")
            if response.status_code == 200:
                data = response.json()
                print(data)  # Depuración: Verifica los datos recibidos
                for producto in data:
                    tarjeta = ft.Container(
                        bgcolor=ft.colors.BLUE_900,
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
                                                ft.Text(f"Precio: ${producto.get('precio', 0):.2f}", color=ft.colors.CYAN_200),
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
                                            "Ver más",
                                            icon=ft.icons.PREVIEW,
                                            on_click=lambda e, id=producto["id"]: ver_detalle(e, id),
                                            style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_600)
                                        ),
                                        ft.ElevatedButton(
                                            "Agregar al carrito",
                                            icon=ft.icons.ADD_SHOPPING_CART,
                                            on_click=lambda e, p=producto: (
                                                agregar_al_carrito(p),
                                                mostrar_snackbar(page, f"{p['nombre']} agregado al carrito.")
                                            ),
                                            style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_GREY_600)
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                    productos_container.controls.append(tarjeta)
            else:
                productos_container.controls.append(ft.Text(f"No se pudieron cargar los productos. Código de estado: {response.status_code}", color=ft.colors.RED))
        except Exception as e:
            productos_container.controls.append(ft.Text(f"Error al conectar con el servidor: {e}", color=ft.colors.RED))

    page.update()

    # Cargar productos al abrir la vista
    page.on_view_pop = lambda _: None  # prevenir errores al volver
    cargar_productos()

    return ft.View(
        route="/home",
        controls=[
            ft.Container(
                bgcolor=ft.colors.BLACK,
                expand=True,
                content=ft.Column(
                    expand=True,
                    controls=[
                        # Header
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Image(src="assets/logo.png", width=100),
                                    search_bar,
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            padding=ft.padding.symmetric(horizontal=12, vertical=10),
                            bgcolor=ft.colors.BLACK,
                        ),
                        # Botones navegación
                        ft.Container(
                            content=ft.Row(
                                controls=botones,
                                wrap=True,
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=10,
                                run_spacing=10
                            ),
                            padding=ft.padding.symmetric(vertical=10),
                            bgcolor=ft.colors.BLACK,
                        ),
                        # Contenedor de productos (ya lleno desde cargar_productos)
                        ft.Container(
                            content=productos_container,
                            padding=20,
                            expand=True,
                            bgcolor=ft.colors.BLACK
                        )
                    ]
                )
            )
        ]
    )
