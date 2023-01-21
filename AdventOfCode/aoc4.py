filename = "input/aoc4_input.txt"
lst = [[]]
with open(filename) as f:
    for f in f.read().splitlines():
        lst[0].append(f.split(","))


def contains_all(lst):
    count = 0
    for i in lst[0]:
        tmp_1 = i[0].split("-")
        tmp_2 = i[1].split("-")

        tmp_1_range = range(int(tmp_1[0]), int(tmp_1[1])+1)
        tmp_2_range = range(int(tmp_2[0]), int(tmp_2[1])+1)

        if int(tmp_1[0]) in tmp_2_range and int(tmp_1[1]) in tmp_2_range:
            count += 1
        elif int(tmp_2[0]) in tmp_1_range and int(tmp_2[1]) in tmp_1_range:
            count += 1
    return count


def overlap_pairs(lst):
    count = 0
    for i in lst[0]:
        tmp_1 = i[0].split("-")
        tmp_2 = i[1].split("-")

        tmp_1_range = range(int(tmp_1[0]), int(tmp_1[1])+1)
        tmp_2_range = range(int(tmp_2[0]), int(tmp_2[1])+1)

        if int(tmp_1[0]) in tmp_2_range or int(tmp_1[1]) in tmp_2_range:
            count += 1
        elif int(tmp_2[0]) in tmp_1_range or int(tmp_2[1]) in tmp_1_range:
            count += 1
    return count


print(contains_all(lst))
print(overlap_pairs(lst))
