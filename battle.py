from csp import Constraint, Variable, CSP
from constraints import *
from backtracking import bt_search
import sys
import argparse

my_utorid = 'nagraar3' # Replace with your UtorID!

def print_solution(s, size):
    s_ = {}
    for (var, val) in s:
        s_[int(var.name())] = val
    for i in range(1, size - 1):
        for j in range(1, size - 1):
            # print(s_[-1 - (i * size + j)], end="")
            print(s_[(i * size + j)], end="")
        print('')


def solve_battleship(inputfile: str, outputfile: str):
    '''solves the battleship solitaire puzzle stored in <inputfile> and writes the solution
        to <outputfile>. If there is more than one solution, any will do.'''

    # Read input
    file = open(inputfile, 'r')
    b = file.read()
    b2 = b.split()
    size = len(b2[0])
    size = size + 2
    b3 = []
    b3 += ['0' + b2[0] + '0']
    b3 += ['0' + b2[1] + '0']
    b3 += [b2[2] + ('0' if len(b2[2]) == 3 else '')]
    b3 += ['0' * size]
    for i in range(3, len(b2)):
        b3 += ['0' + b2[i] + '0']
    b3 += ['0' * size]
    board = "\n".join(b3)

    varlist = []
    varn = {}
    conslist = []

    # 1/0 variables
    # Their names are -1, -2, -3, ...
    for i in range(0, size):
        for j in range(0, size):
            v = None
            if i == 0 or i == size - 1 or j == 0 or j == size - 1:
                v = Variable(str(-1 - (i * size + j)), [0])
            else:
                v = Variable(str(-1 - (i * size + j)), [0, 1])
            varlist.append(v)
            varn[str(-1 - (i * size + j))] = v

    # make 1/0 variables match board info
    ii = 0
    for i in board.split()[3:]:
        jj = 0
        for j in i:
            if j != '0' and j != '.':
                conslist.append(TableConstraint('boolean_match', [varn[str(-1 - (ii * size + jj))]], [[1]]))
            elif j == '.':
                conslist.append(TableConstraint('boolean_match', [varn[str(-1 - (ii * size + jj))]], [[0]]))
            jj += 1
        ii += 1


    # ./S/</>/v/^/M variables
    # Their names are 0, 1, 2, ...
    for i in range(0, size):
        for j in range(0, size):
            v = Variable(str(i * size + j), ['.', 'S', '<', '^', 'v', 'M', '>'])
            varlist.append(v)
            varn[str(str(i * size + j))] = v
            # connect 1/0 variables to W/S/L/R/B/T/M variables
            conslist.append(TableConstraint('connect', [varn[str(-1 - (i * size + j))], varn[str(i * size + j)]],
                                            [[0, '.'], [1, 'S'], [1, '<'], [1, '^'], [1, 'v'], [1, 'M'], [1, '>']]))


    # make W/S/L/R/B/T/M variables match board info
    ii = 0
    for i in board.split()[3:]:
        jj = 0
        for j in i:
            if j != '0':
                conslist.append(TableConstraint('value_match', [varn[str(ii * size + jj)]], [[j]]))
            jj += 1
        ii += 1



    # Add more constraints here
    for i in range(1, size - 1):
        for j in range(1, size - 1):
            main_box = varn[str(-1 - (i * size + j))]
            b_left = varn[str((i - 1) * size + j + 1)]
            b_right = varn[str((i + 1) * size + j + 1)]

            conslist.append(
                Diagonal_constraint(
                    f"Diagonal Check",
                    main_box,
                    b_left
                )
            )
            conslist.append(
                Diagonal_constraint(
                    f"Diagonal Check",
                    main_box,
                    b_right
                )
            )



    # find all solutions and check which one has right ship #'s
    csp = CSP('battleship', varlist, conslist)
    solutions, num_nodes = bt_search('BT', csp, 'mrv', True, True)
    sys.stdout = open(outputfile, 'w')
    for i in range(len(solutions)):
        # Check solutions for correct ship numbers here
        print_solution(solutions[i], size)
        print("--------------")

# def get_diag_neighbours():


if __name__ == '__main__':
    # parse board and ships info
    # b = file.read()
    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     "--inputfile",
    #     type=str,
    #     required=True,
    #     help="The input file that contains the puzzles."
    # )
    # parser.add_argument(
    #     "--outputfile",
    #     type=str,
    #     required=True,
    #     help="The output file that contains the solution."
    # )
    # args = parser.parse_args()
    solve_battleship("input_easy1.txt", "out")
