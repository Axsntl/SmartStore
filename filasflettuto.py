import flet as ft

#Iniciamos la creacion de la pagina de flet
def main(page: ft.Page):
    page.title = "Flettuto - Filas"
    #Asi se agregan las filas
    texto1= ft.Text(value="Texto 1", size=30, color="blue")
    texto2= ft.Text(value="Texto 2", size=30, color="red")
    
    #Se crea la fila
    fila_textos= ft.Row(
        controls=[texto1, texto2],
        #Con controls se agregan los elementos a la fila
        alignment=ft.MainAxisAlignment.CENTER   
        #Se alinea la fila al centro    
    )   
ft.app(target=main)
