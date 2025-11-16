import requests
from Hotdog import *
from Ingredientes import *

# urls de los ingredientes y el menu
url_ingredientes = "http://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-1/refs/heads/main/ingredientes.json"
url_menu = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-1/refs/heads/main/menu.json"

def llamada_api(url):
    """
    Funcion para extraer los datos de la API:
    Recibe: url de la API a tomar los datos
    Retorna: Datos de la API
    """
    r = requests.get(url)

    print(f"Status Code: {r.status_code}\n ")
    print(f"Content Type: {r.headers['content-type']}")

    if r.status_code == 200:
        print("\nDatos cargados con éxito.\n")
        return r.json()
    else:
        print("Error con la carga de datos, intente de nuevo. \n")




def construir_menu():
    """
    Genera el menu en una estructura de datos local (lista de objetos) a partir de la informacion extraida 
    de la API
    Recibe: __. Parte de la llamada a la funcion llamada_api con el url del menu
    Retorna: menu en formato de lista de objetos como estructura de datos local
    """
    menu = llamada_api(url_menu)
    nuevo_menu=[]
    for i in menu:
        i = list(i.values())
        name = i[0]
        bread = i[1]
        sausage = i[2]
        toppings = i[3]
        sauces = i[4]
        side = i[5]
        hotdog = Hotdog(name,bread,sausage,toppings,sauces,side)
        nuevo_menu.append(hotdog)
    #forzar tolerante a la salsa
    #print(nuevo_menu)
    return nuevo_menu

def construir_ingredientes():
    """
    Genera los ingredientes en una estructura de datos local (lista de objetos) a partir de la informacion extraida 
    de la API
    Recibe: __. Parte de la llamada a la funcion llamada_api con el url de los ingredientes
    Retorna: ingredientes en formato de lista de objetos como estructura de datos local
    """
    ingredientes = llamada_api(url_ingredientes)
    nuevos_ingredientes=[]
    for i in ingredientes:
        category=i["Categoria"]
        opcion=i["Opciones"]
        if category=="Pan":
            for j in opcion:
                name=j["nombre"]
                type=j["tipo"]
                size=j["tamaño"]
                unit=j["unidad"]
                pan = Bread (name,type,size,unit)
                nuevos_ingredientes.append (pan )
        elif category=="Salchicha":
            for j in opcion:
                name=j["nombre"]
                type=j["tipo"]
                size=j["tamaño"]
                unit=j["unidad"]
                salchicha=Sausage (name,type,size,unit)
                nuevos_ingredientes.append (salchicha)
        elif category=="Acompañante":
            for j in opcion:
                name=j["nombre"]
                type=j["tipo"]
                size=j["tamaño"]
                unit=j["unidad"]
                acompañante=Side(name,type,size,unit)
                nuevos_ingredientes.append (acompañante)
        elif category=="Salsa":
            for j in opcion:
                name=j["nombre"]
                base=j["base"]
                color=j["color"]
                salsa=Sauce(name,base,color)
                nuevos_ingredientes.append (salsa)
        elif category=="toppings":
           for j in opcion:
                name=j["nombre"]
                type=j["tipo"]
                presentation=j["presentación"]
                toppings=Topping(name,type,presentation)
                nuevos_ingredientes.append (toppings) 

    return nuevos_ingredientes
    #print(nuevos_ingredientes)


