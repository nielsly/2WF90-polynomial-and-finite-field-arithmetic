from Poly import Poly


class Field:

    def __init__(self, mod: int, poly: list or Poly):
        self.mod = mod
        if type(poly) == list:
            self.poly = Poly(poly, mod)
        else:
            self.poly = poly

    def reduce(self, f: Poly):
        return f % self.poly

    def add(self, f: Poly, g: Poly):
        return (f + g) % self.poly

    def subtract(self, f: Poly, g: Poly):
        return (f - g) % self.poly
    
    def multiply(self, f: Poly, g:Poly):
        return f * g % self.poly

    def equals(self, f: Poly, g: Poly):
        return (f % self.poly) == (g % self.poly)

    # Divide two polynomials in a field
    def divide(self, f: Poly, g: Poly):
        assert g != Poly([0])  # Make sure we don't divide by zero

        # First mod out the polynomials modulus to make sure we are working with the polynomials in their smallest form
        poly1 = self.reduce(f)
        poly2 = self.reduce(g)
        if (poly1 / poly2)[1] != Poly([0]):  # Check whether rest is zero
            poly1 = poly1 + self.poly  # Since we are operating a field, add the polynomial modulus
            if (poly1 / poly2)[1] != Poly([0]):
                poly1 = f - self.poly  # And here subtract in case adding did not give us a nice result
                if (poly1 / poly2)[1] != Poly([0]):
                    raise AssertionError  # All options are exhausted, abort
                else:
                    return (poly1 / poly2)[0]
            else:
                return (poly1 / poly2)[0]
        else:
            return (poly1 / poly2)[0]

    # Find an inverse, based on algorithm 3.3.3 from the script
    def inverse(self, a: Poly):
        gcd = a.euclid(self.poly)
        if gcd[2] == Poly([1]):
            return self.reduce(gcd[0])
        else:
            raise AssertionError
