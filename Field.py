from Poly import Poly


class Field:

    def __init__(self, mod: int, poly: list or Poly):
        self.mod = mod
        if type(poly) == list:
            self.poly = Poly(poly, mod)
        else:
            self.poly = poly

    def add(self, f: Poly, g: Poly):
        return (f + g) % self.poly

    def subtract(self, f: Poly, g: Poly):
        return (f - g) % self.poly
