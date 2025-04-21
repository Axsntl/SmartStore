import flet as ft

def HomeView(page: ft.Page):
    search_bar = ft.TextField(
        hint_text="Buscar en SmartStore",
        expand=True,
        border_radius=10,
        height=40,
        content_padding=10,
    )

    # Cada botón en un contenedor con ancho fijo o adaptable
    botones = [
        ft.Container(
            content=ft.TextButton(
                icon=ft.icons.HOME,
                text="Inicio",
                on_click=lambda _: page.go("/home")
            ),
            width=150,  # ancho razonable para responsividad
            padding=5
        ),
        ft.Container(
            content=ft.TextButton(icon=ft.icons.CATEGORY, text="Categorías"),
            width=150,
            padding=5
        ),
        ft.Container(
            content=ft.TextButton(icon=ft.icons.STORE, text="Tiendas"),
            width=150,
            padding=5
        ),
        ft.Container(
            content=ft.TextButton(icon=ft.icons.ADD_BOX, text="Vender"),
            width=150,
            padding=5
        ),
        ft.Container(
            content=ft.TextButton(icon=ft.icons.ACCOUNT_CIRCLE, text="Perfil"),
            width=150,
            padding=5
        ),
        ft.Container(
            content=ft.TextButton(icon=ft.icons.SHOPPING_BAG, text="Compras"),
            width=150,
            padding=5
        ),
        ft.Container(
            content=ft.TextButton(icon=ft.icons.NOTIFICATIONS, text="Notificaciones"),
            width=150,
            padding=5
        ),
        ft.Container(
            content=ft.TextButton(icon=ft.icons.SHOPPING_CART, text="Carrito"),
            width=150,
            padding=5
        ),
    ]

    return ft.View(
        route="/home",
        controls=[
            ft.Column(
                controls=[
                    # HEADER
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
                        bgcolor=ft.colors.WHITE,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=4,
                            color=ft.colors.BLACK12
                        ),
                    ),
                    # Barra de navegación responsiva
                    ft.Container(
                        content=ft.Row(
                            controls=botones,
                            wrap=True,
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=5,
                            run_spacing=5
                        ),
                        padding=ft.padding.symmetric(vertical=5),
                        bgcolor=ft.colors.BLUE_GREY_100,
                    ),
                    # CONTENIDO PRINCIPAL
                    ft.Container(
                        content=ft.Text(
                            "¡Bienvenido a SmartStore!",
                            size=22,
                            weight=ft.FontWeight.BOLD,
                        ),
                        padding=20,
                        alignment=ft.alignment.center,
                        expand=True,
                    ),
                ],
                expand=True
            )
        ]
    )
