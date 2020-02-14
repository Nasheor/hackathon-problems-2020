'''
Author: Stephen Driscoll
'''


def read_input():
    discard = input()
    num_tests = int(input())

    grids = list()
    patterns = list()
    for i in range(num_tests):
        grids.append(read_grid())
        patterns.append(read_grid())

    return grids, patterns


def read_grid():
    line = input()
    splits = line.split(' ')
    rows = int(splits[0])
    columns = int(splits[1])

    grid = list()
    for i in range(rows):
        grid.append(list())
        line = input()
        for j in range(columns):
            grid[i].append(line[j])

    return grid


def solve(larger, pattern):
    for a in range(len(larger)):
        for b in range(len(larger[0])):
            found = True
            for c in range(len(pattern)):
                for d in range(len(pattern[0])):
                    if len(larger) <= (a + c) or len(larger[0]) <= (b + d) or larger[a + c][b + d] != pattern[c][d]:
                        found = False
                        break
                if not found:
                    break
            if found:
                return True

    return False


def write_output(results):
    for i in range(len(results)):
        if results[i]:
            print("YES")
        else:
            print("NO")


def main():
    grids, patterns = read_input()

    results = list()
    for i in range(len(patterns)):
        results.append(solve(grids[i], patterns[i]))

    write_output(results)


if __name__ == "__main__":
    main()
