# screens/profile.py

import flet as ft
import screens.auth as auth  # para acceder a usuario_actual y reiniciar sesión
from screens.auth import iniciar_sesion


def ProfileView(page: ft.Page):
    """
    Vista de perfil de usuario:
     - Foto de perfil (placeholder)
     - Nombre, ID y correo
     - Accordion para 'Mis productos' y 'Compras'
     - Botones para cerrar sesión y volver
    """
    page.title = "Perfil"

    # Header: Avatar y datos básicos
    avatar = ft.CircleAvatar(
        content=ft.Icons.ACCOUNT_CIRCLE,
        bgcolor=ft.Colors.BLUE_200,
        radius=40
    )
    user_info = ft.Column(
        controls=[
            ft.Text(auth.usuario_actual.get("nombre", ""), size=20, weight=ft.FontWeight.BOLD),
            ft.Text(f"ID: {auth.usuario_actual.get('id', '')}", size=12, color=ft.Colors.WHITE70),
            ft.Text(f"Correo: {auth.usuario_actual.get('email', '')}", size=12, color=ft.Colors.WHITE70),
        ],
        spacing=4
    )
    header = ft.Row(
        controls=[avatar, user_info],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Accordion para secciones
    accordion = ft.Accordion(
        expand=False,
        content=[
            ft.AccordionItem(
                title="Mis productos",
                content=ft.Column([
                    ft.Text("Producto A"),
                    ft.Text("Producto B"),
                    # TODO: reemplazar con datos reales de API (vendedor_id)
                ], spacing=6)
            ),
            ft.AccordionItem(
                title="Compras realizadas",
                content=ft.Column([
                    ft.Text("(Aquí aparecerán tus compras...)"),
                ], spacing=6)
            ),
        ]
    )

    # Botones de acción
    def logout(e):
        iniciar_sesion(None)  # limpiar sesión
        page.go("/login")

    actions = ft.Row(
        controls=[
            ft.ElevatedButton(
                "Cerrar sesión",
                icon=ft.Icons.LOGOUT,
                bgcolor=ft.Colors.RED,
                on_click=logout
            ),
            ft.ElevatedButton(
                "Volver",
                icon=ft.Icons.ARROW_BACK,
                on_click=lambda e: page.go("/home")
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # Construcción de la vista
    return ft.View(
        route="/profile",
        controls=[
            ft.Container(
                expand=True,
                bgcolor=ft.Colors.BLACK,
                padding=20,
                content=ft.Column(
                    controls=[
                        header,
                        ft.Divider(color=ft.Colors.WHITE24),
                        accordion,
                        ft.Divider(color=ft.Colors.WHITE24),
                        actions
                    ],
                    spacing=20,
                    expand=True
                )
            )
        ]
    )
