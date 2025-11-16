

class Hotdog():

    def __init__(self,name,bread,sausage,toppings,sauces,sides):
        self.name = name
        self.bread = bread
        self.sausage = sausage
        self.toppings = toppings
        self.sauces = sauces
        self.sides =sides

    def mostrar(self):
        def _name(x):
            # Si el ingrediente es un objeto con atributo name, usarlo; si es lista, mapear nombres
            try:
                if isinstance(x, list):
                    return ", ".join([getattr(i, 'name', str(i)).capitalize() for i in x])
                return getattr(x, 'name', str(x)).capitalize()
            except Exception:
                return str(x)

        print(f"--{self.name}--\n"
              f"Pan: {_name(self.bread)}\n"
               f"Salchicha: {_name(self.sausage)}\n"
               f"Toppings: {_name(self.toppings)}\n"
                f"Salsas: {_name(self.sauces)}\n"
                f"Acompañantes: {_name(self.sides)}\n" )
        
    def verificar_longitud(self):
        if self.bread.size == self.sausage.size and self.bread.unit == self.sausage.unit:
            longitud_valida = True
        else:
            longitud_valida = False
        return longitud_valida
    
    def validadr_longitud(self):
        """Valida interactivamente la longitud entre pan y salchicha.
        Si no coinciden, muestra advertencia y pide confirmación al usuario.
        Retorna True si la longitud es válida o el usuario confirma, False en caso contrario.
        """
        try:
            if self.verificar_longitud():
                return True
            print("\nAdvertencia: la longitud o unidad del pan y la salchicha no coinciden.")
            resp = input("¿Deseas continuar con estas selecciones? (s/n): ").strip().lower()
            while resp not in ('s', 'n', 'si', 'no'):
                resp = input("Entrada inválida. Responde 's' para sí o 'n' para no: ").strip().lower()
            return resp.startswith('s')
        except Exception:
            return False
    
    def seleccion_ingrediente(self,ingredientes):

        print(" 1. Pan\n 2. Salchicha\n 3. Acompañante\n 4. Salsa\n 5. Topping\n")
        Listado=input ("Ingresa el listado que quieres ver: ")
        while Listado not in ["1", "2","3","4","5"]:
            Listado=input("ERROR: Ingresa una opción: ")
        
        Listado = int(Listado)
        target_class = ""

        if Listado == 1:
            target_class = self.bread
            

        elif Listado == 2:
            target_class = self.sausage
        elif Listado == 3:
            target_class = self.sides
        elif Listado == 4:
            target_class = self.sauces
        elif Listado == 5:
            target_class = self.toppings

        if target_class:
            found = False
            for i in ingredientes:
                if isinstance(i, target_class):
                    for i, n in enumerate(ingredientes):
                        print(f"{i+1}. {n.name.capitalize()}")

                    print("\n")
                    num=input("Ingresa el numero del hotdog que deseas eliminar: ")
                    while num.isnumeric() == False or int(num) not in range(0, len(ingredientes)+1):
                        num=input("Ingresa el numero del hotdog que deseas eliminar: ")

            if not found:
                print("\nNo se encontraron ingredientes en esta categoría.\n")

