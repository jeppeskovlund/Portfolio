filename = "input/aoc2_input.txt"
lst = []
with open(filename) as f:
    for f in f.read().splitlines():
        lst.append(f)
# ROCK = A X
# PAPER = B Y
# SCISSOR = C Z

count = 0
for x in lst:
    if x[0] == "A":
        if x[2] == "X":
            count += (1+3)
        elif x[2] == "Y":
            count += (2+6)
        elif x[2] == "Z":
            count += 3
    elif x[0] == "B":
        if x[2] == "X":
            count += 1
        elif x[2] == "Y":
            count += (2+3)
        elif x[2] == "Z":
            count += (3+6)
    elif x[0] == "C":
        if x[2] == "X":
            count += (1+6)
        elif x[2] == "Y":
            count += 2
        elif x[2] == "Z":
            count += (3+3)
print(count)
count = 0
# X =lose
# Y = DRaw
# Z = WIN
for x in lst:
    if x[0] == "A":
        if x[2] == "X":
            count += 3
        elif x[2] == "Y":
            count += (1+3)
        elif x[2] == "Z":
            count += (2+6)
    elif x[0] == "B":
        if x[2] == "X":
            count += 1
        elif x[2] == "Y":
            count += (2+3)
        elif x[2] == "Z":
            count += (3+6)
    elif x[0] == "C":
        if x[2] == "X":
            count += 2
        elif x[2] == "Y":
            count += (3+3)
        elif x[2] == "Z":
            count += (1+6)
print(count)
