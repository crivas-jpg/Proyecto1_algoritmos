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
            gestion_inventario (ingredientes)
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





main()