def crear_hotdog(menu, ingredientes, inventario):
    """
    Interfaz para crear un nuevo Hotdog seleccionando ingredientes existentes.
    - Pide nombre del hotdog
    - Muestra cada categoría (Pan, Salchicha, Acompañante, Salsa, Topping)
    - El usuario selecciona el número correspondiente del listado filtrado
    - Crea y agrega el hotdog al `menu`
    """
    from Hotdog import Hotdog
    print("\nCrear un nuevo hot dog\n")
    name = input("Nombre del nuevo hotdog: ").strip()
    while not name:
        name = input("Nombre no puede estar vacío. Ingresa nombre: ").strip()

    def elegir_por_clase(cls, prompt, allow_skip=False):
        opciones = [i for i in ingredientes if isinstance(i, cls)]
        if not opciones:
            print(f"No hay opciones disponibles para {prompt}.")
            return None
        print(f"\nSelecciona {prompt}:")
        for idx, obj in enumerate(opciones, start=1):
            print(f"{idx}. {obj.name.capitalize()}")
        if allow_skip:
            print("0. Omitir")

        num = input(f"Ingresa el número de {prompt}: ")
        valid_range = list(map(str, range(1, len(opciones)+1)))
        if allow_skip:
            valid_range.append("0")
        while num not in valid_range:
            num = input("Entrada inválida. Intenta de nuevo: ")
        if allow_skip and num == "0":
            return None
        return opciones[int(num)-1]

    def buscar_en_inventario_por_nombre(nombre, inventario):
        for k, v in inventario.items():
            if v[0].lower() == nombre.lower():
                return k, v[1]
        return None, None

    def validar_seleccion_e_inventario(obj, cls_name):
        """Valida que el objeto exista en el inventario y tenga al menos 1 unidad.
        Si no existe, da opción de seleccionar otro o cancelar. Si existe pero qty<1, muestra advertencia y pide confirmación."""
        if obj is None:
            return None  # caller will decide
        nombre = getattr(obj, 'name', str(obj))
        key, qty = buscar_en_inventario_por_nombre(nombre, inventario)
        if key is None:
            print(f"No se encontró '{nombre}' en el inventario.")
            opt = input("Deseas seleccionar otro ingrediente (s) o cancelar el registro (c)? (s/c): ")
            while opt.lower() not in ('s', 'c', 'si', 'n') and opt.lower() not in ('s','c'):
                opt = input("Entrada inválida. Escribe 's' para seleccionar otro o 'c' para cancelar: ")
            if opt.lower().startswith('s'):
                return 'REPLACE'
            else:
                return 'CANCEL'
        if qty < 1:
            print(f"Advertencia: No hay inventario suficiente de '{nombre}' (cantidad = {qty}).")
            opt = input("Deseas continuar con esta selección a pesar de todo? (s/n): ")
            while opt.lower() not in ('s', 'n', 'si', 'no'):
                opt = input("Entrada inválida. (s/n): ")
            if opt.lower().startswith('s'):
                return 'OK'
            else:
                return 'REPLACE'
        return 'OK'

    # Selección iterativa con validaciones
    # Pan (obligatorio)
    while True:
        bread = elegir_por_clase(Bread, "Pan")
        if bread is None:
            print("No se pueden crear hotdogs sin pan. Cancelando creación.")
            return None
        r = validar_seleccion_e_inventario(bread, 'Pan')
        if r == 'OK':
            break
        elif r == 'CANCEL':
            print("Creación cancelada por el usuario.")
            return None
        # REPLACE -> repetir selección

    # Salchicha (obligatorio)
    while True:
        sausage = elegir_por_clase(Sausage, "Salchicha")
        if sausage is None:
            print("No se pueden crear hotdogs sin salchicha. Cancelando creación.")
            return None
        r = validar_seleccion_e_inventario(sausage, 'Salchicha')
        if r == 'OK':
            break
        elif r == 'CANCEL':
            print("Creación cancelada por el usuario.")
            return None

    # Opcionales: acompañante, salsa, topping
    while True:
        side = elegir_por_clase(Side, "Acompañante", allow_skip=True)
        if side is None:
            break
        r = validar_seleccion_e_inventario(side, 'Acompañante')
        if r == 'OK':
            break
        elif r == 'CANCEL':
            print("Creación cancelada por el usuario.")
            return None
        # else REPLACE -> repetir

    while True:
        sauce = elegir_por_clase(Sauce, "Salsa", allow_skip=True)
        if sauce is None:
            break
        r = validar_seleccion_e_inventario(sauce, 'Salsa')
        if r == 'OK':
            break
        elif r == 'CANCEL':
            print("Creación cancelada por el usuario.")
            return None

    while True:
        topping = elegir_por_clase(Topping, "Topping", allow_skip=True)
        if topping is None:
            break
        r = validar_seleccion_e_inventario(topping, 'Topping')
        if r == 'OK':
            break
        elif r == 'CANCEL':
            print("Creación cancelada por el usuario.")
            return None

    nuevo = Hotdog(name, bread, sausage, topping, sauce, side)

    # Validar longitudes mediante método de la clase Hotdog (pide confirmación si no coinciden)
    try:
        ok_long = nuevo.validadr_longitud()
    except Exception:
        ok_long = nuevo.verificar_longitud()

    if not ok_long:
        print("No se confirmó la longitud del hotdog. Registro cancelado.")
        return None

    # Verificar inventario final para todos los ingredientes seleccionados (si alguno queda sin stock, avisar)
    faltantes = []
    sin_stock = []
    seleccionados = [nuevo.bread, nuevo.sausage]
    for optional in (nuevo.sides, nuevo.sauces, nuevo.toppings):
        if optional is None:
            continue
        seleccionados.append(optional)

    for item in seleccionados:
        if item is None:
            continue
        # if list, iterate
        if isinstance(item, list):
            items_iter = item
        else:
            items_iter = [item]
        for it in items_iter:
            nombre = getattr(it, 'name', str(it))
            key, qty = buscar_en_inventario_por_nombre(nombre, inventario)
            if key is None:
                faltantes.append(nombre)
            elif qty < 1:
                sin_stock.append((nombre, qty))

    if faltantes:
        print("\nAdvertencia: los siguientes ingredientes no se encontraron en inventario:")
        for f in faltantes:
            print(f" - {f}")
        print("Se cancelará el registro para que el usuario seleccione ingredientes existentes.")
        return None

    if sin_stock:
        print("\nAdvertencia: los siguientes ingredientes no tienen stock suficiente:")
        for s in sin_stock:
            print(f" - {s[0]} (cantidad = {s[1]})")
        opt = input("Deseas continuar y agregar el hotdog al menú igual? (s/n): ")
        while opt.lower() not in ('s','n','si','no'):
            opt = input("Entrada inválida. (s/n): ")
        if not opt.lower().startswith('s'):
            print("Creación cancelada por el usuario.")
            return None

    menu.append(nuevo)
    print(f"\nHotdog '{name}' creado y agregado al menú satisfactoriamente.\n")
    return nuevo


