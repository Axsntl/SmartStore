import flet as ft
import requests
import time
import screens.auth as auth  # módulo de autenticación
from screens.ticket_generator import generar_ticket_pdf

# Carrito compartido en memoria\ n
carrito = []

# ========= Funciones auxiliares ===========

def agregar_al_carrito(producto):
    """Agrega un producto al carrito o incrementa su cantidad."""
    global carrito
    for item in carrito:
        if item["id"] == producto["id"]:
            item["cantidad"] += 1
            return
    nuevo = producto.copy()
    nuevo["cantidad"] = 1
    carrito.append(nuevo)


def eliminar_producto(producto_id):
    """Elimina un producto del carrito por su ID."""
    global carrito
    carrito = [item for item in carrito if item["id"] != producto_id]


def actualizar_stock_backend(producto_id, delta):
    """Ajusta el stock en el backend tras un cambio de cantidad."""
    try:
        requests.patch(
            f"http://127.0.0.1:8000/productos/{producto_id}/stock",
            json={"delta": delta}
        )
    except Exception as e:
        print(f"DEBUG: Error actualizando stock: {e}")


def actualizar_cantidad(producto_id, nueva_cantidad):
    """Actualiza la cantidad en carrito y sync con backend."""
    global carrito
    for item in carrito:
        if item["id"] == producto_id:
            delta = nueva_cantidad - item["cantidad"]
            item["cantidad"] = nueva_cantidad
            actualizar_stock_backend(producto_id, -delta)
            return


def vaciar_carrito():
    """Vacía todo el carrito."""
    global carrito
    carrito.clear()


def mostrar_snackbar(page, mensaje, color=ft.colors.GREEN):
    """Muestra una notificación al usuario."""
    page.snack_bar = ft.SnackBar(ft.Text(mensaje), bgcolor=color)
    page.snack_bar.open = True
    page.update()

# ========== Vista principal del carrito ===========

def CartView(page: ft.Page):
    page.title = "Carrito de Compras"

    # Checkbox para decidir si generar PDF
    toggle_ticket = ft.Checkbox(label="Generar Ticket al finalizar", value=False)
    
    # Contenedor para items y acciones
    contenedor = ft.Column(spacing=20, scroll=ft.ScrollMode.AUTO)

    # Función para reconstruir la UI cada vez que cambia el carrito
    def rebuild():
        contenedor.controls.clear()
        total = 0

        # Si carrito vacío
        if not carrito:
            contenedor.controls.append(
                ft.Text("Tu carrito está vacío", size=20, color=ft.colors.WHITE70)
            )
            contenedor.controls.append(
                ft.ElevatedButton("Seguir comprando", icon=ft.icons.HOME,
                                  on_click=lambda e: page.go("/home"))
            )
        else:
            # Listado de productos
            for item in carrito:
                subtotal = item["precio"] * item["cantidad"]
                total += subtotal

                # Tarjeta de producto con botones +/-
                contenedor.controls.append(
                    ft.Card(
                        content=ft.Container(
                            padding=12,
                            bgcolor=ft.colors.GREY_900,
                            border_radius=8,
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    # Imagen del producto
                                    ft.Image(src=item["imagen_path"], width=80, height=80),
                                    # Detalles del producto
                                    ft.Column(
                                        spacing=6,
                                        controls=[
                                            ft.Text(item["nombre"], size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                                            ft.Text(f"Precio unitario: ${item['precio']:.2f}", color=ft.colors.CYAN_200),
                                            ft.Text(f"Subtotal: ${subtotal:.2f}", weight=ft.FontWeight.BOLD, color=ft.colors.LIGHT_BLUE_200)
                                        ]
                                    ),
                                    # Controles de cantidad
                                    ft.Row(
                                        spacing=5,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            ft.IconButton(
                                                icon=ft.icons.REMOVE,
                                                tooltip="Disminuir",
                                                on_click=lambda e, pid=item["id"]: (
                                                    actualizar_cantidad(pid, max(item["cantidad"]-1,1)), rebuild(), page.update()
                                                )
                                            ),
                                            ft.Text(str(item["cantidad"]), size=16, color=ft.colors.WHITE),
                                            ft.IconButton(
                                                icon=ft.icons.ADD,
                                                tooltip="Aumentar",
                                                on_click=lambda e, pid=item["id"]: (
                                                    actualizar_cantidad(pid, item["cantidad"]+1), rebuild(), page.update()
                                                )
                                            )
                                        ]
                                    ),
                                    # Botón eliminar
                                    ft.IconButton(
                                        icon=ft.icons.DELETE_FOREVER,
                                        tooltip="Eliminar producto",
                                        on_click=lambda e, pid=item["id"]: (
                                            eliminar_producto(pid), rebuild(), page.update()
                                        )
                                    )
                                ]
                            )
                        ),
                        elevation=4
                    )
                )

            # Sección resumen y acciones finales
            contenedor.controls.append(
                ft.Container(
                    padding=10,
                    bgcolor=ft.colors.GREY_800,
                    border_radius=8,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(f"Total a pagar: ${total:.2f}", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                            ft.ElevatedButton("Vaciar carrito", icon=ft.icons.CLEANING_SERVICES,
                                              on_click=lambda e: (vaciar_carrito(), rebuild(), page.update())
                            )
                        ]
                    )
                )
            )

            # Checkbox y botones de acción
            contenedor.controls.append(
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        toggle_ticket,
                        ft.ElevatedButton(
                            "Realizar compra", icon=ft.icons.PAYMENT,
                            on_click=lambda e: handle_buy(page)
                        ),
                        ft.ElevatedButton(
                            "Refrescar", icon=ft.icons.REFRESH,
                            on_click=lambda e: rebuild()
                        )
                    ]
                )
            )
        page.update()

    # Handler de acción de compra
    def handle_buy(page):
        print("DEBUG: Iniciando compra, generar ticket =", toggle_ticket.value)
        if toggle_ticket.value:
            if auth.usuario_actual:
                generar_ticket_pdf(auth.usuario_actual, carrito)
                mostrar_snackbar(page, "Ticket PDF generado y compra realizada")
            else:
                mostrar_snackbar(page, "Debes iniciar sesión para generar ticket", color=ft.colors.RED)
                return
        else:
            mostrar_snackbar(page, "Compra realizada sin ticket")

        vaciar_carrito()
        rebuild()
        time.sleep(1)
        page.go("/home")

    # Iniciar la vista
    rebuild()
    return ft.View(
        route="/cart",
        controls=[
            ft.Container(
                expand=True,
                bgcolor=ft.colors.BLACK,
                padding=20,
                content=contenedor
            )
        ]
    )
