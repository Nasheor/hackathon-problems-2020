'''
Author: Stephen Driscoll
'''
from penaltyChecker import calculate_penalty
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
    previous_empty_spaces = empty_spaces
    required_options = 1
    while empty_spaces:
        min_options = dimensions

        # Search for suitable numbers in rows
        for x in range(dimensions):
            for test_number in range(dimensions):
                row_options, penalty = [], dimensions
                for y in range(dimensions):
                    if grid[x][y] == "":
                        if penalties[x][y][test_number] < penalty:
                            penalty = penalties[x][y][test_number]
                            row_options = [y]
                        elif penalties[x][y][test_number] == penalty:
                            row_options.append(y)
                if 0 < len(row_options) <= required_options:
                    if penalty == min(penalties[x][row_options[0]]):
                        insert_number(grid, penalties, n, x, row_options[0], (test_number + 1))
                        required_options = 1
                        empty_spaces -= 1
                elif 0 < len(row_options):
                    min_options = min(min_options, len(row_options))

        # Search for suitable numbers in boxes
        for x1 in range(n):
            for y1 in range(n):
                for test_number in range(dimensions):
                    box_options, penalty = [], dimensions
                    for x2 in range(n):
                        for y2 in range(n):
                            x, y = (x1 * n) + x2, (y1 * n) + y2
                            if grid[x][y] == "":
                                if penalties[x][y][test_number] < penalty:
                                    penalty = penalties[x][y][test_number]
                                    box_options = [tuple((x, y))]
                                elif penalties[x][y][test_number] == penalty:
                                    box_options.append(tuple((x, y)))
                    if 0 < len(box_options) <= required_options:
                        if penalty == min(penalties[box_options[0][0]][box_options[0][1]]):
                            insert_number(grid, penalties, n, box_options[0][0], box_options[0][1],
                                          (test_number + 1))
                            required_options = 1
                            empty_spaces -= 1
                    elif 0 < len(box_options):
                        min_options = min(min_options, len(box_options))

        # Search for suitable numbers in columns
        for y in range(dimensions):
            for test_number in range(dimensions):
                col_options, penalty = [], dimensions
                for x in range(dimensions):
                    if grid[x][y] == "":
                        if penalties[x][y][test_number] < penalty:
                            penalty = penalties[x][y][test_number]
                            col_options = [x]
                        elif penalties[x][y][test_number] == penalty:
                            col_options.append(x)
                if 0 < len(col_options) <= required_options:
                    if penalty == min(penalties[col_options[0]][y]):
                        insert_number(grid, penalties, n, col_options[0], y, (test_number + 1))
                        required_options = 1
                        empty_spaces -= 1
                elif 0 < len(col_options):
                    min_options = min(min_options, len(col_options))

        if previous_empty_spaces == empty_spaces:
            required_options = min_options
        else:
            previous_empty_spaces = empty_spaces

    # Done
    print("Penalty " + str(calculate_penalty(n, grid)))
    print('\n'.join([' '.join([str(cell) for cell in row]) for row in grid]))
