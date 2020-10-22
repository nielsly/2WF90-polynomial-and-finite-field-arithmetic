from random import randint


# Class representing polynomials with several functions to help in polynomial manipulation
class Poly:
    def __init__(self, a: list or str or int, m: int = 0, degree=0):
        """
        Initializes a Poly
        :param a: input polynomial in a different representation, either as a `list`, a `str`, or an `int`.
        `list`s are to be given given in the format `[X^n,...,X,1]`.
        `str`s are to be given in the format `X^n + ... X + 1` or `X^n+...+X+1`
        `int`s are to be given as a number
        :param m: modulus of the polynomial, standard 0 (i.e. numbers are never reduced)
        :param degree: degree of the polynomial, only needed for `int`s, standard 0 (i.e. polynomial is simply a number)
        """
        # set modulus of polynomial
        self.m: int = m

        # if polynomial is a string
        if type(a) == str:
            # split on all spaces to get the terms and the signs
            a = a.split(' ')

            # add spaces if there weren't any
            if len(a) == 1:
                # split string on `+`, then join with ` + `, split on `-` then join with ` - `
                if a[0].startswith('-'):
                    # if first number is negative add a minus sign to the front
                    a = '-' + ' - '.join(' + '.join(a[0][1:].split('+')).split('-'))
                else:
                    a = ' - '.join(' + '.join(a[0].split('+')).split('-'))
                # split it into terms and signs
                a = a.split(' ')

            # split the first term on `^`, to seperate each term into the coefficient * X and the degree
            spl = a[0].split('^')

            # set `degree` of polynomial
            if len(spl) > 1:
                # if first term has a degree > 1
                # `degree` = degree of term
                degree = int(spl[1])
            elif spl[0].endswith('X'):
                # else if the degree of the term is 1, set `degree` to 1
                degree = 1
            else:
                # set `degree` to 0 if the only term is a coefficient or 0 (technically incorrect for 0)
                # to make sure if someone enters a non-zero degree in the parameters the class does not use that one
                degree = 0

            # create new `list` of length `degree + 1` which will hold the `list` representation of the polynomial
            p = [0] * (degree + 1)

            # get coefficient of first term
            if spl[0].endswith('X'):
                # if term ends on X
                if spl[0] == '-X':
                    # if term is `"-X"`, set coefficient as -1
                    p[0] = -1
                elif spl[0] == 'X':
                    # else if term is "X". set coefficient as 1
                    p[0] = 1
                else:
                    # else set coefficient to the number before `"X"`
                    p[0] = int(spl[0][:-1])
            else:
                # if term does not end on X, it is a coefficient already, set it to be that coefficient
                p[0] = int(spl[0])

            # get coefficients of other terms
            for i in range(2, len(a), 2):
                # increase in steps of 2, with the sign in `i - 1` and the term in `i`
                if a[i - 1] == '-':
                    # if sign is negative negate the term
                    a[i] = '-' + a[i]

                # split into term and degree
                spl = a[i].split('^')

                # if term ends on `"X"`
                if spl[0].endswith('X'):
                    if spl[0] == '-X' or spl[0] == "X":
                        # if term is `"-X"` or `"X"`
                        if len(spl) == 1:
                            # if degree of term is 1
                            # set coefficient p_{`degree` - 1} to 1 if sign is positive, else to -1
                            p[degree - 1] = 1 if a[i - 1] == '+' else -1
                        else:
                            # if degree is higher than 1
                            # set coefficient p_{`degree` - degree of term} to 1 if sign is positive, else to -1
                            p[degree - int(spl[1])] = 1 if a[i - 1] == '+' else -1
                    else:
                        # if term has coefficient
                        if len(spl) == 1:
                            # if term has no degree
                            # set coefficient p_{`degree` - 1} to coefficient
                            p[degree - 1] = int(spl[0][:-1])
                        else:
                            # if term has a degree
                            # set coefficient p_{`degree` - degree of term} to coefficient
                            p[degree - int(spl[1])] = int(spl[0][:-1])
                else:
                    # if term is only coefficient or 0, set final term p_n to coefficient
                    p[degree] = int(spl[0])

            if m != 0:
                # if modulus is not 0, reduce all terms of `p`
                for i in range(len(p)):
                    p[i] %= m
            # set `data` of the `Poly` to be the `list` representation of the polynomial.
            self.data: list = p
            # trim any leading zeroes
            self.trim()
        elif type(a) == int:
            # if input was only a coefficient
            if degree < 0:
                # if invalid `degree` was entered, throw an error
                raise ValueError('When declaring a Poly with an int, a non-negative degree is also required.')
            # else set `data` of `Poly` to be a list consisting of the coefficient and `degree` trailing zeroes
            self.data: list = [0] * (degree + 1)
            self.data[0] = a
        elif type(a) == list:
            # if input was the `list` representation
            if m != 0:
                # if modulus is not 0, reduce all terms
                for i in range(len(a)):
                    a[i] %= m
            # set `data` of the `Poly` to be the `list` representation of the polynomial.
            self.data: list = a
            # trim any leading zeroes
            self.trim()
        else:
            # else throw error
            raise TypeError('Type Poly requires type str, int or list, not ' + str(type(a)))

    def deg(self) -> int:
        """
        Gets the degree of the polynomial
        :return: `int` degree
        """
        # return (length of data - index of first non-zero element) - 1
        for i, e in enumerate(self.data):
            if e != 0:
                return len(self.data) - i - 1
        # return -1 if Poly = 0
        return -1

    def lc(self) -> int:
        """
        Gets the leading coefficient of the polynomial
        :return: `int` leading coefficient
        """
        # return first non-zero element
        for n in self.data:
            if n != 0:
                return n
        # return 0 if Poly = 0
        return 0

    def __str__(self, spaces: bool = False) -> str:
        """
        Gets the string representation of the polynomial, can have spaces
        :param spaces: boolean whether to add spaces to the output
        :return: `str` representation of the polynomial
        """
        # get degree
        degree = self.deg()

        # reverse the elements of `data` to make construction easier
        self.data.reverse()
        # initialize output as empty string
        out = ""
        for i in range(degree, -1, -1):
            # loop over all terms, starting with the first term (at index `degree` due to us reversing the list)
            # get term
            n = self.data[i]
            if n != 0:
                # if term is non-zero we print it
                if n > 0 and i != degree:
                    # if if term is larger than 0 and it is not the first term
                    # add the sign, with spaces if specified
                    if spaces:
                        out += " + "
                    else:
                        out += "+"
                elif n < 0:
                    # if if term is smaller than 0 and the degree is not 0
                    # add the sign, with spaces if specified, excluding the first term
                    if i == degree or not spaces:
                        out += "-"
                    else:
                        out += " - "
                if abs(n) != 1 or i == 0:
                    # if coefficient is not 1 or -1 or if degree is 0
                    # add the coefficient excluding the sign
                    out += str(abs(n))
                if i > 0:
                    # if degree is larger than 0
                    # add `"X"` to the term
                    out += "X"
                    if i > 1:
                        # if degree is larger than 1
                        # add power degree
                        out += "^" + str(i)
        # reverse the `data` again now that we are done
        self.data.reverse()

        # output `str` representation of the polynomial, `"0"` if empty string was not altered, as all elements are 0
        return out if out != "" else str(0)

    def __repr__(self) -> str:
        """
        Gets the string representation of the polynomial when printing to console, wrapper for `str()`
        :return: `str` representation of the polynomial
        """
        return str(self)

    # * for poly
    def __mul__(self, other):
        """
        Multiplies a polynomial with an integer or a polynomial with a polynomial
        :param other: `int` or `Poly` to multiply the polynomial with
        :return: `Poly` the polynomial multiplied by `other`
        """
        # copy the polynomial's `data` as `a'`, get its length as `n`
        ap = self.data.copy()
        n = len(ap)

        if type(other) == int:
            # if other was an integer
            for i in range(n):
                # multiply each term by that integer
                ap[i] *= other

            # and output polynomial with list representation `ap`
            return Poly(ap, self.m)

        # else copy the other polynomial as `b'` and get its length as `m`
        bp = other.data.copy()
        m = len(bp)

        # reverse `a'` and `b'` for easier multiplication
        ap.reverse(), bp.reverse()

        # get maximal length of product and initialize it as a string of that many zeroes
        length = n + m - 1
        p = [0] * length

        for i in range(n):
            # loop over all elements in `a'`
            for j in range(m):
                # loop over all elements in `b'`
                if ap[i] != 0 and bp[j] != 0:
                    # if either term is not `0`, multiply the two terms and add their degrees
                    p[i + j] += ap[i] * bp[j]
        # reverse product to get final `list` representation of the product polynomial
        p.reverse()
        # output the product
        return Poly(p, self.m)

    def __add__(self, other):
        """
        Adds a polynomial or integer to the polynomial
        :param other: `int` or `Poly` to add to polynomial
        :return: `Poly` the polynomial with `other` added
        """
        # get copy of the polynomial `a'`
        ap = self.data.copy()
        if type(other) == int:
            # if `other` was an integer, add it to the final term
            ap[-1] += other
            # output the polynomial with the integer added
            return Poly(ap, self.m)

        # copy `data` of `other` as `b'`
        bp = other.data.copy()

        # reverse the `data`s for easier manipulation
        ap.reverse(), bp.reverse()

        # pad with zeroes if the second polynomial has more terms
        # first get the lengths as `n` and `m`
        n, m = len(ap), len(bp)
        # then add `m - n` zeroes to the end of the `data` (i.e. add leading zeroes to the polynomial)
        ap += [0] * (m - n)
        for i in range(m):
            # loop over all elements
            # add elements at the same indices with eachother if `b'`s element is non-zero
            if bp[i] != 0:
                ap[i] += bp[i]
        # reverse `data` again to get final `list` representation
        ap.reverse()
        # output the polynomial with `other` added
        return Poly(ap, self.m)

    def __sub__(self, other):
        """
        Subtracts a polynomial or integer from the polynomial
        :param other: `int` or `Poly` to subtract from polynomial
        :return: `Poly` the polynomial with `other` subtracted
        """
        # get copy of the polynomial `a'`
        ap = self.data.copy()
        if type(other) == int:
            # if `other` was an integer, subtract it from the final term
            ap[-1] -= other
            # output the polynomial with the integer subtracted
            return Poly(ap, self.m)

        # copy `data` of `other` as `b'`
        bp = other.data.copy()

        # reverse the `data`s for easier manipulation
        ap.reverse(), bp.reverse()

        # pad with zeroes if the second polynomial has more terms
        # first get the lengths as `n` and `m`
        n, m = len(ap), len(bp)
        # then add `m - n` zeroes to the end of the `data` (i.e. add leading zeroes to the polynomial)
        ap += [0] * (m - n)
        for i in range(m):
            # loop over all elements
            # subtract element of `b'` from `a'`s element if it is non-zero
            if bp[i] != 0:
                ap[i] -= bp[i]
        # reverse `data` again to get final `list` representation
        ap.reverse()
        # output the polynomial with `other` subtracted
        return Poly(ap, self.m)

    def copy(self):
        """
        Makes copy of the polynomial
        :return: `Poly` copy of the polynomial
        """
        return Poly(self.data, self.m)

    def __truediv__(self, other):
        """
        (Modular) long division for polynomials
        Based on algorithm 2.2.6 of the reader with adjustments made for modular arithmetic
        :param other: `Poly` or `int` to divide the polynomial with
        :return: (`Poly`,`Poly`) the quotient of the polynomial divided by `other` and the remainder
        """
        if other == 0:
            # throw error if division by 0 is attempted
            raise ZeroDivisionError("Division by zero attempted on " + str(self) + " and " + str(other) + ".")

        if type(other) == int:
            # if other is an `int`, make it a polynomial to make calculation easier
            other = Poly(other, self.m)

        # intialize quotient as empty list of length equal to the polynomial
        q = [0] * len(self)
        # copy the polynomial as `r`
        r = self.copy()

        # get degrees of `r` and `other`
        deg_r, deg_b = r.deg(), other.deg()

        lc_b = other.lc()

        while deg_r >= deg_b:
            # We need to eliminate the highest order coefficient
            # We can safely loop through all possibilities, since we know that m < 100
            lc_div = 1
            lc_r = r.lc()
            for i in range(1, self.m + 1):
                if (lc_r - i * lc_b) % self.m == 0:
                    lc_div = i
                    break

            # q <- lc(r)/lc(b) * X^{deg(r)-deg(b)}
            q[deg_r - deg_b] += lc_div

            n = Poly(lc_div, self.m, deg_r - deg_b)
            nb = n * other
            # r <- r - lc(r)/lc(b) * X^{deg(r)-deg(b)} * b
            r = (r - nb) % self.m
            deg_r = r.deg()

        # reverse `q` to get the final `list` representation of the quotient polynomial
        q.reverse()
        # output quotient and remainder with leading zeroes removed
        return Poly(q, self.m), r.trim()

    def gcd(self, other):
        """
        Gets GCD of the polynomial with some other polynomial or integer, uses `euclid`
        :param other: `Poly` or `int` to get GCD of the polynomial with
        :return: `Poly` the GCD of the two inputs
        """
        return self.euclid(other)[2]

    # extended euclidean algorithm for polynomials
    # Based on algorithm 2.2.11 from the script
    def euclid(self, other):
        """
        The Extended Euclidian algorithm for polynomials
        Based on algorithm 2.2.11 from the reader
        :param other: `Poly` or `int` `b` to divide the polynomial `a` by
        :return: (`Poly`,`Poly`,`Poly`) `x`, `y`, and `GCD` of `a,b` with `GCD = xa + yb`
        """
        if type(other) == int:
            # if other is an `int`, make it a polynomial to make calculation easier
            other = Poly(other, self.m)

        # set x,v,y,u according to the algo
        x, v, y, u = Poly(1, self.m), Poly(1, self.m), Poly(0, self.m), Poly(0, self.m)
        # get `a, b` as copies of the input polynomials
        a, b = self.copy(), other.copy()
        while b != 0:
            q, r = a / b
            a = b
            b = r
            # x' = x, y' = y
            xp = x
            yp = y
            x = u
            y = v
            # u = x' - qu, v = y' - qv
            u = xp - q * u
            v = yp - q * v

        # get modular inverse lc(a)^-1
        lc_a_inv = modular_inverse(a.lc(), self.m, True)
        x *= lc_a_inv
        y *= lc_a_inv
        # output x*lc(a)^{-1}, y*lc(a)^{-1} and the gcd(a,b)
        return x, y, self * x + other * y

    def __len__(self) -> int:
        """
        Get length of polynomial `data` excluding leading zeroes
        :return: `int` length of polynomial
        """
        # return length of data - index of first non-zero element
        for i, e in enumerate(self.data):
            if e != 0:
                return len(self.data) - i
        # return 1 if Poly == 0 or if `data` == [] (as then it should be [0])
        return 1

    # remove leading zeroes
    def trim(self):
        """
        Trim leading zeroes from the polynomials `data` inplace
        :return: `Poly` the polynomial with `data` not having any leading zeroes
        """
        # if `data` is empty set it to be [0] (should not happen)
        if len(self.data) == 0:
            self.data = [0]
        # remove any leading zeroes using the len(Poly) function, which returns the length without any zeroes
        # This allows us to use it to find the index where the first non-zero element is
        self.data = self.data[len(self.data) - len(self):]
        return self

    def __mod__(self, m):
        """
        Modulo for polynomials, if input is `int`, all coefficients are reduced by that number, if input is `poly`, then
        we use long division and get the remainder
        :param m: `Poly` or `int` modulus
        :return: `Poly` the reduced polynomial
        """
        if type(m) == int:
            # if modulus is integer
            if m != 0:
                # and is not 0
                # copy the polynomial as `a`
                a = self.data.copy()
                for i in range(len(a)):
                    # loop over each element in the polynomial
                    # and reduce the coefficient by `m`
                    a[i] %= m
                # output reduced polynomial
                return Poly(a, self.m)
            else:
                # if m = 0
                # the polynomial taken mod 0 gives the polynomial itself
                return self
        elif type(m) == Poly:
            if m.deg() + 1 == 0:
                # apparently Poly a mod (Poly b = 0) = Poly a
                return self

            # very inefficient code below

            # if len(self.data) < degm:
            #     return Poly(self.data, self.m) % self.m
            # m.trim()
            # # lc*x^(degm) + (bx^j + ... + c) = 0 => lc*x^(degm) = -bx^j - ... - c
            # lcm = m.lc()
            #
            # # shift everything except lc to right hand side
            # rhs = m.data[1:]
            #
            # # lc * x ^ (degm) = -bx ^ j - ... - c => x^(degm) -b/lc * x^j - ... - c/lc
            # for i in range(len(rhs)):
            #     rhs[i] = 0 - rhs[i] // lcm
            #
            # # get poly as list
            # data = self.data
            # # get everything to the right of x^(degm) term
            # output = Poly(self.data[-degm + 1:], self.m)
            # # get everything else to get x^(degm) (f*x^(deg-1) + ... + g)
            # rest = data[:-degm + 1]
            #
            # # Create a step poly before the loop and adjust its data instead of creating a new
            # # one each iteration (saves ~0.4 seconds):
            # stepPoly = Poly([0], self.m)
            # # for each term in the rest get product with rhs for substitution
            # for i in range(len(rest)):
            #     step = rhs.copy()
            #     # for each term in rhs
            #     for j in range(len(step)):
            #         # get product
            #         step[j] *= rest[i]
            #     # pad with zeroes to match degree of term
            #     step += [0] * (len(rest) - i - 1)
            #     stepPoly.data = step
            #     # add step to current answer
            #     output += stepPoly
            #
            # # recurse if still not fully reduced
            # if output.deg() >= m.deg():
            #     return output % m
            # # else return with reduced terms
            # return output % self.m

            # end of very inefficient code, pretty efficient code below

            # output the remainder of dividing the polynomial by `m`
            return (self.copy() / m)[1]

    def __lt__(self, other) -> bool:
        """
        < operator for `Poly`s
        :param other: right-hand side polynomial
        :return: `bool` `True` if the polynomial < `other` else `False`
        """
        if type(other) == int:
            # convert `other` to a `Poly` for easy calculation if it is `int`
            other = Poly(other, self.m)
        # output the reverse other > the polynomial
        return other > self

    def __le__(self, other) -> bool:
        """
        <= operator for `Poly`s
        :param other: right-hand side polynomial
        :return: `bool` `True` if the polynomial <= `other` else `False`
        """
        if type(other) == int:
            # convert `other` to a `Poly` for easy calculation if it is `int`
            other = Poly(other, self.m)
        # output the reverse other > the polynomial
        return other >= self

    def __gt__(self, other) -> bool:
        """
        > operator for `Poly`s
        :param other: right-hand side polynomial
        :return: `bool` `True` if the polynomial > `other` else `False`
        """
        if type(other) == int:
            # convert `other` to a `Poly` for easy calculation if it is `int`
            other = Poly(other, self.m)
        # copy the polynomial into `s`
        s = self.copy()
        # take degrees of `s` and `other` once
        deg_s = s.deg()
        deg_o = other.deg()
        if deg_s < deg_o:
            # if the degree of the polynomial is smaller than the degree of `other` it is clearly `False`
            return False
        elif deg_o < deg_s:
            # if the degree of `other` is smaller than the degree of the polynomial it is clearly `True`
            return True
        # subtract `other` taken modulo the modulus of the polynomial from `s`
        s -= other % self.m
        # if the leading coefficient is greater than zero `s` > `other`
        return s.lc() > 0

    def __ge__(self, other) -> bool:
        """
        >= operator for `Poly`s
        :param other: right-hand side polynomial
        :return: `bool` `True` if the polynomial >= `other` else `False`
        """
        if type(other) == int:
            # convert `other` to a `Poly` for easy calculation if it is `int`
            other = Poly(other, self.m)
        # copy the polynomial into `s`
        s = self.copy()
        # take degrees of `s` and `other` once
        deg_s = s.deg()
        deg_o = other.deg()
        if deg_s < deg_o:
            # if the degree of the polynomial is smaller than the degree of `other` it is clearly `False`
            return False
        elif deg_o < deg_s:
            # if the degree of `other` is smaller than the degree of the polynomial it is clearly `True`
            return True
        # subtract `other` taken modulo the modulus of the polynomial from `s`
        s -= other % self.m
        # if the leading coefficient is greater than or equal to zero `s` >= `other`
        return s.lc() >= 0

    def __ne__(self, other) -> bool:
        """
        != operator for `Poly`s
        :param other: right-hand side polynomial
        :return: `bool` `True` if the polynomial == `other` else `False`
        """
        # output the negation of the reverse the polynomial == `other`
        return not self == other

    def __eq__(self, other) -> bool:
        """
        == operator for `Poly`s
        :param other: right-hand side polynomial
        :return: `bool` `True` if the polynomial == `other` else `False`
        """
        if type(other) == int:
            # convert `other` to a `Poly` for easy calculation if it is `int`
            other = Poly(other, self.m)
        # copy the polynomial into `s`
        s = self.copy()
        # subtract `other` taken modulo the modulus of the polynomial from `s`
        s -= other % self.m
        # if the leading coefficient is zero `s` == `other`
        return s.lc() == 0

    def pow(self, n: int):
        """
        pow() or ** operator for `Poly`s using a form of Square and Multiply
        :param n: `int` the power
        :return: `Poly` the polynomial taken power `n`
        """
        # copy the polynomial as `x`
        x = self.copy()
        # z <- 1
        z = Poly(1, self.m)
        # while n > 1
        while n > 1:
            # if n is odd then z <- zx, x <- x^2, n <- floor(n/2)
            # if n is even then x <- x^2, n <- n/2
            if n % 2 == 1:
                z *= x
                n -= 1
            x *= x
            n /= 2
        # output zx
        return z * x

    def poly_mod_eq(self, other, m) -> bool:
        """
        Check if two polynomials are equivalent modulo `m`
        :param other: `Poly` second polynomial
        :param m: `Poly` modulus
        :return: True if the polynomial mod `m` == `other` mod `m`, else False
        """
        return self % m == other % m

    def irreducible(self) -> bool:
        """
        # Check if polynomial is irreducible.
        # Based on algorithm 5.1.4, but with a for-loop to prevent infinite loops
        :return:
        """
        q = self.m
        for t in range(1, self.deg()):
            # t <- 1, calculate while t < n
            if self.gcd(Poly('X^{}-X'.format(q ** t), self.m)) != Poly(1, self.m):
                # t < n
                return False
        # t == n
        return True


