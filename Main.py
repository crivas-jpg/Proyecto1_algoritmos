def main():
    
    print("1. Gentión de Ingregientes\n 2. Gentión de Inventario\n 3. Gentión de Menu\n 4. Simular un día de ventas\n 5. Módulo de estadísticas\n 6. Salir")
    opcion=input("Ingresa una opción:")
    while opcion not in ["1", "2","3","4","5","6"]:
        opcion=input("ERROR: Ingresa una opción:")
    
    if opcion=="1" :
        print("Gestion de ingredientes")
    elif opcion=="2":
        print("Gestion de inventario")
    elif opcion=="3":
        print("Gestion de menu")
    elif opcion=="4":
        print("simular dia de ventas")
    elif opcion=="5":
        print("Módulo de estadísticas ")
    elif opcion=="6":
        print("Salir")



main()