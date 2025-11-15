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


def gestion_inventario (ingredientes,inventario):
    """"
    Modulo 2 del programa
    Recibe: Input para seleccionar opcion del modulo
    Retorna: Output de cada opcion con todas sus funcionalidades 
    """


    print(" 1. Visualizar todo el inventario\n 2. Buscar la existencia de un ingrediente específico\n 3. Listar las existencias de todos los ingredientes de una categoría\n 4. Actualizar la existencia de un producto específico\n 5. Volver al menu principal\n")
    
    opcion_2=input("Ingresa una opción: ")
    while opcion_2 not in ["1", "2","3","4","5"]:
        opcion_2=input("ERROR: Ingresa una opción: ")
    
    if opcion_2=="1" :
        """
        Opcion para visualizar todo el inventario.
        Recibe: Nada
        Retorna: Todos los ingredientes enumerados junto con su cantidad
        """

        print("\nVisualizar todo el inventario\n")

        for key,value in inventario.items():
            print(f"{key}. {value[0].capitalize()}: {value[1]}")

        print("\n")

    elif opcion_2=="2":
        """
        Esta opcion permite seleccionar un ingrediente del menu a partir de 
        su numero y muestra la cantidad del mismo en el inventario
        Recibe: Input de un numero de ingrediente
        Retorna: Cantidad de dicho ingrediente
        """
        print("\nBuscar la existencia de un ingrediente específico\n")
    
        for i, n in enumerate(ingredientes):
            print(f"{i+1}. {n.name.capitalize()}")

        print("\n")

        num = input("Ingrese el numero del ingrediente a verificar el inventario: ")
        while num.isnumeric() == False or int(num) not in range(0, len(ingredientes)+1):
            num=input("ERROR. Ingresa el numero del ingrediente que verificar: ")

        for key,value in inventario.items():
            if key == int(num):
                print(f"\n{value[0].capitalize()}: {value[1]}")
        print("\n")

    elif opcion_2=="3":
        """
        Esta opcion muestra el inventario por categoria
        Recibe: Input sobre categoria deseada
        Retorna: Cantidad de cada elemento perteneciente a la categoria
        """
        ingcat = {}
        print("\nListar las existencias de todos los ingredientes de una categoría\n")

        print(" 1. Pan\n 2. Salchicha\n 3. Acompañante\n 4. Salsa\n 5. Topping\n")
        Listado=input ("Ingresa el listado que quieres ver: ")
        while Listado not in ["1", "2","3","4","5"]:
            Listado=input("ERROR: Ingresa una opción: ")

        Listado = int(Listado)
        target_class = ""
        if Listado == 1:
            target_class = Bread
        elif Listado == 2:
            target_class = Sausage
        elif Listado == 3:
            target_class = Side
        elif Listado == 4:
            target_class = Sauce
        elif Listado == 5:
            target_class = Topping

        if target_class:
            found = False
            for i in ingredientes:
                if isinstance(i, target_class):
                    for key, value in inventario.items():
                        if value[0] == i.name:
                            ingcat[value[0]] = value[1]
                            found = True
                if not found:
                    print("\nNo se encontraron ingredientes en esta categoría.\n")
        print("\n")
        for key,value in ingcat.items():
            print(f"{key.capitalize()}: {value}")
        print("\n")

    elif opcion_2=="4":
        """"
        Esta opcion permite seleccionar un ingrediente a partir de su numero
        y luego modificar su cantidad (adicionar o restar)
        """
        print("\nActualizar la existencia de un producto específico\n")

        for i, n in enumerate(ingredientes):
            print(f"{i+1}. {n.name.capitalize()}")

        print("\n")

        num = input("Ingrese el numero del ingrediente a modificar el inventario: ")
        while num.isnumeric() == False or int(num) not in range(0, len(ingredientes)+1):
            num=input("ERROR. Ingresa el numero del ingrediente que deseas modificar: ")

        print("\nDeseas sumar o restar inventario?\n"
              "1. Sumar\n"
              "2. Restar\n")
        opt = input("Ingresa la opcion deseada: ")

        while opt.isnumeric() == False and opt != ["1","2"]:
            print("ERROR. Intente de nuevo.")
            opt = input("Ingresa la opcion deseada: ")

        print("\nCuantas unidades/porciones deseas?\n")
        unidades = input("Unidades/porciones deseadas: ")

        while unidades.isnumeric() == False or unidades == "0":
            print("ERROR. Intente de nuevo.")
            unidades = input("Unidades/porciones deseadas: ")

        if opt == "1":
            for key,value in inventario.items():
                if key == int(num):
                    value[1] += int(unidades)
            print("\nAdicion exitosa!\n")
        elif opt == "2":
            for key,value in inventario.items():
                if key == int(num):
                    value[1] -= int(unidades)
            print("\nSustraccion exitosa!\n")
            

    elif opcion_2=="5":
        print("\nVolver a menu principal\n")

main()

