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
        f"Unidad:{self.unit}\n")

class Sausage(Ingredient):

    def __init__(self, name, type, size, unit):
        super().__init__(name, type, size, unit)

    def mostrar(self):
        print(self.name, self.type, self.size, self.unit)

class Side(Ingredient):

    def __init__(self, name, type, size, unit):
        super().__init__(name, type, size, unit)

    def mostrar(self):
        print(self.name, self.type, self.size, self.unit)

class Sauce(Ingredient):
    def __init__(self,name,type,size,unit,base,color):
        super().__init__(name,type,size,unit)
        self.base = base
        self.color = color
    
    def mostrar(self):
        print(self.name, self.base, self.color)

class Topping(Ingredient):

    def __init__(self, name, type,size,unit,presentation):
        super().__init__(name, type,size,unit)
        self.presentation = presentation

    def mostrar(self):
        print(self.name, self.type, self.presentation)