def modular_inverse(n: int, m: int, return_poly=False) -> Poly or int:
    """
    Takes the modular inverse of an `int`
    :param n: `int` input number
    :param m: `int` modulus
    :param return_poly: `bool` whether to return an `int` or a `poly`
    :return: `int` or `poly` modular inverse of `n`
    """
    # `n` cannot be zero and the modulus must be positive
    assert (n != 0 and m > 0)

    for i in range(1, m + 1):
        if (i * n) % m == 1:
            # find the `i` for which `i * n`  mod `m` is 1
            if return_poly:
                # return as `Poly` if specified
                return Poly(i, m)
            else:
                # else return as `int`
                return i
    # throw error if no such `i` can be found
    raise AssertionError


def find_irred(m: int, deg: int, give_all=False) -> list or Poly:
    """
    Finds all irreducible polynomials of degree `n` in Z/`m`Z
    :param m: `int` modulus
    :param deg: `int` the degree of the polynomials
    :param give_all: `bool` whether to return all found `Poly`s or a random one
    :return: `list` or `Poly`, the `list` contains all irreducible polynomials and the `Poly` is a random polynomial
    """
    if deg < 0:
        # must enter a valid polynomial degree and the polynomial cannot be zero
        raise ValueError('Degree must 0 or higher')

    # initialize `list` to store any found `Poly`s
    found_polys = []
    # initialize `data` for polynomials as empty list of length `deg + 1`
    data = [0] * (deg + 1)
    for n in range(1, m):
        # for all positive integers `n` < `m`, positive as we else we cannot guarantee the degree is correct
        # set the first coefficient as `n`
        data[0] = n
        # create a `Poly` to manipulate, using `data`
        poly = Poly(data, m)
        # find all irreducible polynomials of degree `deg` with `n` as its leading coefficient, using `find_irred_step`
        found = find_irred_step(poly, deg)
        if len(found) > 0:
            # if any polynomials were found, add them to the list
            found_polys += found
    if len(found_polys) == 0:
        # if no polynomials are found, throw an error
        raise ValueError('No such polynomial exists')

    # the code above may give duplicates, we remove these
    # initialize new `list` to store unique output polynomials
    output_polys = []
    for x in found_polys:
        # loop over all found polynomials
        if x not in output_polys:
            # if it is not yet in the list
            # add it to the list
            output_polys.append(x)
    if give_all:
        # if specified to give all `Poly`s
        # output the entire list
        return output_polys
    # else output a random `Poly`
    return output_polys[randint(0, len(output_polys) - 1)]


def find_irred_step(poly: Poly, d: int) -> list:
    """
    Recursive helper function for `find_irred`
    Bruteforce to find all polynomials matching (X^{deg} + ... + X^d + ... 1)
    :param poly: `Poly` partially filled in polynomial
    :param d: `int` deg - current term
    :return: `list` of found polynomials
    """
    # initialize `list` to store found `Poly`s
    found_polys = []
    if poly.irreducible():
        # check if the current `Poly` is irreducible
        # if it is, add it to the list
        found_polys.append(poly)
    if d == 0:
        # check if on final term, irreducibility check has already been done
        # so we just output the list containing only `poly`
        return found_polys
    for n in range(0, poly.m):
        # loop over all non-negative numbers `n` < `m`
        # get a copy of partially filled in `poly` as `new_poly`
        new_poly = poly.copy()
        # set term `d` to `n`
        new_poly.data[d] = n
        # find all irreducible polynomials starting from this `poly` recursively
        found = find_irred_step(new_poly, d - 1)
        if len(found) > 0:
            # if any were found, add them to the list
            found_polys += found
    # output the list of found irreducible polynomials
    return found_polys
