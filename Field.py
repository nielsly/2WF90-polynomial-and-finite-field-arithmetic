from random import randint

from Poly import Poly, known_primes, find_irred


class Field:

    def __init__(self, m: int, poly: list or Poly):
        """
        Initialise a Field
        :param m: Modulus of the field
        :param poly: Polynomial modulus of the field
        """

        # Simple prime check for the modulo. We use a pre-generated list of primes, since we know p < 100:
        if m not in known_primes:
            raise ValueError("Modulus is not prime")

        self.m: int = m
        if type(poly) == list:
            self.poly: Poly = Poly(poly, self.m)
        else:
            self.poly: Poly = poly

    def order(self) -> int:
        """
        Calculates the order of a field
        :rtype: int
        :return: The order of the field
        """
        return self.m ** self.poly.deg()

    def reduce(self, f: Poly) -> Poly:
        """
        Reduces a polynomial to its smallest representative in the field
        :param f: The polynomial to reduce
        :return: The reduced form of f
        """
        return f % self.poly

    def elements(self) -> list:
        """
        Creates a list of all the elements in this field
        :return: List of Poly elements
        """
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
        """
        Generates an addition table for this field
        :return: A two-dimensional Poly array representing the addition table of this field
        """
        elements = self.elements()

        table = []
        for row in range(0, len(elements)):  # Generate row by row
            row_arr = []
            for column in range(0, len(elements)):
                row_arr.append(self.reduce(elements[row] + elements[column]))
            table.append(row_arr)

        return table

    def mult_table(self) -> list:
        """
        Generates the multiplication table of this field
        :return: A two-dimensional Poly array representing the multiplication table of this field
        """
        elements = self.elements()

        table = []
        for row in range(0, len(elements)):  # Generate row by row
            row_arr = []
            for column in range(0, len(elements)):
                row_arr.append(self.reduce(elements[row] * elements[column]))
            table.append(row_arr)

        return table

    def display(self, a: Poly) -> Poly:
        """
        Determines the unique representative of a polynomial in this field
        :param a: The polynomial for which the unique representative is returned
        :return: Returns the unique representative as a Poly
        """
        # If the degree of a is lower than the polynomial modulus, we can just return it
        if a.deg() < self.poly.deg():
            return a
        else:  # Otherwise, reduce it
            return self.reduce(a)

    def add(self, f: Poly, g: Poly) -> Poly:
        """
        Adds two polynomials together within the field.
        :param f: Polynomial 1
        :param g: Polynomial 2
        :return: The sum of f and g within this field
        """
        return (f + g) % self.poly

    def subtract(self, f: Poly, g: Poly) -> Poly:
        """
        Subtracts two polynomials within the field.
        :param f: Polynomial 1
        :param g: Polynomial 2
        :return: The subtraction result of f - g within this field
        """
        return (f - g) % self.poly

    def multiply(self, f: Poly, g: Poly):
        """
        Multiplies two polynomials within the field
        :param f: Polynomial 1
        :param g: Polynomial 2
        :return: The product of f and g within this field
        """
        return (f * g) % self.poly

    def equals(self, f: Poly, g: Poly):
        """
        Determine whether two polynomials are equal within the field
        :param f: Polynomial 1
        :param g: Polynomial 2
        :return: True when f and g are equal, False otherwise
        """
        return (f % self.poly) == (g % self.poly)

    def divide(self, f: Poly, g: Poly) -> Poly:
        """
        Divide two polynomials in this field.
        :param f: Polynomial 1
        :param g: Polynomial 2
        :return: The result of f/g as a Poly
        """
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

    def inverse(self, a: Poly) -> Poly:
        """
        Find the inverse of a polynomial within this field, based on algorithm 3.3.3 from the script
        :param a: Polynomial to find the inverse of
        :return: The inverse of a. Raises an AssertionError when a is irreducible in a
        """
        gcd = a.euclid(self.poly)

        if gcd[2] == Poly([1]):
            return self.reduce(gcd[0])
        else:  # Polynomial is irreducible
            raise AssertionError

    def is_primitive(self, a: Poly) -> bool:
        """
        Check is a polynomial is primitive is in this field. Based on algorithm 4.4.3
        :param a: The polynomial to check for primitivity
        :return: True if a is primitive, False otherwise
        """
        q = self.order()
        p = get_prime_divisors(q - 1)
        k = len(p)
        i = 0

        while i < k and self.reduce(a.pow((q - 1) // p[i])) != Poly(1, self.m):
            i += 1

        return i >= k

    def find_prim(self, give_all: bool = True) -> list or Poly:
        """
        Find a primitive element in this field. Based on algorithm 4.4.4
        :param give_all: Whether to return all primitives or just one. If False, a random one will be selected.
        :return: A list of primitive elements of this field or a single primitive element.
        """
        assert (self.poly.irreducible())

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


def get_prime_factors(n: int) -> list:
    """
    Get all the prime factors of an integer n. Uses brute force and should therefore only be used on relatively small
    numbers. Taken from https://stackoverflow.com/a/22808285/5627123
    :param n: The integer to factor
    :return: An array containing the prime factors of n
    """
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
    """
    Get the unique prime divisors of an integer n
    :param n: The integer to get the prime divisors of
    :return: An array containing the unique prime divisors of n
    """
    p = get_prime_factors(n)
    divisors = []
    for i in p:
        if i not in divisors:
            divisors.append(i)
    return divisors


def poly_table_pretty(polys: list) -> list:
    """
    Format a table in the same way as the answer
    :param polys: The table to format
    :return: The formatted table
    """
    for i in range(0, len(polys)):
        for j in range(0, len(polys)):
            polys[i][j] = str(polys[i][j])
    return polys


# Replace the polynomials in the table with an array of their coefficients, so we can print it correctly
def poly_table(polys: list) -> list:
    """
    Replaces all Poly's in the table by their coefficients, so it can be used in an answer
    :param polys: The table to do the replace operations on
    :return: The table with the Poly's replaced by their coefficient array
    """
    for i in range(0, len(polys)):
        for j in range(0, len(polys)):
            polys[i][j] = polys[i][j].data
    return polys
