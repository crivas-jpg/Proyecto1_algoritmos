
class Hotdog():
    def __init__(self,name,bread,sausage,toppings,sauces,sides):
        self.name = name
        self.bread = bread
        self.sausage = sausage
        self.toppings = toppings
        self.sauces = sauces
        self.sides =sides

    def mostrar(self):
        """
        Muestra la informacion del hotdog creado"""
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
        """
        Verifica si la longitud y unidad del pan y la salchicha son iguales
        Retorna True si coinciden, False si no
        """
        try:
            bread = self.bread
            sausage = self.sausage
            if not bread or not sausage:
                return False
            bread_size = getattr(bread, 'size', None)
            bread_unit = getattr(bread, 'unit', None)
            sausage_size = getattr(sausage, 'size', None)
            sausage_unit = getattr(sausage, 'unit', None)
            if bread_size is None or bread_unit is None or sausage_size is None or sausage_unit is None:
                return False
            return (str(bread_size).strip().lower() == str(sausage_size).strip().lower() and
                    str(bread_unit).strip().lower() == str(sausage_unit).strip().lower())
        except Exception:
            return False


class Hotdog():

    def __init__(self,name,bread,sausage,toppings,sauces,sides):
        self.name = name
        self.bread = bread
        self.sausage = sausage
        self.toppings = toppings
        self.sauces = sauces
        self.sides =sides

    def mostrar(self):
        """
        Muestra la informacion del hotdog creado"""
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
    
    def validadr_longitud(self):
        """Funcion para validar la longitud entre pan y salchicha,
        se busca que sean iguales
        En caso de que no sean compatibles le muestra una advertencia 
        al usuario y le pide confirmar la accion
        Recibe: nada
        Retorna: True si la longitud es válida o el usuario confirma, False en caso contrario
        """
        try:
            if self.verificar_longitud():
                return True
            print("\nAdvertencia: la longitud o unidad del pan y la salchicha no coinciden.")
            resp = input("Desea continuar con estas selecciones? (s/n): ").strip().lower()
            while resp not in ('s', 'n', 'si', 'no'):
                resp = input("Entrada inválida. Responde 's' para sí o 'n' para no: ").strip().lower()
            return resp.startswith('s')
        except Exception:
            return False
    
    