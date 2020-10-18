import json

import asn1tools as asn

from Field import Field
from Poly import Poly

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

# Loop over exercises and solve
for exercise in my_exercises['exercises']:
    operation = exercise[0]  # get operation type
    params = exercise[1]  # get parameters

    if operation == 'display-poly':
        poly = Poly(params['f'], m=params['mod'])
        own_answer = str(poly)

        print("{} :".format(exercise))
        print("Correct: {} - Own answer: [{}] - Correct answer: [{}]\n"
              .format(own_answer == params['answer'], own_answer, params['answer']))
        params['answer'] = own_answer

    if operation == 'add-poly':
        poly = Poly(params['f'], m=params['mod'])
        poly2 = Poly(params['g'], m=params['mod'])
        own_answer, own_answer_poly = str(poly + poly2), (poly + poly2).data

        print("{} :".format(exercise))
        print(
            "Correct: {} - Own answer: [{}] - Correct answer: [{}] || Own answer poly: [{}] - Correct answer poly: [{}]\n"
                .format(own_answer == params['answer'] and own_answer_poly == params['answer-poly'], own_answer,
                        params['answer'], own_answer_poly, params['answer-poly']))
        params['answer'] = own_answer
        params['answer-poly'] = own_answer_poly

    if operation == 'subtract-poly':
        poly = Poly(params['f'], m=params['mod'])
        poly2 = Poly(params['g'], m=params['mod'])
        own_answer, own_answer_poly = str(poly - poly2), (poly - poly2).data

        print("{} :".format(exercise))
        print(
            "Correct: {} - Own answer: [{}] - Correct answer: [{}] || Own answer poly: [{}] - Correct answer poly: [{}]\n"
                .format(own_answer == params['answer'] and own_answer_poly == params['answer-poly'], own_answer,
                        params['answer'], own_answer_poly, params['answer-poly']))
        params['answer'] = own_answer
        params['answer-poly'] = own_answer_poly

    if operation == 'multiply-poly':
        poly = Poly(params['f'], m=params['mod'])
        poly2 = Poly(params['g'], m=params['mod'])
        own_answer, own_answer_poly = str(poly * poly2), (poly * poly2).data

        print("{} :".format(exercise))
        print(
            "Correct: {} - Own answer: [{}] - Correct answer: [{}] || Own answer poly: [{}] - Correct answer poly: [{}]\n"
                .format(own_answer == params['answer'] and own_answer_poly == params['answer-poly'], own_answer,
                        params['answer'], own_answer_poly, params['answer-poly']))
        params['answer'] = own_answer
        params['answer-poly'] = own_answer_poly

    if operation == 'long-div-poly':
        poly = Poly(params['f'], m=params['mod'])
        poly2 = Poly(params['g'], m=params['mod'])

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
        params['answ-q'] = answ_q
        params['answ-q-poly'] = answ_q_poly
        params['answ-r'] = answ_r
        params['answ-r-poly'] = answ_r_poly

    if operation == 'euclid-poly':
        poly = Poly(params['f'], m=params['mod'])
        poly2 = Poly(params['g'], m=params['mod'])

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
        print(
            "Correct: {} - Own answer a: [{}] - Correct answer a: [{}] || Own answer b: [{}] - Correct answer b: [{}] || Own answer d: [{}] - Correct answer d: [{}]\n"
            .format(answ_a == params['answ-a'] and answ_a_poly == params['answ-a-poly'] and answ_b == params['answ-b']
                    and answ_b_poly == params['answ-b-poly'] and answ_d == params['answ-d'] and
                    answ_d_poly == params['answ-d-poly'], answ_a, params['answ-a'], answ_b, params['answ-b'], answ_d,
                    params['answ-d']))
        params['answ-a'] = answ_a
        params['answ-a-poly'] = answ_a_poly
        params['answ-b'] = answ_b
        params['answ-b-poly'] = answ_b_poly
        params['answ-d'] = answ_d
        params['answ-d-poly'] = answ_d_poly

    if operation == 'equals-poly-mod':
        poly = Poly(params['f'], m=params['mod'])
        poly2 = Poly(params['g'], m=params['mod'])
        poly3 = Poly(params['h'], m=params['mod'])

        own_answer = poly.poly_mod_eq(poly2, poly3)

        print("{} :".format(exercise))
        print(
            "Correct: {} - Own answer: [{}] - Correct answer: [{}]\n".format(own_answer == params['answer'],
                                                                             own_answer, params['answer']))
        params['answer'] = own_answer

    if operation == 'irreducible':
        poly = Poly(params['f'], m=params['mod'])
        own_answer = poly.irreducible()

        print("{} :".format(exercise))
        print("Correct: {} - Own answer: [{}] - Correct answer: [{}]\n"
              .format(own_answer == params['answer'], own_answer, params['answer']))
        params['answer'] = own_answer

    if operation == 'find-irred':
        deg = params['deg']
        mod = params['mod']
        own_answer, own_answer_poly = str(poly.findIrred(mod, deg)), Poly.findIrred(mod, deg).data

        print("{} :".format(exercise))
        print(
            "Correct: {} - Own answer: [{}] - Correct answer: [{}] || Own answer poly: [{}] - Correct answer poly: [{}]\n"
                .format(own_answer == params['answer'] and own_answer_poly == params['answer-poly'], own_answer,
                        params['answer'], own_answer_poly, params['answer-poly']))
        params['answer'] = own_answer
        params['answer-poly'] = own_answer_poly

    if operation == 'add-field':
        field = Field(params['mod'], params['mod-poly'])
        poly = Poly(params['a'], m=params['mod'])
        poly2 = Poly(params['b'], m=params['mod'])
        own_answer, own_answer_poly = str(field.add(poly, poly2)), (field.add(poly, poly2)).data

        print("{} :".format(exercise))
        print(
            "Correct: {} - Own answer: [{}] - Correct answer: [{}] || Own answer poly: [{}] - Correct answer poly: [{}]\n"
                .format(own_answer == params['answer'] and own_answer_poly == params['answer-poly'], own_answer,
                        params['answer'], own_answer_poly, params['answer-poly']))
        params['answer'] = own_answer
        params['answer-poly'] = own_answer_poly

    if operation == 'subtract-field':
        field = Field(params['mod'], params['mod-poly'])
        poly = Poly(params['a'], m=params['mod'])
        poly2 = Poly(params['b'], m=params['mod'])
        own_answer, own_answer_poly = str(field.subtract(poly, poly2)), (field.subtract(poly, poly2)).data

        print("{} :".format(exercise))
        print(
            "Correct: {} - Own answer: [{}] - Correct answer: [{}] || Own answer poly: [{}] - Correct answer poly: [{}]\n"
                .format(own_answer == params['answer'] and own_answer_poly == params['answer-poly'], own_answer,
                        params['answer'], own_answer_poly, params['answer-poly']))
        params['answer'] = own_answer
        params['answer-poly'] = own_answer_poly
        
    if operation == 'multiply-field':
        field = Field(params['mod'], params['mod-poly'])
        poly = Poly(params['a'], m=params['mod'])
        poly2 = Poly(params['b'], m=params['mod'])
        own_answer, own_answer_poly = str(field.multiply(poly, poly2)), (field.multiply(poly, poly2)).data

        print("{} :".format(exercise))
        print(
            "Correct: {} - Own answer: [{}] - Correct answer: [{}] || Own answer poly: [{}] - Correct answer poly: [{}]\n"
                .format(own_answer == params['answer'] and own_answer_poly == params['answer-poly'], own_answer,
                        params['answer'], own_answer_poly, params['answer-poly']))
        params['answer'] = own_answer
        params['answer-poly'] = own_answer_poly


    if operation == 'inverse-field':
        field = Field(params['mod'], params['mod-poly'])
        poly = Poly(params['a'], m=params['mod'])
        try:
            own_answer, own_answer_poly = str(field.inverse(poly)), (field.inverse(poly)).data
        except AssertionError:
            own_answer, own_answer_poly = "ERROR", []

        print("{} :".format(exercise))
        print(
            "Correct: {} - Own answer: [{}] - Correct answer: [{}] || Own answer poly: [{}] - Correct answer poly: [{}]\n"
                .format(own_answer == params['answer'] and own_answer_poly == params['answer-poly'], own_answer,
                        params['answer'], own_answer_poly, params['answer-poly']))
        params['answer'] = own_answer
        params['answer-poly'] = own_answer_poly

    if operation == 'division-field':
        field = Field(params['mod'], params['mod-poly'])
        poly = Poly(params['a'], m=params['mod'])
        poly2 = Poly(params['b'], m=params['mod'])
        try:
            own_answer, own_answer_poly = str(field.divide(poly, poly2)), (field.divide(poly, poly2)).data
        except AssertionError:
            own_answer, own_answer_poly = "ERROR", []

        print("{} :".format(exercise))
        print(
            "Correct: {} - Own answer: [{}] - Correct answer: [{}] || Own answer poly: [{}] - Correct answer poly: [{}]\n"
                .format(own_answer == params['answer'] and own_answer_poly == params['answer-poly'], own_answer,
                        params['answer'], own_answer_poly, params['answer-poly']))
        params['answer'] = own_answer
        params['answer-poly'] = own_answer_poly

    if operation == 'equals-field':
        field = Field(params['mod'], params['mod-poly'])
        poly = Poly(params['a'], m=params['mod'])
        poly2 = Poly(params['b'], m=params['mod'])
        own_answer = field.equals(poly, poly2)

        print("{} :".format(exercise))
        print(
            "Correct: {} - Own answer: [{}] - Correct answer: [{}]\n"
                .format(own_answer == params['answer'], own_answer,
                        params['answer']))
        params['answer'] = own_answer

    if operation == 'add-table':
        params['answer'] = ['X+1', '2X+1']
        params['answer-poly'] = [[1, 1], [2, 1]]

    # Save answer
    my_answers['exercises'].append({operation: params})

# Save exercises with answers to file
my_file = open(base_location + "output.ops", "wb+")  # write to binary file
my_file.write(json.dumps(my_answers).encode())  # add encoded exercise list
my_file.close()
