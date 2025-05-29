# screens/profile.py

import flet as ft
import screens.auth as auth  # para acceder a usuario_actual y reiniciar sesión
from screens.auth import iniciar_sesion
import requests

#He de escribir que, algunos cambios no se reflejaran por que la pantalla de flet, es estatica, y no se actualiza automaticamente, por lo que se tendra que hacer un rebuild de la pantalla cada vez que se quiera ver algun cambio, en el amplio sentido de la palabra.
# --- Funciones auxiliares ---
# --- Expander personalizado ---
class SimpleExpander:
    def __init__(self, label, content, on_expand=None, on_collapse=None):
        self.expanded = False
        self.label = label
        self.content = content
        self.on_expand = on_expand
        self.on_collapse = on_collapse  # Nuevo: callback opcional al colapsar

    def build(self):
        def toggle(e):
            self.expanded = not self.expanded
            content_container.visible = self.expanded
            e.control.text = ("▼ " if self.expanded else "► ") + self.label
            e.control.update()
            if self.expanded and self.on_expand:
                self.on_expand()
            elif not self.expanded and self.on_collapse:
                self.on_collapse()
        content_container = ft.Container(content=self.content, visible=self.expanded)
        return ft.Column([
            ft.TextButton("► " + self.label, on_click=toggle),
            content_container
        ])


def obtener_mis_productos(usuario_id):
    try:
        response = requests.get(f"http://127.0.0.1:8000/mis_productos/{usuario_id}")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error al obtener productos: {e}")
    return []


def ProfileView(page: ft.Page):
    """
    Vista de perfil de usuario:
     - Foto de perfil (placeholder)
     - Nombre, ID y correo
     - Secciones expandibles para 'Mis productos' y 'Compras'
     - Botones para cerrar sesión y volver
    """
    page.title = "Perfil"

    # Header: Avatar y datos básicos
    avatar = ft.CircleAvatar(
        content=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=40, color=ft.Colors.BLUE_900),
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

    # Contenedor dinámico para productos
    productos_column = ft.Column()

    def rebuild():
        productos_column.controls.clear()
        usuario_id = auth.usuario_actual.get("id")
        productos = obtener_mis_productos(usuario_id)
        if productos:
            for p in productos:
                desc_ctrl = ft.TextField(value=p['descripcion'], width=200)
                stock_ctrl = ft.TextField(value=str(p['stock']), width=60)
                precio_ctrl = ft.TextField(value=str(p['precio']), width=80)
                productos_column.controls.append(
                    ft.Row([
                        ft.Text(p['nombre'], width=120),
                        desc_ctrl,
                        ft.IconButton(
                            ft.Icons.SAVE,
                            tooltip="Guardar descripción",
                            on_click=lambda e, pid=p['id'], ctrl=desc_ctrl: actualizar_descripcion(pid, ctrl.value)
                        ),
                        stock_ctrl,
                        ft.IconButton(
                            ft.Icons.SAVE,
                            tooltip="Guardar stock",
                            on_click=lambda e, pid=p['id'], ctrl=stock_ctrl: actualizar_stock(pid, int(ctrl.value))
                        ),
                        precio_ctrl,
                        ft.IconButton(
                            ft.Icons.SAVE,
                            tooltip="Guardar precio",
                            on_click=lambda e, pid=p['id'], ctrl=precio_ctrl: actualizar_precio(pid, float(ctrl.value))
                        ),
                        ft.IconButton(
                            ft.Icons.DELETE,
                            tooltip="Eliminar producto",
                            on_click=lambda e, pid=p['id']: eliminar_producto(pid)
                        ),
                    ], spacing=8)
                )
        else:
            productos_column.controls.append(ft.Text("No tienes productos publicados."))
        page.update()

    def clear_productos():
        productos_column.controls.clear()
        page.update()

    expander_mis_productos = SimpleExpander(
        "Mis productos",
        productos_column,
        on_expand=rebuild,
        on_collapse=clear_productos
    ).build()

    # Sección compras (puedes hacerla dinámica igual si lo necesitas)
    expander_compras = SimpleExpander(
        "Compras realizadas",
        ft.Column([
            ft.Text("(Aquí aparecerán tus compras...)"),
        ], spacing=6)
    ).build()

    def logout(e):
        iniciar_sesion(None)
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
            ft.ElevatedButton(
                "Refrescar productos",
                icon=ft.Icons.REFRESH,
                on_click=lambda e: rebuild()
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # Construcción de la vista
    view = ft.View(
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
                        expander_mis_productos,
                        expander_compras,
                        ft.Divider(color=ft.Colors.WHITE24),
                        actions
                    ],
                    spacing=20,
                    expand=True
                )
            )
        ]
    )

    def eliminar_producto(producto_id):
        try:
            response = requests.delete(f"http://127.0.0.1:8000/productos/{producto_id}")
            if response.status_code == 200:
                ft.SnackBar(ft.Text("Producto eliminado correctamente"), bgcolor=ft.Colors.GREEN)
                rebuild()
            else:
                ft.SnackBar(ft.Text("Error al eliminar producto"), bgcolor=ft.Colors.RED)
        except Exception as e:
            print(f"Error al eliminar producto: {e}")

    def actualizar_stock(producto_id, nuevo_stock):
        try:
            delta = nuevo_stock  # O calcula la diferencia si lo prefieres
            response = requests.patch(
                f"http://127.0.0.1:8000/productos/{producto_id}/stock",
                json={"delta": delta}
            )
            if response.status_code == 200:
                ft.SnackBar(ft.Text("Stock actualizado"), bgcolor=ft.Colors.GREEN)
                rebuild()
            else:
                ft.SnackBar(ft.Text("Error al actualizar stock"), bgcolor=ft.Colors.RED)
        except Exception as e:
            print(f"Error al actualizar stock: {e}")

    def actualizar_descripcion(producto_id, nueva_desc):
        try:
            response = requests.patch(
                f"http://127.0.0.1:8000/productos/{producto_id}/descripcion",
                json={"descripcion": nueva_desc}
            )
            if response.status_code == 200:
                ft.SnackBar(ft.Text("Descripción actualizada"), bgcolor=ft.Colors.GREEN)
                rebuild()
            else:
                ft.SnackBar(ft.Text("Error al actualizar descripción"), bgcolor=ft.Colors.RED)
        except Exception as e:
            print(f"Error al actualizar descripción: {e}")

    def actualizar_precio(producto_id, nuevo_precio):
        try:
            response = requests.patch(
                f"http://127.0.0.1:8000/productos/{producto_id}/precio",
                json={"precio": nuevo_precio}
            )
            if response.status_code == 200:
                ft.SnackBar(ft.Text("Precio actualizado"), bgcolor=ft.Colors.GREEN)
                rebuild()
            else:
                ft.SnackBar(ft.Text("Error al actualizar precio"), bgcolor=ft.Colors.RED)
        except Exception as e:
            print(f"Error al actualizar precio: {e}")

    # Llama a rebuild al cargar la vista
    rebuild()
    return view
