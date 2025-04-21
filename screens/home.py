import flet as ft

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
        crear_boton("Seguimiento", ft.icons.LOCAL_SHIPPING, "/tracking"),
    ]

    # Usamos Container externo para aplicar el fondo negro
    return ft.View(
        route="/home",
        controls=[
            ft.Container(
                bgcolor=ft.colors.BLACK,
                expand=True,
                content=ft.Column(
                    expand=True,
                    controls=[
                        # Header con logo y búsqueda
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
                        # Barra de navegación
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
                        # Contenido principal
                        ft.Container(
                            content=ft.Text(
                                "¡Bienvenido a SmartStore!",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.WHITE
                            ),
                            padding=20,
                            alignment=ft.alignment.center,
                            expand=True,
                            bgcolor=ft.colors.BLACK
                        ),
                    ]
                )
            )
        ]
    )
