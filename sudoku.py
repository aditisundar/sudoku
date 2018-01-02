from math import *
from timeit import default_timer
from itertools import *


num = 9
rows = "ABCDEFGHI"
cols = "123456789"

def prepare(str):
    array = {}
    i=0
    for r in range(num):
        for c in range(num):
            key = ""+ rows[r]+cols[c]
            if str[i] != '.' and str[i] != '0':
                array[key] = str[i]
            else:
                array[key] = "123456789"
            i+=1
    return array
def disp_sud(puzzle):
    for s in sorted(puzzle.keys()):
        if s[1] == "1": print()
        if len(puzzle[s])==1:
            print(puzzle[s], end = " ")
        else:
            print(".", end = " ")
    print()
def disp_pos(puzzle):
    for s in sorted(puzzle.keys()):
        if s[1] == "1": print()
        print(puzzle[s], end = "\t")
    print()
def row(puzzle, str):
    row_array = []
    n = rows.index(str[0])
    return [rows[n]+cols[i] for i in range(9)]
def column(puzzle, str):
    col_array = []
    n = cols.index(str[1])
    return [rows[i]+cols[n] for i in range(9)]
def box(puzzle, str): #returns an array of keys based on which quadrant r,c is located
    r = str[0]
    c = str[1]
    grid = []
    final = []
    if rows.index(r)<3 and cols.index(c)<3: #1
        grid = [[r+c] for r in "ABC" for c in "123"]
    elif rows.index(r)<3 and cols.index(c)<6: #2
        grid = [[r+c] for r in "ABC" for c in "456"]
    elif rows.index(r)<3 and cols.index(c)<9: #3
        grid = [[r+c] for r in "ABC" for c in "789"]
    elif rows.index(r)<6 and cols.index(c)<3: #4
        grid = [[r+c] for r in "DEF" for c in "123"]
    elif rows.index(r)<6 and cols.index(c)<6: #5
        grid = [[r+c] for r in "DEF" for c in "456"]
    elif rows.index(r)<6 and cols.index(c)<9: #6
        grid = [[r+c] for r in "DEF" for c in "789"]
    elif rows.index(r)<9 and cols.index(c)<3: #7
        grid = [[r+c] for r in "GHI" for c in "123"]
    elif rows.index(r)<9 and cols.index(c)<6: #8
        grid = [[r+c] for r in "GHI" for c in "456"]
    elif rows.index(r)<9 and cols.index(c)<9: #9
        grid = [[r+c] for r in "GHI" for c in "789"]
    for a in grid:
        final += a
    return final
def unit(puzzle, str):
    return row(puzzle,str)+column(puzzle,str)+box(puzzle,str)
def solved(puzzle): #if the puzzle contains one or more zeros, returns false
    if not puzzle: return False
    for a in puzzle:
        if len(puzzle[a]) != 1:
            return False
    return True


def eliminate(puzzle):
    prev = [] #new
    while puzzle != prev: #new
        prev = puzzle.copy() #new
        for g in puzzle:

            if puzzle[g] == "":
                return False
            u = unit(puzzle,g) #list of locations in this square's unit (A1, A2...)
            if len(puzzle[g]) == 1: #if cell has only one number
                for cell in u:
                    if cell != g:
                        puzzle[cell] = puzzle[cell].replace(puzzle[g],"") #remove that number from other cells in unit
                continue

            el = set() #list of possibilities to eliminate from g
            for cell in u:
                if len(puzzle[cell]) == 1: #if any other cells in unit are solved
                    el.add(puzzle[cell]) # add those number to elimination list

            for e in el:
                if e in puzzle[g]:
                    puzzle[g] = puzzle[g].replace(e,"") #remove those numbers from g's possibilities

            #ONLY SQUARE
            for p in puzzle[g]:
                rowstr = ''.join(puzzle[r] for r in row(puzzle,g))
                onlyrow = rowstr.count(p)
                if onlyrow == 1:
                    puzzle[g] = p
                    return eliminate(puzzle)

                colstr = ''.join(puzzle[c] for c in column(puzzle,g))
                onlycol = colstr.count(p)
                if onlycol == 1:
                    puzzle[g] = p
                    return eliminate(puzzle)

                boxstr = ''.join(puzzle[b] for b in box(puzzle,g))
                onlybox = boxstr.count(p)
                if onlybox == 1:
                    puzzle[g] = p
                    return eliminate(puzzle)

    return puzzle


def solve(puzzle):
    '''
    if not solved(puzzle):
        puzzle = eliminate(puzzle)
        return solve(puzzle)
    '''
    if not puzzle: return False
    if solved(puzzle): return puzzle

    min_poss = min((len(puzzle[g]),g)[1] for g in puzzle if len(puzzle[g])>1)
    possibilities = puzzle[min_poss]

    for val in possibilities:
        test_puzzle = puzzle.copy()
        test_puzzle[min_poss] = val

        test_puzzle = eliminate(test_puzzle)
        if solve(test_puzzle):
            return solve(test_puzzle)
        else: continue



filename = input("enter filename: ")
with open(filename) as f:
    puzzles = f.read().splitlines()

print()
i = 0
totaltime = []
for p in puzzles:
    sudoku = prepare(p)
    print("#", i)
    print("original: ")
    disp_sud(sudoku)
    print()
    start = default_timer()
    sudoku = solve(sudoku)
    duration = default_timer() - start
    print("solved:")
    disp_sud(sudoku)
    print()
    print("time: ", duration, "seconds")
    i+=1
    totaltime.append(duration)

max_time = max(totaltime)
max_time_puzzle = totaltime.index(max_time)
print("total time: ", sum(totaltime))
print("longest puzzle: ", "#", max_time_puzzle, " ", max_time, " seconds")