import json

import asn1tools as asn

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
              .format(answ_q == params['answ-q'] and answ_r == params['answ-r'], answ_q, params['answ-q'], answ_r,
                      params['answ-r']))
        params['answ-q'] = answ_q
        params['answ-q-poly'] = answ_q_poly
        params['answ-r'] = answ_r
        params['answ-r-poly'] = answ_r_poly

    # if operation == 'euclid-poly':
    #     poly = Poly(params['f'], m=params['mod'])
    #     poly2 = Poly(params['g'], m=params['mod'])
    #     own_answer, own_answer_poly = "", [] # str(poly.euclid(poly2)), poly.euclid(poly2).data
    #
    #     print("{} :".format(exercise))
    #     print("Correct: {} - Own answer: [{}] - Correct answer: [{}] || Own answer poly: [{}] - Correct answer poly: [{}]\n"
    #           .format(own_answer == params['answer'] and own_answer_poly == params['answer-poly'], own_answer, params['answer'], own_answer_poly, params['answer-poly']))
    #     params['answer'] = own_answer
    #     params['answer-poly'] = own_answer_poly

    if operation == 'euclid-poly-mod':
        poly = Poly(params['f'], m=params['mod'])
        poly2 = Poly(params['g'], m=params['mod'])
        poly3 = Poly(params['h'], m=params['mod'])
        # TODO change method name
        own_answer, own_answer_poly = str(poly * poly2), (poly * poly2).data

        print("{} :".format(exercise))
        print(
            "Correct: {} - Own answer: [{}] - Correct answer: [{}] || Own answer poly: [{}] - Correct answer poly: [{}]\n"
                .format(own_answer == params['answer'] and own_answer_poly == params['answer-poly'], own_answer,
                        params['answer'], own_answer_poly, params['answer-poly']))
        params['answer'] = own_answer
        params['answer-poly'] = own_answer_poly

    if operation == 'irreducible':
        poly = Poly(params['f'], m=params['mod'])
        own_answer = None  # poly.irreducible()

        print("{} :".format(exercise))
        print("Correct: {} - Own answer: [{}] - Correct answer: [{}]\n"
              .format(own_answer == params['answer'], own_answer, params['answer']))
        params['answer'] = own_answer

    if operation == 'find-irred':
        deg = params['deg']
        own_answer, own_answer_poly = "", []  # str(Poly.find_irreducible(mod, deg)), Poly.find_irreducible(mod, deg).data

        print("{} :".format(exercise))
        print(
            "Correct: {} - Own answer: [{}] - Correct answer: [{}] || Own answer poly: [{}] - Correct answer poly: [{}]\n"
                .format(own_answer == params['answer'] and own_answer_poly == params['answer-poly'], own_answer,
                        params['answer'], own_answer_poly, params['answer-poly']))
        params['answer'] = own_answer
        params['answer-poly'] = own_answer_poly

    if operation == 'add-field':
        params['answer'] = 'X+3'
        params['answer-poly'] = [1, 3]

    if operation == 'add-table':
        params['answer'] = ['X+1', '2X+1']
        params['answer-poly'] = [[1, 1], [2, 1]]

    # Save answer
    my_answers['exercises'].append({operation: params})

# Save exercises with answers to file
my_file = open(base_location + "output.ops", "wb+")  # write to binary file
my_file.write(json.dumps(my_answers).encode())  # add encoded exercise list
my_file.close()
