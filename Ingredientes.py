class Ingredient():

    def __init__(self,name,type,size,unit):
        self.name = name
        self.type = type
        self.size = size
        self.unit = unit

class Bread(Ingredient):

    def __init__(self, name, type, size, unit):
        super().__init__(name, type, size, unit)


class Sausage(Ingredient):

    def __init__(self, name, type, size, unit):
        super().__init__(name, type, size, unit)

class Side(Ingredient):

    def __init__(self, name, type, size, unit):
        super().__init__(name, type, size, unit)

class Sauce(Ingredient):
    def __init__(self,name,type,size,unit,base,color):
        super().__init__(name,type,size,unit)
        self.base = base
        self.color = color

class Topping(Ingredient):

    def __init__(self, name, type,size,unit,presentation):
        super().__init__(name, type,size,unit)
        self.presentation = presentation
