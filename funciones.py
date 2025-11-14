import requests
from Menu import *
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

ingredientes = llamada_api(url_ingredientes)
menu = llamada_api(url_menu)

def construir_menu():
    nuevo_menu=[]
    for i in menu:
        name = i["nombre"]
        bread = i["Pan"]
        sausage = i["Salchicha"]
        toppings = i["toppings"]
        if 'Salsas' in menu:
            sauce = i["Salsas"]
        else:
            sauce = i['salsas']
        side = i["Acompañante"]
        Hotdog(name,bread,sausage,toppings,sauce,side)
        nuevo_menu.append(Hotdog)
    #forzar tolerante a la salsa
    print(nuevo_menu)

def construir_ingredientes():
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
                Bread (name,type,size,unit)
                nuevos_ingredientes.append (Bread )
        elif category=="Salchicha":
            for j in opcion:
                name=j["nombre"]
                type=j["tipo"]
                size=j["tamaño"]
                unit=j["unidad"]
                Sausage (name,type,size,unit)
                nuevos_ingredientes.append (Sausage)
        elif category=="Acompañante":
            for j in opcion:
                name=j["nombre"]
                type=j["tipo"]
                size=j["tamaño"]
                unit=j["unidad"]
                Side(name,type,size,unit)
                nuevos_ingredientes.append (Side)
        elif category=="Salsa":
            for j in opcion:
                name=j["nombre"]
                type=''
                size=''
                unit=''
                base=j["base"]
                color=j["color"]
                Sauce(name,base,color)
                nuevos_ingredientes.append (Sauce)
        elif category=="toppings":
           for j in opcion:
                name=j["nombre"]
                type=j["tipo"]
                size=''
                unit=''
                presentation=j["presentación"]
                Topping(name,type,presentation)
                nuevos_ingredientes.append (Topping) 

    print(nuevos_ingredientes)


construir_menu()
construir_ingredientes()