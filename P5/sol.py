import sys


def read_input():
    line = sys.stdin.readline()
    splits = line.split(' ')

    n = int(splits[0])
    num_lines = int(splits[1])

    lines = list()
    for i in range(num_lines):
        line = sys.stdin.readline()
        lines.append(line)
    return n, lines


def solve(n, lines):
    # Penalties is a 3D array that keeps track of all potential penalties if we were to add a particular number.
    # After each insertion we update the row, column and box for the value inserted.
    dimensions = n * n
    grid = [["" for x in range(dimensions)] for y in range(dimensions)]
    penalties = [[[0 for x in range(dimensions)] for y in range(dimensions)] for i in range(dimensions)]

    for line in lines:
        splits = line.split(' ')
        insert_number(grid, penalties, n, (int(splits[0]) - 1), (int(splits[1]) - 1), int(splits[2]))

    # While there are still empty spaces, find and insert the best number next. This is not a backtracking solution.
    empty_spaces = (dimensions * dimensions) - len(lines)
    while empty_spaces:
        best_x, best_y, best_option, best_num_options = 0, 0, 0, (dimensions + 1)
        for x in range(dimensions):
            for y in range(dimensions):
                if not grid[x][y] == "":
                    continue

                options, penalty = [], dimensions
                for i in range(dimensions):
                    if penalties[x][y][i] < penalty:
                        penalty = penalties[x][y][i]
                        options = [i + 1]
                    elif penalties[x][y][i] == penalty:
                        options.append(i + 1)

                if len(options) < best_num_options:
                    best_x, best_y, best_option, best_num_options = x, y, options[0], len(options)
                    if best_num_options == 1:
                        break
            if best_num_options == 1:
                break

        if not best_num_options == 1:
            return grid

        insert_number(grid, penalties, n, best_x, best_y, best_option)
        empty_spaces -= 1

    return grid


def insert_number(grid, penalties, n, row, column, number):
    dimensions = n * n
    grid[row][column] = number      # Insert number
    penalties[row][column] = 0      # Clear penalties that were associated with that number

    # Update penalty values in rows
    for x in range(dimensions):
        if grid[x][column] == "":
            penalties[x][column][(number - 1)] += 1

    # Update penalty values in columns
    for y in range(dimensions):
        if grid[row][y] == "":
            penalties[row][y][(number - 1)] += 1

    # Update penalty values in box
    top, left = row - (row % n), column - (column % n)
    for boxRow in range(n):
        for boxColumn in range(n):
            if grid[top + boxRow][left + boxColumn] == "":
                penalties[top + boxRow][left + boxColumn][(number - 1)] += 1


def calculate_penalty(n, grid):
    dimensions = n * n
    penalty = 0

    # check rows
    for y in range(dimensions):
        original = set()
        for x in range(dimensions):
            if original.__contains__(grid[x][y]):
                penalty += 1
            else:
                original.add(grid[x][y])

    # check columns
    for x in range(dimensions):
        original = set()
        for y in range(dimensions):
            if original.__contains__(grid[x][y]):
                penalty += 1
            else:
                original.add(grid[x][y])

    # check boxes
    top, left = 0, 0
    while top < dimensions:
        while left < dimensions:
            original = set()
            for x in range(n):
                for y in range(n):
                    if original.__contains__(grid[top + x][left + y]):
                        penalty += 1
                    else:
                        original.add(grid[top + x][left + y])
            left += n
        top += n

    return penalty


def write_output(file_name, grid):
    with open(file_name, 'w') as file_out:
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                file_out.write(str(grid[i][j]) + " ")
            file_out.write("\n")


def main():
    n, lines = read_input()

    grid = solve(n, lines)

    # print("Penalty: " + str(calculate_penalty(n, grid)))

    for x in range(n * n):
        line = ""
        for y in range(n * n):
            line += str(grid[x][y]) + " "
        print(line)
    # print("Penalty: " + str(calculate_penalty(n, grid)))


if __name__ == "__main__":
    main()
