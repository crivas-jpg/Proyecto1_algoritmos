import requests
import json
from Hotdog import *
from Ingredientes import *
import json

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
    Esta funcion permite crear un nuevo hotdog a partir de los ingredintes existentes
    Recibe: Inputs para: nombre del hotdog y seleccion de ingredientes
    Para esto se muestran (enumerados) cada instancia de cada categoria
    (por ejmplo, se listan todos los panes y se le pide al usuario que seleccione uno)
    Retorna: Nuevo hotdog agregado al menu o None si se cancela el registro
    El hotdog creado es agregado al menu
    """
    from Hotdog import Hotdog
    print("\nCrear un nuevo hot dog\n")
    name = input("Nombre del nuevo hotdog: ").strip()
    # validar
    while not name:
        name = input("Nombre no puede estar vacío. Ingresa nombre: ").strip()

    def elegir_por_clase(cls, prompt, allow_skip=False):
        """
        Esta funcion muestra las opciones disponibles de una clase dada (categoria de ingrediente)
        Recibe: Clase del ingrediente a mostrar, prompt para el input, allow_skip para permitir omitir la seleccion
        Retorna: Instancia seleccionada o None si se omite
        """
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
        # mapeo
        valid_range = list(map(str, range(1, len(opciones)+1)))
        if allow_skip:
            valid_range.append("0")
        while num not in valid_range:
            num = input("Entrada inválida. Intenta de nuevo: ")
        if allow_skip and num == "0":
            return None
        return opciones[int(num)-1]

    def buscar_en_inventario_por_nombre(nombre, inventario):
        """
        Permite buscar un ingrediente en el inventario a partir de su nombre
        Recibe: Nombre del ingrediente a buscar
        Retorna: Numero del ingregiente en el inventario (key) y su cantidad
        """
        for k, v in inventario.items():
            if v[0].lower() == nombre.lower():
                return k, v[1]
        return None, None

    def validar_seleccion_e_inventario(obj, cls_name):
        """
        Valida que el objeto exista en el inventario y tenga al menos 1 unidad
        Si no existe, da opción de seleccionar otro o cancelar
        Si existe pero la cantidad es menor a 1, muestra advertencia y pide confirmación
        Recibe: objeto seleccionado y nombre de la clase (categoria)
        Retorna: 'OK' si todo bien, 'REPLACE' para repetir seleccion, 'CANCEL' para cancelar registro
        """
        if obj is None:
            return None  
        nombre = getattr(obj, 'name', str(obj))
        key, qty = buscar_en_inventario_por_nombre(nombre, inventario)
        if key is None:
            print(f"\nNo se encontró '{nombre}' en el inventario\n")
            opt = input("Deseas seleccionar otro ingrediente (s) o cancelar el registro (c)? (s/c): ")
            while opt.lower() not in ('s', 'c', 'si', 'n') and opt.lower() not in ('s','c'):
                opt = input("Entrada inválida. Escribe 's' para seleccionar otro o 'c' para cancelar: ")
            if opt.lower().startswith('s'):
                return 'REPLACE'
            else:
                return 'CANCEL'
        if qty < 1:
            print(f"Advertencia! No hay inventario suficiente de '{nombre}' (cantidad = {qty}).\n")
            opt = input("Deseas continuar con esta selección a pesar de todo? (s/n): ")
            while opt.lower() not in ('s', 'n', 'si', 'no'):
                opt = input("Entrada inválida. (s/n): ")
            if opt.lower().startswith('s'):
                return 'OK'
            else:
                return 'REPLACE'
        return 'OK'

    # Selección iterativa con validaciones
    while True:
        """
        Este bucle permite seleccionar el ingrediente, validando su existencia en inventario
        Se llaman a las funciones elegir_por_clase para listar todas las opciones de una categoria
        validar_seleccion_e_inventario para validar existencia y cantidad en inventario
        Sirve para confrimar que todas las condiciones se cumplan antes de proceder a crear el hotdog
        Es conveniente usar el while para que el programa siga pidiendo inputs hasta que sean logicos
        """
        # Pan (obligatorio)
        bread = elegir_por_clase(Bread, "Pan")
        if bread is None:
            print("\nNo se pueden crear hotdogs sin pan. Cancelando creación.\n")
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

    # una vez se supera el while se crea el nuevo hotdog
    nuevo = Hotdog(name, bread, sausage, topping, sauce, side)

    # Validar longitudes mediante método de la clase Hotdog (pide confirmación si no coinciden)
    try:
        ok_long = nuevo.validadr_longitud()
    except Exception:
        ok_long = nuevo.verificar_longitud()

    if not ok_long:
        print("\nNo se confirmó la longitud del hotdog. Registro cancelado.\n")
        return None

    # Verificar inventario final para todos los ingredientes seleccionados 
    # (si alguno queda sin stock, avisar)
    faltantes = []
    sin_stock = []
    seleccionados = [nuevo.bread, nuevo.sausage] # los que van ajuro
    for optional in (nuevo.sides, nuevo.sauces, nuevo.toppings): # pueden ir o no
        if optional is None:
            continue
        seleccionados.append(optional)

    for item in seleccionados:
        """
         Esta funcion busca un ingrediente en el inventario por nombre
         Sirve para validar existencia y cantidad en inventario de los elementos opcionales de un hotdog
         """
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
        """
        Esta seccion muestra los ingredientes faltantes en el inventario 
        """
        print("\nAdvertencia: los siguientes ingredientes no se encontraron en inventario.\n")
        for f in faltantes:
            print(f" - {f}")
        print("\nSe cancelará el registro para que el usuario seleccione ingredientes existentes.\n")
        return None

    if sin_stock:
        """
         Esta seccion muestra los ingredientes sin stock (cantidad menor a 1) en el inventario
         """
        print("\nAdvertencia! los siguientes ingredientes no tienen stock suficiente.\n")
        for s in sin_stock:
            print(f" - {s[0]} (cantidad = {s[1]})")
        opt = input("Deseas continuar y agregar el hotdog al menú igual? (s/n): ")
        while opt.lower() not in ('s','n','si','no'):
            opt = input("Entrada inválida. (s/n): ")
        if not opt.lower().startswith('s'):
            print("Creación cancelada por el usuario.")
            return None

    menu.append(nuevo)
    print(f"\nHotdog '{name}' creado y agregado al menú exitosamente!\n")
    return nuevo


def verificar_inventario_hotdog(hotdog, ingredientes, inventario):
    """
    Esta funcion verifica si hay inventario suficiente para crear un hotdog
    Revisa que cada ingrediente del hotdog exista en *inventario* y tenga al menos 1 unidad/porcion
    Valida longitudes entre pan y salchicha llamando a la funcion verificar_longitud de la clase Hotdog
    Recibe: Numero de hotdog a revisar
    Retorna: True si todo está bien, False en caso contrario
    """
    def buscar_en_inventario_por_nombre(nombre):
        """
        Esta funcion busca un ingrediente en el inventario por nombre
        Recibe: Nombre del ingrediente a buscar
        Retorna: Numero del ingregiente en el inventario (key) y su cantidad 
        """
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
            print("\nAdvertencia! la longitud o unidad del pan y la salchicha no coinciden.\n")
            resp = input("Deseas continuar con esta venta igualmente? (s/n): ").strip().lower()
            while resp not in ('s', 'n', 'si', 'no'):
                resp = input("Entrada inválida. (s/n): ").strip().lower()
            if not resp.startswith('s'):
                return False
    except Exception:
        pass

    if faltantes:
        print("\nNo se encontraron los siguientes ingredientes en inventario.\n")
        for f in faltantes:
            print(f" - {f}")
        return False

    if sin_stock:
        print("\nLos siguientes ingredientes no tienen stock suficiente:\n")
        for s in sin_stock:
            print(f" - {s[0]} (cantidad = {s[1]})")
        return False

    print("\nHay suficiente inventario para vender este hotdog.\n")
    return True



def gestion_ingredientes (ingredientes, menu, inventario):
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
        while borrar.isnumeric() == False or int(borrar) not in range(1, len(ingredientes)+1):
            borrar=input("ERROR. Ingresa el numero del ingrediente que deseas eliminar: ")

        idx = int(borrar)-1
        ingrediente_obj = ingredientes[idx]

        """ 
        Determinar hot dogs que usan este ingrediente 
        (comparando por nombre)
        """
        def uses_ingredient(hotdog, ing_name):
            def name_of(x):
                try:
                    return getattr(x, 'name', str(x)).lower()
                except Exception:
                    return str(x).lower()

            ing_name_l = ing_name.lower()
            if name_of(hotdog.bread) == ing_name_l:
                return True
            if name_of(hotdog.sausage) == ing_name_l:
                return True
            # sides, sauces, toppings pueden ser objetos o listas o strings
            for attr in ('sides', 'sauces', 'toppings'):
                val = getattr(hotdog, attr, None)
                if val is None:
                    continue
                if isinstance(val, list):
                    for it in val:
                        if name_of(it) == ing_name_l:
                            return True
                else:
                    if name_of(val) == ing_name_l:
                        return True
            return False

        ing_name = getattr(ingrediente_obj, 'name', str(ingrediente_obj))
        hotdogs_using = [h for h in menu if uses_ingredient(h, ing_name)]

        if hotdogs_using:
            print(f"\nEl ingrediente '{ing_name}' está siendo usado por {len(hotdogs_using)} hotdog(s) en el menu.\n")
            for h in hotdogs_using:
                print(f" - {h.name}")
            resp = input("Eliminar este ingrediente también eliminará los hot dogs listados. Confirma la acción? (s/n): ").strip().lower()
            while resp not in ('s','n','si','no'):
                resp = input("Entrada inválida. Responde 's' para sí o 'n' para no: ").strip().lower()
            if not resp.startswith('s'):
                print("\nOperación cancelada. No se eliminó nada.\n")
                return
            # Se eliminan ingrediente/s y hotdogs relacionados
            # Eliminar hotdogs del menú
            removed_names = [h.name for h in hotdogs_using]
            menu[:] = [h for h in menu if h not in hotdogs_using]
            # Eliminar ingrediente de la lista de ingredientes
            ingredientes.pop(idx)
            # Eliminar entrada del inventario que corresponda a este ingrediente
            keys_to_remove = [k for k,v in inventario.items() if v[0].lower() == ing_name.lower()]
            for k in keys_to_remove:
                inventario.pop(k, None)
            print("\nIngrediente y hot dogs relacionados eliminados correctamente!\n")
            for n in removed_names:
                print(f" - {n}")
            print("\n")
        else:
            # No hay hotdogs usando el ingrediente: confirmar eliminación 
            resp = input(f"¿Deseas eliminar el ingrediente '{ing_name}'? (s/n): ").strip().lower()
            while resp not in ('s','n','si','no'):
                resp = input("Entrada inválida. Responde 's' para sí o 'n' para no: ").strip().lower()
            if not resp.startswith('s'):
                print("\nOperación cancelada. No se eliminó nada.\n")
                return
            ingredientes.pop(idx)
            # Eliminar del inventario
            keys_to_remove = [k for k,v in inventario.items() if v[0].lower() == ing_name.lower()]
            for k in keys_to_remove:
                inventario.pop(k, None)
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

        """
        Esta opcion muestra los hotdogs del menu enumarandolos y le permite al usuario
        seleccionar uno y verificar si hay inventario suficiente para venderlo
        Criterio: el inventario debe ser mayor o igual a 1 para poder venderlo
        Recibe: Input del numero del hotdog a verificar
        Retorna: Mensaje de si hay o no inventario suficiente
        """
        for i, h in enumerate(menu):
            print(f"{i+1}. {h.name.capitalize()}")

        print("\n")
        num = input("Ingrese el número del hotdog a verificar: ")
        while num.isnumeric() == False or int(num) not in range(1, len(menu)+1):
            num = input("ERROR. Ingresa el numero del hotdog que verificar: ")

        hot = menu[int(num)-1]
        verificar_inventario_hotdog(hot, ingredientes, inventario)
        

    elif opcion_3=="3":
        """
        Esta opcion agrega un nuevo hotdog al menu
        NOTA: usa la funcion crear_hotdog
        Recibe: Input de todos los atributos del hotdog
        Retorna: Mensaje de confirmacion
        """
        print("\nAgregar un nuevo hot dog\n")
        try:
            crear_hotdog(menu, ingredientes, inventario)
        except Exception as e:
            print(f"\nOcurrió un error al crear el hotdog: {e}\n")



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
        # Verificar si hay suficiente inventario para seguir vendiendo este hotdog
        puede_vender = verificar_inventario_hotdog(hot, ingredientes, inventario)
        if puede_vender:
            # Si hay inventario, pedir confirmación antes de eliminar
            resp = input("Advertencia: aún hay inventario suficiente para vender este hotdog.\n¿Deseas eliminarlo de todas formas? (s/n): ").strip().lower()
            while resp not in ('s','n','si','no'):
                resp = input("Entrada inválida. Responde 's' para sí o 'n' para no: ").strip().lower()
            if not resp.startswith('s'):
                print("\nEliminación cancelada.\n")
            else:
                menu.pop(idx)
                print("\nEliminado correctamente!\n")
        else:
            # Si no ha inventario se elimina de una
            menu.pop(idx)
            print("\nEliminado correctamente!\n")

    elif opcion_3=="5":
        print("\nVolver a menu principal\n")


def escribrir_datos_json(file,ingredientes):
    """
    Esta funcion transforma la lista de ingredientes local (que parte de la informacion de la API)
    en un archivo json conservando el mismo formato de la api
    Recibe: nombre del archivo donde se guardara el json y la lista de ingredientes local
    Retorna: Nada. Crea el archivo json
    """

    # Agrupar por categoría de la misma manera que la api
    categorias = {
        "Pan": [],
        "Salchicha": [],
        "Acompañante": [],
        "Salsa": [],
        "toppings": []
    }

    for ing in ingredientes:
        # Declarar atributos de cada ingrediente de acuerdo a su clase
        try:
            if isinstance(ing, Bread):
                categorias["Pan"].append({
                    "nombre": ing.name,
                    "tipo": ing.type,
                    "tamaño": ing.size,
                    "unidad": ing.unit
                })
            elif isinstance(ing, Sausage):
                categorias["Salchicha"].append({
                    "nombre": ing.name,
                    "tipo": ing.type,
                    "tamaño": ing.size,
                    "unidad": ing.unit
                })
            elif isinstance(ing, Side):
                categorias["Acompañante"].append({
                    "nombre": ing.name,
                    "tipo": ing.type,
                    "tamaño": ing.size,
                    "unidad": ing.unit
                })
            elif isinstance(ing, Sauce):
                categorias["Salsa"].append({
                    "nombre": ing.name,
                    "base": getattr(ing, 'base', None),
                    "color": getattr(ing, 'color', None)
                })
            elif isinstance(ing, Topping):
                categorias["toppings"].append({
                    "nombre": ing.name,
                    "tipo": getattr(ing, 'type', None),
                    "presentación": getattr(ing, 'presentation', None)
                })
            else:
                # Fallback genérico: intentar serializar atributos conocidos
                d = {"nombre": getattr(ing, 'name', str(ing))}
                if hasattr(ing, 'type'):
                    d['tipo'] = getattr(ing, 'type')
                if hasattr(ing, 'size'):
                    d['tamaño'] = getattr(ing, 'size')
                if hasattr(ing, 'unit'):
                    d['unidad'] = getattr(ing, 'unit')
                categorias.setdefault('Otros', []).append(d)
        except Exception:
            continue

    # Construir la lista de categorías como la api
    salida = []
    for cat in ("Pan", "Salchicha", "Acompañante", "Salsa", "toppings"):
        salida.append({"Categoria": cat, "Opciones": categorias.get(cat, [])})


    try:
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(salida, f, indent=2)
    except Exception as e:
        print(f"Error al escribir JSON en {file}: {e}")

import random

def simular_dia(Hotdog, inventario):
    # Copia del inventario para reiniciar cada simulación
    inventario = inventario_inicial.copy()

    # Variables de control
    total_hot_dogs = 0
    clientes_cambiaron = 0
    clientes_sin_compra = 0
    ventas_por_tipo = {nombre: 0 for nombre in Hotdog.keys()}
    hotdogs_fallidos = []
    ingredientes_fallidos = []
    acompanantes_vendidos = 0

    # Simulación de clientes
    clientes_del_dia = random.randint(0, 200)
    print(f"Hoy llegaron {clientes_del_dia} clientes.\n")

    for i in range(clientes_del_dia):
        hot_dogs = random.randint(0, 5)

        if hot_dogs == 0:
            print(f"El cliente {i} cambió de opinión")
            clientes_cambiaron += 1
            continue

        print(f"\nCliente {i}: quiere {hot_dogs} hot dogs")
        seleccionados = []
        orden_valida = True

        for j in range(hot_dogs):
            seleccion = random.choice(list(Hotdog.keys()))
            detalle = Hotdog[seleccion]

            # Verificar inventario
            for ingrediente in detalle["Bread"] + detalle["Sausage"] + detalle["Topping"] + detalle["Sauce"] + detalle["Side"]:
                if inventario.get(ingrediente, 0) <= 0:
                    print(f"   No se pudo preparar '{seleccion.upper()}' por falta de: {ingrediente}")
                    print(f"   El cliente {i} se marchó sin llevarse nada")
                    clientes_sin_compra += 1
                    hotdogs_fallidos.append(seleccion)
                    ingredientes_fallidos.append(ingrediente)
                    orden_valida = False
                    break

            if not orden_valida:
                break

            # Restar inventario
            for ingrediente in detalle["Bread"] + detalle["Sausage"] + detalle["Topping"] + detalle["Sauce"] + detalle["Side"]:
                inventario[ingrediente] -= 1

            # Acompañante adicional
            adicional = random.choice([True, False])
            if adicional:
                acompanantes_vendidos += 1

            # Contar acompañantes del combo
            acompanantes_vendidos += len(detalle["Side"])

            print(f"   Hot dog {j+1}: {seleccion.upper()} (Acompañante adicional: {'Sí' if adicional else 'No'})")
            seleccionados.append(seleccion)
            ventas_por_tipo[seleccion] += 1

        if orden_valida:
            total_hot_dogs += hot_dogs
            print(f"    Cliente {i} compró: {', '.join(seleccionados)}")

    # --- Reporte final ---
    print("\n--- RESUMEN DEL DÍA ---")
    print(f"Total de clientes: {clientes_del_dia}")
    print(f"Clientes que cambiaron de opinión: {clientes_cambiaron}")
    print(f"Clientes que no pudieron comprar: {clientes_sin_compra}")
    print(f"Total de hot dogs vendidos: {total_hot_dogs}")
    print(f"Promedio de hot dogs por cliente: {total_hot_dogs / clientes_del_dia if clientes_del_dia > 0 else 0:.2f}")
    print(f"Hot dog más vendido: {max(ventas_por_tipo, key=ventas_por_tipo.get)}")
    print(f"Hot dogs que causaron que clientes se marcharan: {set(hotdogs_fallidos) if hotdogs_fallidos else 'Ninguno'}")
    print(f"Ingredientes que causaron que clientes se marcharan: {set(ingredientes_fallidos) if ingredientes_fallidos else 'Ninguno'}")
    print(f"Acompañantes vendidos (incluyendo combos): {acompanantes_vendidos}")