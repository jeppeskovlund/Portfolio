file = "input/aoc8_input.txt"
tree_lines = []
with open(file) as f:
    for index, char in enumerate(f.read().splitlines()):
        tree_lines.append([])
        for i in char:
            tree_lines[index].append(i.strip())


def left(index, tree, tree_line):
    for t in tree_line[:index]:
        if t >= tree:
            return False
    return True


def right(index, tree, tree_line):
    for t in tree_line[index+1:]:
        if t >= tree:
            return False
    return True


def up(index, ind, tree, tree_lines):
    for t in range(ind-1, -1, -1):
        #print('UP HER:', tree_lines[t][index])
        if tree_lines[t][index] >= tree:
            return False
    return True


def down(index, ind, tree, tree_lines):
    for t in range(ind+1, len(tree_lines)):
        if tree_lines[t][index] >= tree:
            return False
    return True


def left_count(index, tree, tree_line):
    count = 0
    for t in reversed(tree_line[:index]):
        if t >= tree:
            count += 1
            return count
        else:
            count += 1
    return count


def right_count(index, tree, tree_line):
    count = 0
    for t in tree_line[index+1:]:
        if t >= tree:
            count += 1
            return count
        else:
            count += 1
    return count


def up_count(index, ind, tree, tree_lines):
    count = 0
    for t in range(ind-1, -1, -1):
        if tree_lines[t][index] >= tree:
            count += 1
            return count
        else:
            count += 1
    return count


def down_count(index, ind, tree, tree_lines):
    count = 0
    for t in range(ind+1, len(tree_lines)):
        if tree_lines[t][index] >= tree:
            count += 1
            return count
        else:
            count += 1
    return count


def check_ways(tree_lines):
    count = 0
    for ind, tree_l in enumerate(tree_lines):
        for index, tree in enumerate(tree_l):
            if left(index, tree, tree_lines[ind]) or right(index, tree, tree_lines[ind]) or up(index, ind, tree, tree_lines) or down(index, ind, tree, tree_lines):
                count += 1
    return print(count)


def check_ways_second(tree_lines):
    highest = 0
    for ind, tree_l in enumerate(tree_lines):
        for index, tree in enumerate(tree_l):
            score = left_count(index, tree, tree_lines[ind]) * right_count(index, tree, tree_lines[ind]) * up_count(
                index, ind, tree, tree_lines) * down_count(index, ind, tree, tree_lines)
            if score > highest:
                highest = score
    return print(highest)


check_ways(tree_lines)
check_ways_second(tree_lines)
