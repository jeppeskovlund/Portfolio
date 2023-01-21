filename = "input/aoc6_input.txt"
letters = []
with open(filename) as f:
    for letter in f.read():
        letters.append(letter)


def first_problem(letters):
    lst_letters = letters.copy()
    for count, letter in enumerate(lst_letters):
        if count > 3:
            tmp_lst = lst_letters[count-3:count+1]
            if len(set(tmp_lst)) == 4:
                print(count+1)
                break


def second_problem(lst_letters):
    lst_letters = letters.copy()
    for count, letter in enumerate(lst_letters):
        if count > 13:
            tmp_lst = lst_letters[count-13:count+1]
            if len(set(tmp_lst)) == 14:
                print(count+1)
                break


first_problem(letters)
second_problem(letters)
