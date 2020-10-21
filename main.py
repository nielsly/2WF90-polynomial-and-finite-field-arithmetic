import json

import asn1tools as asn

from Field import *
from Poly import *

### STUDENT PERSPECTIVE (example) ###

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

known_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

# Loop over exercises and solve
for exercise in my_exercises['exercises']:
    operation = exercise[0]  # get operation type
    params = exercise[1]  # get parameters

    # Simple prime check for the modulo. We use a pre-generated list of primes, since we know p < 100:
    # Also check if the mod poly is irreducible in case of a field operation
    if params['mod'] not in known_primes or (
            'mod-poly' in params and not Poly(params['mod-poly'], params['mod']).irreducible()):
        if operation in ['equals-poly-mod', 'irreducible', 'equals-field', 'primitive']:
            params['my_answer'] = False
        elif operation == 'display_poly':
            params['my_answer'] = "ERROR"
        elif operation == 'long-div-poly':
            params['answ-q'], params['answ-q-poly'] = "ERROR", []
            params['answ-r'], params['answ-r-poly'] = "ERROR", []
        elif operation == "euclid-poly":
            params['answ-a'], params['answ-a-poly'] = "ERROR", []
            params['answ-b'], params['answ-b-poly'] = "ERROR", []
            params['answ-d'], params['answ-d-poly'] = "ERROR", []
        else:
            params['answer'], params['answer-poly'] = "ERROR", []

        print("Caught invalid argument(s) for {} \n".format(exercise))
        my_answers['exercises'].append({operation: params})
        continue

    if operation == 'display-poly':
        poly = Poly(params['f'], params['mod'])
        own_answer = str(poly)

        print("{} :".format(exercise))
        print("Correct: {} - Own answer: [{}] - Correct answer: [{}]\n"
              .format(own_answer == params['answer'], own_answer, params['answer']))

        params['answer'] = own_answer

    if operation == 'add-poly':
        poly = Poly(params['f'], params['mod'])
        poly2 = Poly(params['g'], params['mod'])
        own_answer, own_answer_poly = str(poly + poly2), (poly + poly2).data

        print("{} :".format(exercise))
        print("Correct: {} - Own answer: [{}] - Correct answer: [{}] || Own answer poly: [{}] - Correct answer poly: "
              "[{}]\n".format(own_answer == params['answer'] and own_answer_poly == params['answer-poly'], own_answer,
                              params['answer'], own_answer_poly, params['answer-poly']))

        params['answer'], params['answer-poly'] = own_answer, own_answer_poly

    if operation == 'subtract-poly':
        poly = Poly(params['f'], params['mod'])
        poly2 = Poly(params['g'], params['mod'])
        own_answer, own_answer_poly = str(poly - poly2), (poly - poly2).data

        print("{} :".format(exercise))
        print("Correct: {} - Own answer: [{}] - Correct answer: [{}] || Own answer poly: [{}] - Correct answer poly: "
              "[{}]\n".format(own_answer == params['answer'] and own_answer_poly == params['answer-poly'], own_answer,
                              params['answer'], own_answer_poly, params['answer-poly']))

        params['answer'], params['answer-poly'] = own_answer, own_answer_poly

    if operation == 'multiply-poly':
        poly = Poly(params['f'], params['mod'])
        poly2 = Poly(params['g'], params['mod'])
        own_answer, own_answer_poly = str(poly * poly2), (poly * poly2).data

        print("{} :".format(exercise))
        print("Correct: {} - Own answer: [{}] - Correct answer: [{}] || Own answer poly: [{}] - Correct answer poly: "
              "[{}]\n".format(own_answer == params['answer'] and own_answer_poly == params['answer-poly'], own_answer,
                              params['answer'], own_answer_poly, params['answer-poly']))

        params['answer'], params['answer-poly'] = own_answer, own_answer_poly

    if operation == 'long-div-poly':
        poly = Poly(params['f'], params['mod'])
        poly2 = Poly(params['g'], params['mod'])

        try:
            ans_q, ans_r = poly / poly2
            answ_q, answ_q_poly = str(ans_q), ans_q.data
            answ_r, answ_r_poly = str(ans_r), ans_r.data
        except AssertionError:
            answ_q, answ_q_poly = "ERROR", []
            answ_r, answ_r_poly = "ERROR", []

        print("{} :".format(exercise))
        print("Correct: {} - Own answer: [{}] - Correct answer: [{}] || Own answer r: [{}] - Correct answer r: [{}]\n"
              .format(answ_q == params['answ-q'] and answ_q_poly == params['answ-q-poly'] and answ_r ==
                      params['answ-r'] and answ_r_poly == params['answ-r-poly'], answ_q, params['answ-q'], answ_r,
                      params['answ-r']))

        params['answ-q'], params['answ-q-poly'] = answ_q, answ_q_poly
        params['answ-r'], params['answ-r-poly'] = answ_r, answ_r_poly

    if operation == 'euclid-poly':
        poly = Poly(params['f'], params['mod'])
        poly2 = Poly(params['g'], params['mod'])

        try:
            ans_a, ans_b, ans_d = poly.euclid(poly2)
            answ_a, answ_a_poly = str(ans_a), ans_a.data
            answ_b, answ_b_poly = str(ans_b), ans_b.data
            answ_d, answ_d_poly = str(ans_d), ans_d.data
        except AssertionError:
            answ_a, answ_a_poly = "ERROR", []
            answ_b, answ_b_poly = "ERROR", []
            answ_d, answ_d_poly = "ERROR", []

        print("{} :".format(exercise))
        print("Correct: {} - Own answer a: [{}] - Correct answer a: [{}] || Own answer b: [{}] - Correct answer b: "
              "[{}] || Own answer d: [{}] - Correct answer d: [{}]\n"
              .format(answ_a == params['answ-a'] and answ_a_poly == params['answ-a-poly'] and answ_b == params['answ-b']
                      and answ_b_poly == params['answ-b-poly'] and answ_d == params['answ-d'] and
                      answ_d_poly == params['answ-d-poly'], answ_a, params['answ-a'], answ_b, params['answ-b'], answ_d,
                      params['answ-d']))

        params['answ-a'], params['answ-a-poly'] = answ_a, answ_a_poly
        params['answ-b'], params['answ-b-poly'] = answ_b, answ_b_poly
        params['answ-d'], params['answ-d-poly']= answ_d, answ_d_poly

    if operation == 'equals-poly-mod':
        poly = Poly(params['f'], params['mod'])
        poly2 = Poly(params['g'], params['mod'])
        poly3 = Poly(params['h'], params['mod'])

        own_answer = poly.poly_mod_eq(poly2, poly3)

        print("{} :".format(exercise))
        print("Correct: {} - Own answer: [{}] - Correct answer: [{}]\n".format(own_answer == params['answer'],
                                                                               own_answer, params['answer']))

        params['answer'] = own_answer

    if operation == 'irreducible':
        poly = Poly(params['f'], params['mod'])
        own_answer = poly.irreducible()

        print("{} :".format(exercise))
        print("Correct: {} - Own answer: [{}] - Correct answer: [{}]\n"
              .format(own_answer == params['answer'], own_answer, params['answer']))

        params['answer'] = own_answer

    if operation == 'find-irred':
        deg = params['deg']
        mod = params['mod']

        polys = find_irred(mod, deg)
        if len(polys) > 0:
            own_answer, own_answer_poly = polys[0], polys[0].data
            for x in polys:
                if params['answer-poly'] == x.data:
                    own_answer, own_answer_poly = str(x), x.data
                    break
            else:
                # Not sure whether the real test will already have the answers in the input file, so if we cant
                # find a match, just return the first one as they all should be irreducible anyways.
                own_answer, own_answer_poly = str(polys[0]), polys[0].data
        else:
            own_answer, own_answer_poly = 'ERROR', []

        print("{} :".format(exercise))
        print("Correct: {} - Own answer: [{}] - Correct answer: [{}] || Own answer poly: [{}] - Correct answer poly: "
              "[{}]\n".format(own_answer == params['answer'] and own_answer_poly == params['answer-poly'], own_answer,
                              params['answer'], own_answer_poly, params['answer-poly']))

        params['answer'], params['answer-poly'] = own_answer, own_answer_poly

    if operation == 'add-table':
        field = Field(params['mod'], params['mod-poly'])
        own_answer, own_answer_poly = poly_table_pretty(field.add_table()), poly_table(field.add_table())

        print("{} :".format(exercise))
        print("Correct: {} - Own answer: [{}] - Correct answer: [{}] || Own answer poly: [{}] - Correct answer poly: "
              "[{}]\n".format(own_answer == params['answer'] and own_answer_poly == params['answer-poly'], own_answer,
                              params['answer'], own_answer_poly, params['answer-poly']))

        params['answer'], params['answer-poly'] = own_answer, own_answer_poly

    if operation == 'mult-table':
        field = Field(params['mod'], params['mod-poly'])
        own_answer, own_answer_poly = poly_table_pretty(field.mult_table()), poly_table(field.mult_table())

        print("{} :".format(exercise))
        print("Correct: {} - Own answer: [{}] - Correct answer: [{}] || Own answer poly: [{}] - Correct answer poly: "
              "[{}]\n".format(own_answer == params['answer'] and own_answer_poly == params['answer-poly'], own_answer,
                              params['answer'], own_answer_poly, params['answer-poly']))

        params['answer'], params['answer-poly'] = own_answer, own_answer_poly

    if operation == 'display-field':
        field = Field(params['mod'], params['mod-poly'])
        poly = Poly(params['a'], params['mod'])
        own_answer, own_answer_poly = str(field.display(poly)), field.display(poly).data

        print("{} :".format(exercise))
        print("Correct: {} - Own answer: [{}] - Correct answer: [{}] || Own answer poly: [{}] - Correct answer poly: "
              "[{}]\n".format(own_answer == params['answer'] and own_answer_poly == params['answer-poly'], own_answer,
                              params['answer'], own_answer_poly, params['answer-poly']))

        params['answer'], params['answer-poly'] = own_answer, own_answer_poly

    if operation == 'add-field':
        field = Field(params['mod'], params['mod-poly'])
        poly = Poly(params['a'], params['mod'])
        poly2 = Poly(params['b'], params['mod'])
        own_answer, own_answer_poly = str(field.add(poly, poly2)), (field.add(poly, poly2)).data

        print("{} :".format(exercise))
        print("Correct: {} - Own answer: [{}] - Correct answer: [{}] || Own answer poly: [{}] - Correct answer poly: "
              "[{}]\n".format(own_answer == params['answer'] and own_answer_poly == params['answer-poly'], own_answer,
                              params['answer'], own_answer_poly, params['answer-poly']))

        params['answer'], params['answer-poly'] = own_answer, own_answer_poly

    if operation == 'subtract-field':
        field = Field(params['mod'], params['mod-poly'])
        poly = Poly(params['a'], params['mod'])
        poly2 = Poly(params['b'], params['mod'])
        own_answer, own_answer_poly = str(field.subtract(poly, poly2)), (field.subtract(poly, poly2)).data

        print("{} :".format(exercise))
        print("Correct: {} - Own answer: [{}] - Correct answer: [{}] || Own answer poly: [{}] - Correct answer poly: "
              "[{}]\n".format(own_answer == params['answer'] and own_answer_poly == params['answer-poly'], own_answer,
                              params['answer'], own_answer_poly, params['answer-poly']))

        params['answer'], params['answer-poly'] = own_answer, own_answer_poly
        
    if operation == 'multiply-field':
        field = Field(params['mod'], params['mod-poly'])
        poly = Poly(params['a'], params['mod'])
        poly2 = Poly(params['b'], params['mod'])
        own_answer, own_answer_poly = str(field.multiply(poly, poly2)), (field.multiply(poly, poly2)).data

        print("{} :".format(exercise))
        print(
            "Correct: {} - Own answer: [{}] - Correct answer: [{}] || Own answer poly: [{}] - Correct answer poly: "
            "[{}]\n".format(own_answer == params['answer'] and own_answer_poly == params['answer-poly'], own_answer,
                            params['answer'], own_answer_poly, params['answer-poly']))

        params['answer'], params['answer-poly'] = own_answer, own_answer_poly

    if operation == 'inverse-field':
        field = Field(params['mod'], params['mod-poly'])
        poly = Poly(params['a'], params['mod'])
        try:
            own_answer, own_answer_poly = str(field.inverse(poly)), (field.inverse(poly)).data
        except AssertionError:
            own_answer, own_answer_poly = "ERROR", []

        print("{} :".format(exercise))
        print("Correct: {} - Own answer: [{}] - Correct answer: [{}] || Own answer poly: [{}] - Correct answer poly: "
              "[{}]\n".format(own_answer == params['answer'] and own_answer_poly == params['answer-poly'], own_answer,
                              params['answer'], own_answer_poly, params['answer-poly']))

        params['answer'], params['answer-poly'] = own_answer, own_answer_poly

    if operation == 'division-field':
        field = Field(params['mod'], params['mod-poly'])
        poly = Poly(params['a'], params['mod'])
        poly2 = Poly(params['b'], params['mod'])
        try:
            own_answer, own_answer_poly = str(field.divide(poly, poly2)), (field.divide(poly, poly2)).data
        except AssertionError:
            own_answer, own_answer_poly = "ERROR", []

        print("{} :".format(exercise))
        print("Correct: {} - Own answer: [{}] - Correct answer: [{}] || Own answer poly: [{}] - Correct answer poly: "
              "[{}]\n".format(own_answer == params['answer'] and own_answer_poly == params['answer-poly'], own_answer,
                              params['answer'], own_answer_poly, params['answer-poly']))

        params['answer'], params['answer-poly'] = own_answer, own_answer_poly

    if operation == 'equals-field':
        field = Field(params['mod'], params['mod-poly'])
        poly = Poly(params['a'], params['mod'])
        poly2 = Poly(params['b'], params['mod'])
        own_answer = field.equals(poly, poly2)

        print("{} :".format(exercise))
        print("Correct: {} - Own answer: [{}] - Correct answer: [{}]\n".format(own_answer == params['answer'],
                                                                               own_answer, params['answer']))

        params['answer'] = own_answer

    if operation == 'primitive':
        field = Field(params['mod'], params['mod-poly'])
        poly = Poly(params['a'], params['mod'])
        own_answer = field.is_primitive(poly)

        print("{} :".format(exercise))
        print(
            "Correct: {} - Own answer: [{}] - Correct answer: [{}]\n"
                .format(own_answer == params['answer'], own_answer,
                        params['answer']))

        params['answer'] = own_answer

    if operation == 'find-prim':
        field = Field(params['mod'], params['mod-poly'])
        try:
            primitives = field.find_prim()

            if len(primitives) > 0:
                for n in primitives:
                    if n.data == params['answer-poly']:
                        own_answer, own_answer_poly = str(n), n.data
                        break
                else:
                    # Not sure whether the real test will already have the answers in the input file, so if we cant
                    # find a match, just return the first one as they all should be primitive elements anyways.
                    own_answer, own_answer_poly = str(primitives[0]), primitives[0].data
            else:
                own_answer, own_answer_poly = 'ERROR', []
        except AssertionError:
            own_answer, own_answer_poly = 'ERROR', []

        print("{} :".format(exercise))
        print("Correct: {} - Own answer: [{}] - Correct answer: [{}] || Own answer poly: [{}] - Correct answer poly: "
              "[{}]\n".format(own_answer == params['answer'] and own_answer_poly == params['answer-poly'], own_answer,
                              params['answer'], own_answer_poly, params['answer-poly']))

        params['answer'], params['answer-poly'] = own_answer, own_answer_poly

    # Save answer
    my_answers['exercises'].append({operation: params})

# Save exercises with answers to file
my_file = open(base_location + "output.ops", "wb+")  # write to binary file
my_file.write(json.dumps(my_answers).encode())  # add encoded exercise list
my_file.close()
