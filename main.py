import json
import random

import asn1tools as asn

from Field import *
from Poly import *

### STUDENT PERSPECTIVE ###

# Below code should behave like a black-box.
# That means that by clicking RUN (and, perhaps, changing the location of the exercise file), your output file should be generated.

base_location = './'
ops_loc = base_location + 'operations.asn'
exs_loc = base_location + 'input.ops'

# Compile specification
spec = asn.compile_files(ops_loc, codec="jer")

# Read exercise list
exercise_file = open(exs_loc, 'rb')  # open binary file
file_data = exercise_file.read()  # read byte array
my_exercises = spec.decode('Exercises', file_data)  # decode after specification
exercise_file.close()  # close file

# Create answer JSON
my_answers = {'exercises': []}


def answer_with_poly(s, p):
    print("Correct: {} - Own answer: [{}] - Correct answer: [{}] || Own answer poly: [{}] - Correct answer poly: [{}]\n"
          .format(s == params['answer'] and p == params['answer-poly'], s, params['answer'], p, params['answer-poly']))

    params['answer'], params['answer-poly'] = s, p


def try_except_with_polys(func):
    try:
        a = func()
        return a
    except (ValueError, AssertionError, ZeroDivisionError, TypeError):
        return "ERROR", []


# Loop over exercises and solve
for exercise in my_exercises['exercises']:
    operation = exercise[0]  # get operation type
    params = exercise[1]  # get parameters

    if operation == 'display-poly':
        print("{} :".format(exercise))

        try:
            poly = Poly(params['f'], params['mod'])

            own_answer = str(poly)
        except (ValueError, AssertionError, ZeroDivisionError, TypeError):
            own_answer = "ERROR"

        print("Correct: {} - Own answer: [{}] - Correct answer: [{}]\n"
              .format(own_answer == params['answer'], own_answer, params['answer']))

        params['answer'] = own_answer

    if operation == 'add-poly':
        print("{} :".format(exercise))

        try:
            poly = Poly(params['f'], params['mod'])
            poly2 = Poly(params['g'], params['mod'])

            own_answer, own_answer_poly = str(poly + poly2), (poly + poly2).data
        except (ValueError, AssertionError, ZeroDivisionError, TypeError):
            own_answer, own_answer_poly = "ERROR", []

        answer_with_poly(own_answer, own_answer_poly)

    if operation == 'subtract-poly':
        print("{} :".format(exercise))

        try:
            poly = Poly(params['f'], params['mod'])
            poly2 = Poly(params['g'], params['mod'])

            own_answer, own_answer_poly = str(poly - poly2), (poly - poly2).data
        except (ValueError, AssertionError, ZeroDivisionError, TypeError):
            own_answer, own_answer_poly = "ERROR", []

        answer_with_poly(own_answer, own_answer_poly)

    if operation == 'multiply-poly':
        print("{} :".format(exercise))

        try:
            poly = Poly(params['f'], params['mod'])
            poly2 = Poly(params['g'], params['mod'])

            own_answer, own_answer_poly = str(poly * poly2), (poly * poly2).data
        except (ValueError, AssertionError, ZeroDivisionError, TypeError):
            own_answer, own_answer_poly = "ERROR", []

        answer_with_poly(own_answer, own_answer_poly)

    if operation == 'long-div-poly':
        print("{} :".format(exercise))

        try:
            poly = Poly(params['f'], params['mod'])
            poly2 = Poly(params['g'], params['mod'])

            ans_q, ans_r = poly / poly2
            answ_q, answ_q_poly = str(ans_q), ans_q.data
            answ_r, answ_r_poly = str(ans_r), ans_r.data
        except (ValueError, AssertionError, ZeroDivisionError, TypeError):
            answ_q, answ_q_poly = "ERROR", []
            answ_r, answ_r_poly = "ERROR", []

        print("Correct: {} - Own answer: [{}] - Correct answer: [{}] || Own answer r: [{}] - Correct answer r: [{}]\n"
              .format(answ_q == params['answ-q'] and answ_q_poly == params['answ-q-poly'] and answ_r ==
                      params['answ-r'] and answ_r_poly == params['answ-r-poly'], answ_q, params['answ-q'], answ_r,
                      params['answ-r']))

        params['answ-q'], params['answ-q-poly'] = answ_q, answ_q_poly
        params['answ-r'], params['answ-r-poly'] = answ_r, answ_r_poly

    if operation == 'euclid-poly':
        print("{} :".format(exercise))

        try:
            poly = Poly(params['f'], params['mod'])
            poly2 = Poly(params['g'], params['mod'])

            ans_a, ans_b, ans_d = poly.euclid(poly2)
            answ_a, answ_a_poly = str(ans_a), ans_a.data
            answ_b, answ_b_poly = str(ans_b), ans_b.data
            answ_d, answ_d_poly = str(ans_d), ans_d.data
        except (ValueError, AssertionError, ZeroDivisionError, TypeError):
            answ_a, answ_a_poly = "ERROR", []
            answ_b, answ_b_poly = "ERROR", []
            answ_d, answ_d_poly = "ERROR", []

        print("Correct: {} - Own answer a: [{}] - Correct answer a: [{}] || Own answer b: [{}] - Correct answer b: "
              "[{}] || Own answer d: [{}] - Correct answer d: [{}]\n"
              .format(answ_a == params['answ-a'] and answ_a_poly == params['answ-a-poly'] and answ_b == params['answ-b']
                      and answ_b_poly == params['answ-b-poly'] and answ_d == params['answ-d'] and
                      answ_d_poly == params['answ-d-poly'], answ_a, params['answ-a'], answ_b, params['answ-b'], answ_d,
                      params['answ-d']))

        params['answ-a'], params['answ-a-poly'] = answ_a, answ_a_poly
        params['answ-b'], params['answ-b-poly'] = answ_b, answ_b_poly
        params['answ-d'], params['answ-d-poly'] = answ_d, answ_d_poly

    if operation == 'equals-poly-mod':
        print("{} :".format(exercise))

        try:
            poly = Poly(params['f'], params['mod'])
            poly2 = Poly(params['g'], params['mod'])
            poly3 = Poly(params['h'], params['mod'])

            own_answer = poly.poly_mod_eq(poly2, poly3)
        except (ValueError, AssertionError, ZeroDivisionError, TypeError):
            own_answer = False

        print("Correct: {} - Own answer: [{}] - Correct answer: [{}]\n".format(own_answer == params['answer'],
                                                                               own_answer, params['answer']))

        params['answer'] = own_answer

    if operation == 'irreducible':
        print("{} :".format(exercise))

        try:
            poly = Poly(params['f'], params['mod'])

            own_answer = poly.irreducible()
        except (ValueError, AssertionError, ZeroDivisionError, TypeError):
            own_answer = False

        print("Correct: {} - Own answer: [{}] - Correct answer: [{}]\n"
              .format(own_answer == params['answer'], own_answer, params['answer']))

        params['answer'] = own_answer

    if operation == 'find-irred':
        print("{} :".format(exercise))

        deg = params['deg']
        mod = params['mod']

        try:
            polys = find_irred(mod, deg, True)
            if len(polys) > 0:
                for x in polys:
                    if params['answer-poly'] == x.data:
                        own_answer, own_answer_poly = str(x), x.data
                        break
                else:
                    # if correct answer is empty or correct answer is not found
                    rand = randint(0, len(polys) - 1)
                    own_answer, own_answer_poly = str(polys[rand]), polys[rand].data
            else:
                own_answer, own_answer_poly = 'ERROR', []
        except (ValueError, AssertionError, ZeroDivisionError, TypeError):
            own_answer, own_answer_poly = "ERROR", []

        answer_with_poly(own_answer, own_answer_poly)

    if operation == 'add-table':
        print("{} :".format(exercise))

        try:
            field = Field(params['mod'], params['mod-poly'])

            own_answer, own_answer_poly = poly_table_pretty(field.add_table()), poly_table(field.add_table())
        except (ValueError, AssertionError, ZeroDivisionError, TypeError):
            own_answer, own_answer_poly = "ERROR", []

        answer_with_poly(own_answer, own_answer_poly)

    if operation == 'mult-table':
        print("{} :".format(exercise))

        try:
            field = Field(params['mod'], params['mod-poly'])

            own_answer, own_answer_poly = poly_table_pretty(field.mult_table()), poly_table(field.mult_table())
        except (ValueError, AssertionError, ZeroDivisionError, TypeError):
            own_answer, own_answer_poly = "ERROR", []

        answer_with_poly(own_answer, own_answer_poly)

    if operation == 'display-field':
        print("{} :".format(exercise))

        try:
            field = Field(params['mod'], params['mod-poly'])
            poly = Poly(params['a'], params['mod'])

            own_answer, own_answer_poly = str(field.display(poly)), field.display(poly).data
        except (ValueError, AssertionError, ZeroDivisionError, TypeError):
            own_answer, own_answer_poly = "ERROR", []

        answer_with_poly(own_answer, own_answer_poly)

    if operation == 'add-field':
        print("{} :".format(exercise))

        try:
            field = Field(params['mod'], params['mod-poly'])
            poly = Poly(params['a'], params['mod'])
            poly2 = Poly(params['b'], params['mod'])

            own_answer, own_answer_poly = str(field.add(poly, poly2)), (field.add(poly, poly2)).data
        except (ValueError, AssertionError, ZeroDivisionError, TypeError):
            own_answer, own_answer_poly = "ERROR", []

        answer_with_poly(own_answer, own_answer_poly)

    if operation == 'subtract-field':
        print("{} :".format(exercise))

        try:
            field = Field(params['mod'], params['mod-poly'])
            poly = Poly(params['a'], params['mod'])
            poly2 = Poly(params['b'], params['mod'])

            own_answer, own_answer_poly = str(field.subtract(poly, poly2)), (field.subtract(poly, poly2)).data
        except (ValueError, AssertionError, ZeroDivisionError, TypeError):
            own_answer, own_answer_poly = "ERROR", []

        answer_with_poly(own_answer, own_answer_poly)

    if operation == 'multiply-field':
        print("{} :".format(exercise))

        try:
            field = Field(params['mod'], params['mod-poly'])
            poly = Poly(params['a'], params['mod'])
            poly2 = Poly(params['b'], params['mod'])

            own_answer, own_answer_poly = str(field.multiply(poly, poly2)), (field.multiply(poly, poly2)).data
        except (ValueError, AssertionError, ZeroDivisionError, TypeError):
            own_answer, own_answer_poly = "ERROR", []

        answer_with_poly(own_answer, own_answer_poly)

    if operation == 'inverse-field':
        print("{} :".format(exercise))

        try:
            field = Field(params['mod'], params['mod-poly'])
            poly = Poly(params['a'], params['mod'])

            own_answer, own_answer_poly = str(field.inverse(poly)), (field.inverse(poly)).data
        except (ValueError, AssertionError, ZeroDivisionError, TypeError):
            own_answer, own_answer_poly = "ERROR", []

        answer_with_poly(own_answer, own_answer_poly)

    if operation == 'division-field':
        print("{} :".format(exercise))

        try:
            field = Field(params['mod'], params['mod-poly'])
            poly = Poly(params['a'], params['mod'])
            poly2 = Poly(params['b'], params['mod'])

            own_answer, own_answer_poly = str(field.divide(poly, poly2)), (field.divide(poly, poly2)).data
        except (ValueError, AssertionError, ZeroDivisionError, TypeError):
            own_answer, own_answer_poly = "ERROR", []

        answer_with_poly(own_answer, own_answer_poly)

    if operation == 'equals-field':
        print("{} :".format(exercise))

        try:
            field = Field(params['mod'], params['mod-poly'])
            poly = Poly(params['a'], params['mod'])
            poly2 = Poly(params['b'], params['mod'])

            own_answer = field.equals(poly, poly2)
        except (ValueError, AssertionError, ZeroDivisionError, TypeError):
            own_answer = False

        print("Correct: {} - Own answer: [{}] - Correct answer: [{}]\n".format(own_answer == params['answer'],
                                                                               own_answer, params['answer']))

        params['answer'] = own_answer

    if operation == 'primitive':
        print("{} :".format(exercise))

        try:
            field = Field(params['mod'], params['mod-poly'])
            poly = Poly(params['a'], params['mod'])

            own_answer = field.is_primitive(poly)
        except (ValueError, AssertionError, ZeroDivisionError, TypeError):
            own_answer = False

        print("Correct: {} - Own answer: [{}] - Correct answer: [{}]\n".format(own_answer == params['answer'],
                                                                               own_answer, params['answer']))

        params['answer'] = own_answer

    if operation == 'find-prim':
        print("{} :".format(exercise))

        try:
            field = Field(params['mod'], params['mod-poly'])

            primitives = field.find_prim(True)
            if len(primitives) > 0:
                for n in primitives:
                    if n.data == params['answer-poly']:
                        own_answer, own_answer_poly = str(n), n.data
                        break
                else:
                    # if correct answer is empty or correct answer is not found
                    rand = random.randint(0, len(primitives) - 1)
                    own_answer, own_answer_poly = str(primitives[rand]), primitives[rand].data
            else:
                own_answer, own_answer_poly = 'ERROR', []
        except (ValueError, AssertionError, ZeroDivisionError, TypeError):
            own_answer, own_answer_poly = "ERROR", []

        answer_with_poly(own_answer, own_answer_poly)

    # Save answer
    my_answers['exercises'].append({operation: params})

# Save answers to file
my_file = open(base_location + "output.ops", "wb+")  # write to binary file
my_file.write(json.dumps(my_answers).encode())  # add encoded exercise list
my_file.close()
