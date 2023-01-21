"First december - get the largest calories count for an elf"
elves = []
with open("input/aoc1_input.txt", "r") as file:
    for line in file.readlines():
        elves.append(line.strip())
per_elf = []
elf = 0

for e in elves:
    if str(e) == '':
        per_elf.append(elf)
        elf = 0
    else:
        elf += int(e)
topthree = [0, 0, 0]

for c in per_elf:
    if c > topthree[0] or c > topthree[1] or c > topthree[2]:
        topthree.remove(min(topthree))
        topthree.append(c)

print(sum(topthree))
print(max(per_elf))