def verificar_inventario_hotdog(hotdog, ingredientes, inventario):
    """
    Verifica si hay suficiente inventario para preparar un `hotdog`.
    - Comprueba que cada ingrediente del hotdog exista en `inventario` y tenga al menos 1 unidad.
    - Valida longitudes entre pan y salchicha y pide confirmación si difieren.
    Retorna True si todo está bien, False en caso contrario.
    """
    def buscar_en_inventario_por_nombre(nombre):
        for k, v in inventario.items():
            if v[0].lower() == nombre.lower():
                return k, v[1]
        return None, None

    seleccionados = []
    for attr in ('bread', 'sausage', 'sides', 'sauces', 'toppings'):
        val = getattr(hotdog, attr)
        if val is None:
            continue
        if isinstance(val, list):
            seleccionados.extend(val)
        else:
            seleccionados.append(val)

    faltantes = []
    sin_stock = []

    for it in seleccionados:
        nombre = getattr(it, 'name', str(it))
        key, qty = buscar_en_inventario_por_nombre(nombre)
        if key is None:
            faltantes.append(nombre)
        elif qty < 1:
            sin_stock.append((nombre, qty))

    # Validar longitudes (pedir confirmación si no coinciden)
    try:
        if not hotdog.verificar_longitud():
            print("\nAdvertencia: la longitud o unidad del pan y la salchicha no coinciden.")
            resp = input("¿Deseas continuar con esta venta igualmente? (s/n): ").strip().lower()
            while resp not in ('s', 'n', 'si', 'no'):
                resp = input("Entrada inválida. (s/n): ").strip().lower()
            if not resp.startswith('s'):
                return False
    except Exception:
        pass

    if faltantes:
        print("\nNo se encontraron los siguientes ingredientes en inventario:")
        for f in faltantes:
            print(f" - {f}")
        return False

    if sin_stock:
        print("\nLos siguientes ingredientes no tienen stock suficiente:")
        for s in sin_stock:
            print(f" - {s[0]} (cantidad = {s[1]})")
        return False

    print("\nHay suficiente inventario para vender este hotdog.")
    return True



