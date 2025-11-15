from funciones import*
from Ingredientes import *
from Menu import *


def main():
    menu = construir_menu()
    ingredientes=construir_ingredientes()
    
    while True: 
        print(" 1. Gestión de Ingregientes\n 2. Gestión de Inventario\n 3. Gestión de Menu\n 4. Simular un día de ventas\n 5. Módulo de estadísticas\n 6. Salir\n")
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

def gestion_ingredientes (ingredientes):
    print(" 1. Listar todos los productos de una categoría\n 2. Listar todos los productos en esa categoría de un tipo\n 3. Agregar un ingrediente\n 4. Eliminar un ingrediente\n 5. Volver al menu principal\n")
    opcion_1=input("Ingresa una opción: ")
    while opcion_1 not in ["1", "2","3","4","5"]:
        opcion_1=input("ERROR: Ingresa una opción: ")
    
    if opcion_1=="1" :
        print("\nListar todos los productos de una categoría\n")
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
                    i.mostrar()
                    found = True
            if not found:
                print("\nNo se encontraron ingredientes en esta categoría.\n")
        
        print()
        print()

#no se sabe que hacer acá
    elif opcion_1=="2":
        print("\nListar todos los productos en esa categoría de un tipo\n")
        # por ejemplo si es salchichas, listas todas las salchicas de cerdo, res y pollo

    elif opcion_1=="3":
        print("Agregar un ingrediente")
        print(" 1. Pan\n 2. Salchicha\n 3. Acompañante\n 4. Salsa\n 5. Topping\n")
        Listado=input ("Ingresa el listado que quieres ver: ")
        while Listado not in ["1", "2","3","4","5"]:
            Listado=input("ERROR: Ingresa una opción: ")

        if Listado in["1","2","3"]:
            name=input('Ingresa el nombre del ingrediente: ' )
            type=input("Ingresa el tipo del ingrediente: ")
            size=input("Ingresa el tamaño del ingrediente: ")
            unit=input("Ingresa la unidad del ingrediente: ")
            if Listado == "1":
                pan = Bread(name,type,size,unit)
                ingredientes.append(pan)
            elif Listado == "2":
                salchicha=Sausage(name,type,size,unit)
                ingredientes.append(salchicha)
            elif Listado == "3":
                acompañante=Side(name,type,size,unit)
                ingredientes.append(acompañante)

        elif Listado =="4":
            name=input('Ingresa el nombre del ingrediente: ' )
            base=input('Ingresa la base del ingrediente: ' )
            color=input('Ingresa el color del ingrediente: ' )
            salsa=Sauce(name,"","","",base,color)
            ingredientes.append(salsa)

        elif Listado == "5":
            name=input('Ingresa el nombre del ingrediente: ' )
            type=input('Ingresa el tipo del ingrediente: ' )
            presentation=input('Ingresa la presentación del ingrediente: ' )
            topping=Topping(name,type,presentation)
            ingredientes.append(topping)

        print ('\nIngrediente agregado con exito!\n')
        
    elif opcion_1=="4":
        print("\nEliminar un ingrediente\n")
        for i, n in enumerate(ingredientes):
            print(i, n.name)

        borrar=input("Ingresa el numero del ingrediente que deseas eliminar: ")
        while borrar.isnumeric() == False or int(borrar) not in range(0, len(ingredientes)):
            borrar=input("ERROR. Ingresa el numero del ingrediente que deseas eliminar: ")

        ingredientes.pop(int(borrar))
        print("\nEliminado correctamente!\n")

    elif opcion_1=="5":
        pass

def gestion_inventario (ingredientes):
    print(" 1. Visualizar todo el inventario\n 2. Buscar la existencia de un ingrediente específico\n 3. Listar las existencias de todos los ingredientes de una categoría\n 4. Actualizar la existencia de un producto específico\n 5. Volver al menu principal\n")
    opcion_2=input("Ingresa una opción: ")
    while opcion_2 not in ["1", "2","3","4","5"]:
        opcion_2=input("ERROR: Ingresa una opción: ")
    
    if opcion_2=="1" :
        print("Visualizar todo el inventario")
    elif opcion_2=="2":
        print("Buscar la existencia de un ingrediente específico")
    elif opcion_2=="3":
        print("Listar las existencias de todos los ingredientes de una categoría")
    elif opcion_2=="4":
        print("Actualizar la existencia de un producto específico")
    elif opcion_2=="5":
        print("Volver a menu principal")

def gestion_menu (menu):
    print(" 1. Ver la lista de hot dogs\n 2. Ver, para un hot dog específico, si hay suficiente inventario para venderlo\n 3. Agregar un nuevo hot dog\n 4. Eliminar un hot dog\n 5. VOlver al menu principal")
    opcion_3=input("Ingresa una opción: ")
    while opcion_3 not in ["1", "2","3","4","5"]:
        opcion_3=input("ERROR: Ingresa una opción: ")

    if opcion_3=="1" :
        print("Ver la lista de hot dogs")
    elif opcion_3=="2":
        print("Ver, para un hot dog específico, si hay suficiente inventario para venderlo")
    elif opcion_3=="3":
        print("Agregar un nuevo hot dog")
    elif opcion_3=="4":
        print("Eliminar un hot dog")
    elif opcion_3=="5":
        print("Volver a menu principal")

main()