from csp import Constraint, Variable, CSP
from constraints import *
from backtracking import bt_search
import sys
import argparse

my_utorid = ""


def print_solution(s, size):
    s_ = {}
    for (var, val) in s:
        s_[int(var.name())] = val
    for i in range(1, size - 1):
        for j in range(1, size - 1):
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

    for i in range(0, size):
        for j in range(0, size):
            v = Variable(str(i * size + j), ['.', 'S', '<', '^', 'v', 'M', '>'])
            if j == 0 or j == size - 1 or i == 0 or i == size - 1:
                v.resetDomain(['.'])
            varlist.append(v)
            varn[str(i * size + j)] = v

    ii = 0
    for i in board.split()[3:]:
        jj = 0
        for j in i:
            if j != '0':
                conslist.append(
                    TableConstraint(
                        'value_match',
                        [varn[str(ii * size + jj)]],
                        [[j]]
                    )
                )
            jj += 1
        ii += 1

    # Add more constraints here

    row_num = []
    for vv in b2[0]:
        vv = int(vv)
        row_num.append(vv)

    col_num = []
    for cc in b2[1]:
        cc = int(cc)
        col_num.append(cc)

    # Row
    for i in range(1, size - 1):
        row_vars = []
        for j in range(1, size - 1):
            row_vars.append(varn[str(i * size + j)])

        conslist.append(
            NValuesConstraint(
                f'row_constraint_{i}',
                row_vars,
                ['S', '<', '>', '^', 'v', 'M'],
                row_num[i - 1],
                row_num[i - 1]
            )
        )

    # Column
    for j in range(1, size - 1):
        col_vars = []
        for i in range(1, size - 1):
            col_vars.append(varn[str(i * size + j)])

        conslist.append(
            NValuesConstraint(
                f'col_constraint_{j}',
                col_vars,
                ['S', '<', '>', '^', 'v', 'M'],
                col_num[j - 1],
                col_num[j - 1]
            )
        )

    # Diagonal\Orthogonal Constraint
    for i in range(1, size - 1):
        for j in range(1, size - 1):

            main_box = varn[str(i * size + j)]

            neighbors = {
                "up": varn[str((i - 1) * size + j)],
                "down": varn[str((i + 1) * size + j)],
                "left": varn[str(i * size + (j - 1))],
                "right": varn[str(i * size + (j + 1))]
            }

            diag_positions = [
                (i - 1, j - 1),
                (i - 1, j + 1),
                (i + 1, j - 1),
                (i + 1, j + 1)
            ]

            for (di, dj) in diag_positions:
                diag_var = varn[str(di * size + dj)]
                diagonal_table = []

                for v_main in main_box.domain():
                    for v_diag in diag_var.domain():

                        if v_main == "." or v_diag == ".":
                            diagonal_table.append([v_main, v_diag])

                conslist.append(
                    TableConstraint(
                        f"diag_{i}_{j}_{di}_{dj}",
                        [main_box, diag_var],
                        diagonal_table
                    )
                )
            ordered_vars = [
                main_box,
                neighbors["up"],
                neighbors["down"],
                neighbors["left"],
                neighbors["right"]
            ]

            domain_lists = []
            for var in ordered_vars:
                domain_lists.append(var.domain())

            all_tuples = [[]]
            for domain in domain_lists:
                next_level = []
                for partial in all_tuples:
                    for value in domain:
                        next_level.append(partial + [value])
                all_tuples = next_level

            allowed_tuples = []

            for t in all_tuples:
                curr, up, down, left, right = t
                bool_check = False

                if curr == '.':
                    bool_check = True

                elif curr == 'S':
                    if up == '.' and down == '.' and left == '.' and right == '.':
                        bool_check = True

                elif curr == '<':
                    if left == '.' and up == '.' and down == '.' and right in ('M', '>'):
                        bool_check = True

                elif curr == '>':
                    if right == '.' and up == '.' and down == '.' and left in ('M', '<'):
                        bool_check = True

                elif curr == '^':
                    if up == '.' and left == '.' and right == '.' and down in ('M', 'v'):
                        bool_check = True

                elif curr == 'v':
                    if down == '.' and left == '.' and right == '.' and up in ('M', '^'):
                        bool_check = True

                elif curr == 'M':
                    horiz = (
                            up == '.' and down == '.' and
                            left in ('<', 'M') and right in ('>', 'M')
                    )
                    vert = (
                            left == '.' and right == '.' and
                            up in ('^', 'M') and down in ('v', 'M')
                    )
                    if horiz or vert:
                        bool_check = True

                if bool_check:
                    allowed_tuples.append(t)

            conslist.append(
                TableConstraint(
                    f"cell_{i}_{j}",
                    ordered_vars,
                    allowed_tuples
                )
            )

    csp = CSP('battleship', varlist, conslist)
    solutions, num_nodes = bt_search('GAC', csp, 'mrv', True, False)

    sys.stdout = open(outputfile, 'w')
    for i in range(len(solutions)):
        solution = solutions[i]

        grid = {}
        for (var, val) in solution:
            grid[int(var.name())] = val

        s = 0
        des = 0
        cruz = 0
        batship = 0

        for r in range(1, size - 1):
            for c in range(1, size - 1):
                if grid[r * size + c] == 'S':
                    s += 1

        for c in range(1, size - 1):
            r = 1
            while r < size - 1:
                if grid[r * size + c] == '^':
                    length = 1
                    r2 = r + 1
                    end_found = False
                    while r2 < size - 1 and not end_found:
                        cell = grid[r2 * size + c]
                        if cell in ('M', 'v'):
                            length += 1
                            if cell == 'v':
                                end_found = True
                        else:
                            end_found = True
                        r2 += 1

                    if length == 2:
                        des += 1
                    elif length == 3:
                        cruz += 1
                    elif length == 4:
                        batship += 1
                    r = r2
                else:
                    r += 1

        # Count horizontal ships
        for r in range(1, size - 1):
            c = 1
            while c < size - 1:
                if grid[r * size + c] == '<':
                    length = 1
                    c2 = c + 1
                    end_found = False
                    while c2 < size - 1 and not end_found:
                        cell = grid[r * size + c2]
                        if cell in ('M', '>'):
                            length += 1
                            if cell == '>':
                                end_found = True
                        else:
                            end_found = True
                        c2 += 1

                    if length == 2:
                        des += 1
                    elif length == 3:
                        cruz += 1
                    elif length == 4:
                        batship += 1
                    c = c2
                else:
                    c += 1

        if (s == int(b2[2][0]) and
                des == int(b2[2][1]) and
                cruz == int(b2[2][2]) and
                batship == int(b2[2][3])):
            print_solution(solution, size)
            print("--------------")


if __name__ == '__main__':
    # parse board and ships info
    # file = open(sys.argv[1], 'r')
    # b = file.read()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzles."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    args = parser.parse_args()
    solve_battleship(args.inputfile, args.outputfile)
