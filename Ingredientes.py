class Ingredient():

    def __init__(self,name,type,size,unit):
        self.name = name
        self.type = type
        self.size = size
        self.unit = unit

class Bread(Ingredient):

    def __init__(self, name, type, size, unit):
        super().__init__(name, type, size, unit)

    def mostrar(self):
        print(f"\n--Pan {self.name}--\n" \
        f"Tipo: {self.type}\n" \
        f"Tamaño: {self.size}\n" \
        f"Unidad:{self.unit}\n")

class Sausage(Ingredient):

    def __init__(self, name, type, size, unit):
        super().__init__(name, type, size, unit)

    def mostrar(self):
        print(f"\n--Salchicha {self.name}--\n"
              f"Tipo: {self.type}\n"
              f"Tamaño: {self.size}\n"
              f"Unidad: {self.unit}\n")

class Side(Ingredient):

    def __init__(self, name, type, size, unit):
        super().__init__(name, type, size, unit)

    def mostrar(self):
        print(f"\n--Acompañante: {self.name}--\n"
              f"Tipo: {self.type}\n"
              f"Tamaño: {self.size}\n"
              f"Unidad: {self.unit}\n")

class Sauce(Ingredient):
    def __init__(self,name,base,color):
        self.name = name
        self.base = base
        self.color = color
    
    def mostrar(self):
        print(f"\n--Salsa {self.name}--\n"
              f"Base: {self.base}\n"
              f"Color: {self.color}\n")

class Topping(Ingredient):

    def __init__(self, name, type,presentation):
        self.name = name
        self.type = type
        self.presentation = presentation

    def mostrar(self):
        print(f"\n--Topping: {self.name}--\n"
              f"Tipo: {self.type}\n"
              f"Presentación: {self.presentation}\n")
