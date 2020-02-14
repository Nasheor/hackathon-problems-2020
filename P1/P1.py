"""
Author: Stephen Driscoll
"""
import sys


def insert_number(grid, penalties, n, row, column, number):
    grid[row][column] = number      # Insert number
    penalties[row][column] = 0      # Clear penalties that were associated with that number

    # Update penalty values in rows
    for x in range(dimensions):
        if grid[x][column] == "":
            penalties[x][column][(number - 1)] += 1

    # Update penalty values in box
    top, left = row - (row % n), column - (column % n)
    for boxRow in range(n):
        for boxColumn in range(n):
            if grid[top + boxRow][left + boxColumn] == "":
                penalties[top + boxRow][left + boxColumn][(number - 1)] += 1

    # Update penalty values in columns
    for y in range(dimensions):
        if grid[row][y] == "":
            penalties[row][y][(number - 1)] += 1


if __name__ == "__main__":
    file_text = open(sys.argv[1], 'r')
    line = file_text.readline().split()
    n, k = int(line[0]), int(line[1])
    dimensions = n * n

    # Penalties is a 3D array that keeps track of all potential penalties if we were to add a particular number.
    # After each insertion we update the row, column and box for the value inserted.
    grid = [["" for x in range(dimensions)] for y in range(dimensions)]
    penalties = [[[0 for x in range(dimensions)] for y in range(dimensions)] for i in range(dimensions)]

    for i in range(k):
        line = file_text.readline().split()
        insert_number(grid, penalties, n, (int(line[0]) - 1), (int(line[1]) - 1), int(line[2]))

    # While there are still empty spaces, find and insert the best number next. This is not a backtracking solution.
    empty_spaces = (dimensions * dimensions) - k
    best_x, best_y, best_option, best_num_options, best_possible_num_options = 0, 0, 0, 0, 1
    while empty_spaces:
        best_num_options = (dimensions + 1)
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
                    if best_num_options == best_possible_num_options:
                        break

            if best_num_options == best_possible_num_options:
                break

        best_possible_num_options = best_num_options - 1
        insert_number(grid, penalties, n, best_x, best_y, best_option)
        empty_spaces -= 1

    # Done
    with open(sys.argv[2], 'w') as output:
        output.write('\n'.join([' '.join([str(cell) for cell in row]) for row in grid]))
