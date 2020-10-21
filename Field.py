from Poly import Poly, known_primes, find_irred
from random import randint


class Field:
    # initialise the Field, modulus must be a prime int, poly can be inputted as list or Poly
    def __init__(self, m: int, poly: list or Poly):
        # simple prime check for the modulo. We use a pre-generated list of primes, since we know p < 100:
        if m not in known_primes:
            raise ValueError("Modulus is not prime")

        self.m: int = m
        if type(poly) == list:
            self.poly: Poly = Poly(poly, self.m)
        else:
            self.poly: Poly = poly

    def order(self) -> int:
        return self.m ** self.poly.deg()

    def reduce(self, f: Poly) -> Poly:
        return f % self.poly

    # Get all elements of a field
    def elements(self) -> list:
        elements = []
        poly_data = [0] * (self.poly.deg())

        # We will treat this problem as if we are trying to print a decimal number in radix X
        # We simply loop over all possible decimal numbers and then transform them into polynomials
        for i in range(0, self.order()):
            i_copy = i
            for j in range(0, self.poly.deg()):
                v = i_copy // (self.m ** (self.poly.deg() - j - 1))
                i_copy -= v * (self.m ** (self.poly.deg() - j - 1))
                poly_data[j] = v
            elements.append(Poly(poly_data, self.m))

        return elements

    def add_table(self) -> list:
        elements = self.elements()
        table = []
        for row in range(0, len(elements)):
            row_arr = []
            for column in range(0, len(elements)):
                row_arr.append(self.reduce(elements[row] + elements[column]))
            table.append(row_arr)

        return table

    def mult_table(self) -> list:
        elements = self.elements()
        table = []
        for row in range(0, len(elements)):
            row_arr = []
            for column in range(0, len(elements)):
                row_arr.append(self.reduce(elements[row] * elements[column]))
            table.append(row_arr)

        return table

    def display(self, a: Poly) -> Poly:
        if a.deg() < self.poly.deg():
            return a
        else:
            return self.reduce(a)

    def add(self, f: Poly, g: Poly) -> Poly:
        return (f + g) % self.poly

    def subtract(self, f: Poly, g: Poly) -> Poly:
        return (f - g) % self.poly

    def multiply(self, f: Poly, g: Poly):
        return (f * g) % self.poly

    def equals(self, f: Poly, g: Poly):
        return (f % self.poly) == (g % self.poly)

    # Divide two polynomials in a field (not sure if it will work for 100% of the problems
    def divide(self, f: Poly, g: Poly) -> Poly:
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
    def inverse(self, a: Poly) -> Poly:
        gcd = a.euclid(self.poly)

        if gcd[2] == Poly([1]):
            return self.reduce(gcd[0])
        else:
            raise AssertionError

    # Check if an element is primitive in a field
    # Based on algorithm 4.4.3
    def is_primitive(self, a: Poly) -> bool:
        q = self.order()
        p = get_prime_divisors(q - 1)
        k = len(p)
        i = 0

        while i < k and self.reduce(a.pow((q - 1) // p[i])) != Poly(1, self.m):
            i += 1

        return i >= k

    # Find a primitive element in the field
    # Based on algorithm 4.4.4
    def find_prim(self, give_all: bool = True) -> list or Poly:
        assert(self.poly.irreducible())

        irreducibles = []
        primitives = []
        for d in range(0, self.poly.deg()):
            irreducibles += find_irred(self.m, d)
        for n in irreducibles:
            if self.is_primitive(n):
                primitives.append(n)
        if give_all:
            return primitives
        return primitives[randint(0, len(primitives) - 1)]


# Brute force prime factor algorithm based on https://stackoverflow.com/a/22808285/5627123
# Only to be used on relative small numbers
def get_prime_factors(n: int) -> list:
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)

    if n > 1:
        factors.append(n)
    return factors


def get_prime_divisors(n: int) -> list:
    p = get_prime_factors(n)
    divisors = []
    for i in p:
        if i not in divisors:
            divisors.append(i)
    return divisors


# Format the table in the same way as the answer
def poly_table_pretty(polys: list) -> list:
    for i in range(0, len(polys)):
        for j in range(0, len(polys)):
            polys[i][j] = str(polys[i][j])
    return polys


# Replace the polynomials in the table with an array of their coefficients, so we can print it correctly
def poly_table(polys: list) -> list:
    for i in range(0, len(polys)):
        for j in range(0, len(polys)):
            polys[i][j] = polys[i][j].data
    return polys