def gestion_ingredientes (ingredientes):
    """
    Modulo 1 del programa.
    Recibe: Input para seleccionar opciones del modulo
    Retorna: Returns de cada opcion
    """
    print(" 1. Listar todos los productos de una categoría\n 2. Listar todos los productos en esa categoría de un tipo\n 3. Agregar un ingrediente\n 4. Eliminar un ingrediente\n 5. Volver al menu principal\n")
    opcion_1=input("Ingresa una opción: ")
    while opcion_1 not in ["1", "2","3","4","5"]:
        opcion_1=input("ERROR: Ingresa una opción: ")
    
    if opcion_1=="1" :
        """
        Opcion para listar todos los productos de una categoria.
        Recibe: Input para seleccionar categoria
        Retorna: Todos los elementos de esa categoria con todos sus atributos
        """
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
                    """
                    Se usa el metodo mostrar de la clase Ingrediente que tiene herencia y 
                    polimorfismo para imprimir todos los atributos de una categoria
                    """
                    i.mostrar()
                    found = True
            if not found:
                print("\nNo se encontraron ingredientes en esta categoría.\n")
        
        print()
        print()


    elif opcion_1=="2":
        """
        Esta seccion sirve para mostrar los tipos de una categoria.
        Recibe: Categoria (ej. pan)
        Retorna: Tipos de pan (por ejemplo) que existen en la lista de ingredientes junto con
        los nombres de dicho tipo
        NOTA: no se muestran los demas atributos para no se redundantes
        La opcion 1 del modulo 1 muestra TODOS los atributos de los ingredientes de acuerdo a su categoria
        """

        """
        Se crea un diccionario vacio para almacenar los tipos como keys, se escoge el diccionario
        para eliminar los duplicados, solo se guarda una instancia del tipo
        """

        tipo = {}
        print("\nListar todos los productos en esa categoría de un tipo\n")
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
                    """
                    Bloque try-except porque las salsas no estan clasificadas por tipo
                    se escogio clasificarlas por base.
                    Se inicializan los values como listas vacias
                    """
                    try:
                        tipo[i.type] = []
                        found = True
                    except:
                        tipo[i.base] = []
                        found = True
            if not found:
                print("\nNo se encontraron ingredientes en esta categoría.\n")

            for i in ingredientes:
                if isinstance(i, target_class):
                    """
                    Se guardan los nombres de los productos que corresponden a dicho producto 
                    de dicha categoria
                    """
                    for key,value in tipo.items():
                        try:
                            if key == i.type:
                                tipo[key].append(i.name)
                        except:
                            if key == i.base:
                                tipo[key].append(i.name)

        for key,value in tipo.items():
            print(f"\n--{key}--")
            for v in value:
                print(f"{v}")
        
        print()
        print()
        

    elif opcion_1=="3":
        """
        Opcion para agregar un ingrediente
        Recibe: Input de categoria de ingrediente a agregar
        Retorna: Mensaje de exito
        NOTA: para ver el ingrediente agregado en su respectiva categoria se recomienda usar la 
        opcion 1 (o la 2)
        """
        print("\nAgregar un ingrediente\n")
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
            salsa=Sauce(name,base,color)
            ingredientes.append(salsa)

        elif Listado == "5":
            name=input('Ingresa el nombre del ingrediente: ' )
            type=input('Ingresa el tipo del ingrediente: ' )
            presentation=input('Ingresa la presentación del ingrediente: ' )
            topping=Topping(name,type,presentation)
            ingredientes.append(topping)

        print ('\nIngrediente agregado con exito!\n')
        
    elif opcion_1=="4":
        """
        Opcion para eliminar un ingrediente
        Recibe: Input del numero del ingrediente a eliminar
        Retorna: Mensaje de confirmacion
        NOTA: se puede confirmar esto desplegando todos los ingredientes de una categoria con la opcion 1
        """
        print("\nEliminar un ingrediente\n")
        for i, n in enumerate(ingredientes):
            print(f"{i+1}. {n.name.capitalize()}")

        print("\n")
        borrar=input("Ingresa el numero del ingrediente que deseas eliminar: ")
        while borrar.isnumeric() == False or int(borrar) not in range(0, len(ingredientes)+1):
            borrar=input("ERROR. Ingresa el numero del ingrediente que deseas eliminar: ")

        ingredientes.pop(int(borrar)-1)
        print("\nEliminado correctamente!\n")

    elif opcion_1=="5":
        """
        Para retornar al menu principal
        """
        pass

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

