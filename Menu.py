class Hotdog():

    def __init__(self,name,bread,sausage,toppings,sauces,sides):
        self.name = name
        self.bread = bread
        self.sausage = sausage
        self.toppings = toppings
        self.sauces = sauces
        self.sides =sides

    def mostrar(self):
        print(f"--{self.name}--\n"
              f"Pan: {self.bread}\n"
               f"Salchicha: {self.sausage}\n"
               f"Toppings: {self.toppings}\n"
                f"Salsas: {self.sauces}\n"
                f"Acompañantes: {self.sides}\n" )