from funciones import*
from Ingredientes import *
from Menu import *


def main():
    """
    Menu principal
    Presenta todos los modulos exigidos en la rubrica como opciones a seleccionar
    Recibe: Input para seleccionar modulo deseado
    Retorna: Opciones correspondientes a dicho modulo
    """
    menu = construir_menu()
    ingredientes=construir_ingredientes()

    """"
    Se crea el inventario.
    NOTA: la API no da informacion sobre la cantidad de ningun ingrediente
        El equipo decidio establecer que todos empiezan en 100 unidades
        Cabe destacar que el 100 es flexible para unidades (de salchichas, panes y acompañantes)
        y 100 porciones de salsas o toppings
    """
    inventario = {}
    for i, n in enumerate(ingredientes):
            inventario[i+1] = [n.name,100]
    
    while True: 
        print(" 1. Gestión de Ingredientes\n 2. Gestión de Inventario\n 3. Gestión de Menu\n 4. Simular un día de ventas\n 5. Módulo de estadísticas\n 6. Salir\n")
        opcion=input("Ingresa una opción: ")
        while opcion not in ["1", "2","3","4","5","6"]:
            opcion=input("ERROR: Ingresa una opción: ")
        
        if opcion=="1" :
            print("\n---Gestion de ingredientes---\n")
            gestion_ingredientes(ingredientes)
        elif opcion=="2":
            print("\n---Gestion de inventario---\n")
            gestion_inventario (ingredientes,inventario)
        elif opcion=="3":
            print("\n---Gestion de menu---\n")
            gestion_menu (menu)
        elif opcion=="4":
            print("\n---Simular dia de ventas---\n")
        elif opcion=="5":
            print("\n---Módulo de estadísticas---\n ")

        elif opcion=="6":
            print("\nGracias por visitar Hot Dog CCS!\n")
            break


def gestion_menu (menu):
    """
    Modulo 3 del programa
    Recibe: Input de opciones del modulo
    Retorna: Output de cada opcion del modulo
    """
    print(" 1. Ver la lista de hot dogs\n 2. Ver, para un hot dog específico, si hay suficiente inventario para venderlo\n 3. Agregar un nuevo hot dog\n 4. Eliminar un hot dog\n 5. Volver al menu principal\n")
    opcion_3=input("Ingresa una opción: ")
    while opcion_3 not in ["1", "2","3","4","5"]:
        opcion_3=input("ERROR: Ingresa una opción: ")

    if opcion_3=="1" :
        """
        Se llama al metodo mostrar de la clase Hotdog
        Recibe: Nada
        Retorna: Lista de hotdogs
        """
        print("\nVer la lista de hot dogs\n")

        for h in menu:
            h.mostrar()

    elif opcion_3=="2":
        print("\nVer, para un hot dog específico, si hay suficiente inventario para venderlo\n")


    elif opcion_3=="3":
        print("\nAgregar un nuevo hot dog\n")
    elif opcion_3=="4":
        print("\nEliminar un hot dog\n")

        print("\nEliminar un ingrediente\n")
        for i, n in enumerate(menu):
            print(f"{i+1}. {n.name.capitalize()}")

        print("\n")
        borrar=input("Ingresa el numero del hotdog que deseas eliminar: ")
        while borrar.isnumeric() == False or int(borrar) not in range(0, len(menu)+1):
            borrar=input("ERROR. Ingresa el numero del hotdog que deseas eliminar: ")

        menu.pop(int(borrar)-1)
        print("\nEliminado correctamente!\n")

    elif opcion_3=="5":
        print("\nVolver a menu principal\n")

main()

