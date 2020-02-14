import sys

if __name__ == '__main__':
    lines = int(sys.stdin.readline())
    first_problem = list(map(int, sys.stdin.readline().split()))
    second_problem = list(map(int, sys.stdin.readline().split()))

    bob, alice = 0, 0
    for i in range(3):
        if first_problem[i] < second_problem[i]:
            bob += 1
        elif first_problem[i] == second_problem[i]:
            continue
        else:
            alice += 2
    
    print(alice, " ", bob,"\n")

