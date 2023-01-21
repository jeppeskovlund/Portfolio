import string
from collections import Counter

filename = "input/aoc3_input.txt"
lst = []
with open(filename) as f:
    for f in f.read().splitlines():
        lst.append(f)

keys = string.ascii_lowercase + string.ascii_uppercase
items = range(0, 52)
points = {keys[i]: items[i]+1 for i in range(len(keys))}


def splitlst(lst):
    count = 0
    for i in lst:
        string_1 = i[slice(0, len(i)//2)]
        string_2 = i[slice(len(i)//2, len(i))]  # splitter hver linje op
        x = check_strings(string_1, string_2)
        count += points[x]
    return count


def check_strings(string_1, string_2):
    dict_1 = Counter(string_1)
    dict_2 = Counter(string_2)

    check_dict = dict_1 & dict_2

    same_char = list(check_dict.elements())
    x = same_char[0]
    return x


def three_elves(lst):
    count = 0
    for i in range(0, len(lst)-2, 3):
        dict_1 = Counter(lst[i])
        dict_2 = Counter(lst[i+1])
        dict_3 = Counter(lst[i+2])
        check_dict = dict_1 & dict_2 & dict_3
        same_char = list(check_dict.elements())
        count += points[same_char[0]]
    return count


print(splitlst(lst))
print(three_elves(lst))