def gestion_menu (menu,ingredientes,inventario):
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

        # Listar hotdogs y permitir seleccionar uno para verificar inventario
        for i, h in enumerate(menu):
            print(f"{i+1}. {h.name.capitalize()}")

        print("\n")
        num = input("Ingrese el número del hotdog a verificar: ")
        while num.isnumeric() == False or int(num) not in range(1, len(menu)+1):
            num = input("ERROR. Ingresa el numero del hotdog que verificar: ")

        hot = menu[int(num)-1]
        # Usar la función de funciones.py para verificar inventario
        verificar_inventario_hotdog(hot, ingredientes, inventario)
        

    elif opcion_3=="3":
        print("\nAgregar un nuevo hot dog\n")
        # Llamar a la función que crea un hotdog interactivo
        try:
            crear_hotdog(menu, ingredientes, inventario)
        except Exception as e:
            print(f"Ocurrió un error al crear el hotdog: {e}")



    elif opcion_3=="4":
        """
        Esta opcion enumera todos los hotdogs del menu y le permite
        seleccionar al usuario cual eliminar
        Recibe: Input de numero de hotdog deseado
        Retorna: Mensaje de confirmacion
        """
        print("\nEliminar un hot dog\n")
        for i, n in enumerate(menu):
            print(f"{i+1}. {n.name.capitalize()}")

        print("\n")
        borrar=input("Ingresa el numero del hotdog que deseas eliminar: ")
        while borrar.isnumeric() == False or int(borrar) not in range(1, len(menu)+1):
            borrar=input("ERROR. Ingresa el numero del hotdog que deseas eliminar: ")

        idx = int(borrar)-1
        hot = menu[idx]
        # verificar si hay suficiente inventario para seguir vendiendo este hotdog
        puede_vender = verificar_inventario_hotdog(hot, ingredientes, inventario)
        if puede_vender:
            # si hay inventario, pedir confirmación antes de eliminar
            resp = input("Advertencia: aún hay inventario suficiente para vender este hotdog.\n¿Deseas eliminarlo de todas formas? (s/n): ").strip().lower()
            while resp not in ('s','n','si','no'):
                resp = input("Entrada inválida. Responde 's' para sí o 'n' para no: ").strip().lower()
            if not resp.startswith('s'):
                print("\nEliminación cancelada.\n")
            else:
                menu.pop(idx)
                print("\nEliminado correctamente!\n")
        else:
            # no hay inventario suficiente -> eliminar sin preguntar
            menu.pop(idx)
            print("\nEliminado correctamente!\n")

    elif opcion_3=="5":
        print("\nVolver a menu principal\n")


