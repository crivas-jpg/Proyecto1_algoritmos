def main():
    
    print("1. Gentión de Ingregientes\n 2. Gentión de Inventario\n 3. Gentión de Menu\n 4. Simular un día de ventas\n 5. Módulo de estadísticas\n 6. Salir")
    opcion=input("Ingresa una opción:")
    while opcion not in ["1", "2","3","4","5","6"]:
        opcion=input("ERROR: Ingresa una opción:")
    
    if opcion=="1" :
        print("Gestion de ingredientes")
        gestion_ingredientes()
    elif opcion=="2":
        print("Gestion de inventario")
        gestion_inventario ()
    elif opcion=="3":
        print("Gestion de menu")
        gestion_menu ()
    elif opcion=="4":
        print("simular dia de ventas")
    elif opcion=="5":
        print("Módulo de estadísticas ")

    elif opcion=="6":
        print("Salir")

def gestion_ingredientes ():
    print("1. Listar todos los productos de una categoría\n 2. Listar todos los productos en esa categoría de un tipo\n 3. Agregar un ingrediente\n 4. Eliminar un ingrediente\n 5. Volver al menu principal")
    opcion_1=input("Ingresa una opción:")
    while opcion_1 not in ["1", "2","3","4","5"]:
        opcion_1=input("ERROR: Ingresa una opción:")
    
    if opcion_1=="1" :
        print("Listar todos los productos de una categoría")
    elif opcion_1=="2":
        print("Listar todos los productos en esa categoría de un tipo")
    elif opcion_1=="3":
        print("Agregar un ingrediente")
    elif opcion_1=="4":
        print("Eliminar un ingrediente")
    elif opcion_1=="5":
        print("Volver a menu principal")

def gestion_inventario ():
    print("1. Visualizar todo el inventario\n 2. Buscar la existencia de un ingrediente específico\n 3. Listar las existencias de todos los ingredientes de una categoría\n 4. Actualizar la existencia de un producto específico\n 5. Volver al menu principal")
    opcion_2=input("Ingresa una opción:")
    while opcion_2 not in ["1", "2","3","4","5"]:
        opcion_2=input("ERROR: Ingresa una opción:")
    
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

def gestion_menu ():
    print("1. Ver la lista de hot dogs\n 2. Ver, para un hot dog específico, si hay suficiente inventario para venderlo\n 3. Agregar un nuevo hot dog\n 4. Eliminar un hot dog\n 5. VOlver al menu principal")
    opcion_3=input("Ingresa una opción:")
    while opcion_3 not in ["1", "2","3","4","5"]:
        opcion_3=input("ERROR: Ingresa una opción:")

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