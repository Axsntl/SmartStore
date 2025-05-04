import flet as ft
import requests
import time
import screens.auth as auth  # Importar el módulo auth para acceder dinámicamente a usuario_actual
from screens.ticket_generator import generar_ticket_pdf

# Carrito compartido en memoria
carrito = []

# Gestión del carrito
def agregar_al_carrito(producto):
    global carrito
    for item in carrito:
        if item["id"] == producto["id"]:
            item["cantidad"] += 1
            return
    nuevo = producto.copy()
    nuevo["cantidad"] = 1
    carrito.append(nuevo)


def eliminar_producto(producto_id):
    global carrito
    carrito = [item for item in carrito if item["id"] != producto_id]


def actualizar_stock_backend(producto_id, delta):
    try:
        requests.patch(
            f"http://127.0.0.1:8000/productos/{producto_id}/stock",
            json={"delta": delta}
        )
    except Exception as e:
        print(f"DEBUG: Error al actualizar stock backend: {e}")


def actualizar_cantidad(producto_id, nueva_cantidad):
    global carrito
    for item in carrito:
        if item["id"] == producto_id:
            delta = nueva_cantidad - item["cantidad"]
            item["cantidad"] = nueva_cantidad
            actualizar_stock_backend(producto_id, -delta)
            return


def vaciar_carrito():
    global carrito
    carrito.clear()


def mostrar_snackbar(page, mensaje, color=ft.colors.GREEN):
    page.snack_bar = ft.SnackBar(ft.Text(mensaje), bgcolor=color)
    page.snack_bar.open = True
    page.update()

# Vista del carrito
def CartView(page: ft.Page):
    page.title = "Carrito"

    toggle_ticket = ft.Checkbox(label="Generar Ticket al comprar", value=False)
    contenedor = ft.Column(spacing=15, scroll=ft.ScrollMode.AUTO)

    # Función para reconstruir la UI
    def rebuild():
        contenedor.controls.clear()
        total = 0
        if not carrito:
            contenedor.controls.append(
                ft.Text("Tu carrito está vacío", size=20, color=ft.colors.WHITE70)
            )
            contenedor.controls.append(
                ft.ElevatedButton(
                    "Volver", icon=ft.icons.ARROW_BACK,
                    on_click=lambda e: page.go("/home")
                )
            )
        else:
            for item in carrito:
                subtotal = item["precio"] * item["cantidad"]
                total += subtotal
                input_cantidad = ft.TextField(
                    value=str(item["cantidad"]), width=60,
                    text_align=ft.TextAlign.CENTER,
                    input_filter=ft.InputFilter(allow=True, regex_string=r"\d+"),
                    on_change=lambda e, pid=item["id"]: (
                        actualizar_cantidad(pid, int(e.control.value or 1)), rebuild(), page.update()
                    )
                )
                contenedor.controls.append(
                    ft.Card(
                        content=ft.Container(
                            padding=10,
                            content=ft.Column(
                                spacing=8,
                                controls=[
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text(item["nombre"], size=16, weight=ft.FontWeight.BOLD),
                                            ft.IconButton(
                                                icon=ft.icons.DELETE, tooltip="Eliminar",
                                                on_click=lambda e, pid=item["id"]: (
                                                    eliminar_producto(pid), rebuild(), page.update()
                                                )
                                            )
                                        ]
                                    ),
                                    ft.Row(
                                        spacing=20,
                                        controls=[
                                            ft.Image(src=item["imagen_path"], width=60, height=60),
                                            ft.Column(
                                                spacing=4,
                                                controls=[
                                                    ft.Text(f"Precio: ${item['precio']:.2f}"),
                                                    ft.Row(
                                                        spacing=10,
                                                        controls=[
                                                            ft.Text("Cantidad:"),
                                                            input_cantidad
                                                        ]
                                                    ),
                                                    ft.Text(f"Subtotal: ${subtotal:.2f}", weight=ft.FontWeight.BOLD)
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ),
                        elevation=2,
                        shape=ft.RoundedRectangleBorder(radius=10)
                    )
                )
            # Total y Vaciar
            contenedor.controls.append(
                ft.Container(
                    padding=10,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(f"Total: ${total:.2f}", size=18, weight=ft.FontWeight.BOLD),
                            ft.ElevatedButton("Vaciar carrito", icon=ft.icons.CLEANING_SERVICES,
                                              on_click=lambda e: (vaciar_carrito(), rebuild(), page.update())
                            )
                        ]
                    )
                )
            )
            # Checkbox y Botón Compra
            contenedor.controls.append(
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[toggle_ticket]
                )
            )
            contenedor.controls.append(
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER, spacing=20,
                    controls=[
                        ft.ElevatedButton(
                            "Realizar compra", icon=ft.icons.PAYMENT,
                            on_click=lambda e: handle_buy(e)
                        ),
                        ft.ElevatedButton(
                            "Refrescar", icon=ft.icons.REFRESH,
                            on_click=lambda e: rebuild()
                        ),
                        ft.ElevatedButton(
                            "Volver", icon=ft.icons.ARROW_BACK,
                            on_click=lambda e: page.go("/home")
                        )
                    ]
                )
            )
        page.update()

    # Handler de compra
    def handle_buy(e):
        print("DEBUG: Entró a handle_buy() con toggle_ticket=", toggle_ticket.value)
        if toggle_ticket.value:
            print("DEBUG: ToggleTicket activado")
            if auth.usuario_actual:
                print("DEBUG: Usuario activo:", auth.usuario_actual)
                try:
                    generar_ticket_pdf(auth.usuario_actual, carrito)
                    print("DEBUG: generar_ticket_pdf() finalizó")
                    mostrar_snackbar(page, "Compra realizada y ticket generado")
                except Exception as ex:
                    print("DEBUG: Error en generar_ticket_pdf:", ex)
                    mostrar_snackbar(page, "Error al generar ticket", color=ft.colors.RED)
                    return
            else:
                print("DEBUG: No hay usuario activo")
                mostrar_snackbar(page, "Debes iniciar sesión para generar ticket", color=ft.colors.RED)
                return
        else:
            print("DEBUG: ToggleTicket NO activado")
            mostrar_snackbar(page, "Compra realizada sin ticket")

        vaciar_carrito()
        rebuild()
        page.update()
        time.sleep(2)
        page.go("/home")

    # Inicializar UI
    rebuild()
    return ft.View(
        route="/cart",
        controls=[ft.Container(bgcolor=ft.colors.BLACK, expand=True, padding=20, content=contenedor)]
    )
