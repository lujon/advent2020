import fileinput

rows = [line for line in fileinput.input("input.txt")]

row_length = len(rows[0]) - 1


def count_trees(x_step, y_step):
    x = x_step
    y = y_step

    tree_count = 0

    while y < len(rows):
        if rows[y][x] == "#":
            tree_count += 1
        x = (x + x_step) % row_length
        y += y_step

    return tree_count


# Part 1
print(count_trees(3, 1))

# Part 2
print(count_trees(1, 1)
      * count_trees(3, 1)
      * count_trees(5, 1)
      * count_trees(7, 1)
      * count_trees(1, 2))
