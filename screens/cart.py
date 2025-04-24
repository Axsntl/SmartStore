# screens/cart.py
carrito = []

def agregar_al_carrito(producto):
    # Verificar si ya está en el carrito
    for item in carrito:
        if item["id"] == producto["id"]:
            item["cantidad"] += 1
            return

    # Si es nuevo producto, lo agregamos con cantidad = 1
    nuevo = producto.copy()
    nuevo["cantidad"] = 1
    carrito.append(nuevo)
