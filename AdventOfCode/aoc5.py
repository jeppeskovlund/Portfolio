import copy
import re

filename = "input/aoc5_input.txt"
move_lst = []
from_lst = []
to_lst = []
table = [
    [],
    ['R', 'G', 'J', 'B', 'T', 'V', 'Z'],
    ['J', 'R', 'V', 'L'],
    ['S', 'Q', 'F'],
    ['Z', 'H', 'N', 'L', 'F', 'V', 'Q', 'G'],
    ['R', 'Q', 'T', 'J', 'C', 'S', 'M', 'W'],
    ['S', 'W', 'T', 'C', 'H', 'F'],
    ['D', 'Z', 'C', 'V', 'F', 'N', 'J'],
    ['L', 'G', 'Z', 'D', 'W', 'R', 'F', 'Q'],
    ['J', 'B', 'W', 'V', 'P']
]

with open(filename) as f:
    for f in f.read().splitlines():
        f = re.findall('[0-9]+', f)
        move_lst.append(int(f[0]))
        from_lst.append(int(f[1]))
        to_lst.append(int(f[2]))


def first_problem(move_lst, from_lst, to_lst):
    tables = copy.deepcopy(table)
    for i in range(len(move_lst)):
        for _ in range(move_lst[i]):
            tables[to_lst[i]].append(tables[from_lst[i]][-1])
            if len(tables[from_lst[i]]) != 0:
                tables[from_lst[i]].pop(-1)

    return last_of_list(tables)


def second_problem(move_lst, from_lst, to_lst):
    tables = copy.deepcopy(table)
    for i in range(len(move_lst)):
        tables[to_lst[i]].extend(tables[from_lst[i]][-move_lst[i]:])
        del tables[from_lst[i]][-move_lst[i]:]

    return last_of_list(tables)


def last_of_list(tables):
    tot = ""
    for i in range(1, len(tables)):
        tot += tables[i][-1]
    return tot


print(first_problem(move_lst, from_lst, to_lst))
print(second_problem(move_lst, from_lst, to_lst))
