#!/usr/bin/env python
import csv
import math

puzzleFile = 'puzzle.csv'

class puzzle():
  def __init__(self, fileName):
    self.fileName = fileName
    self.puzzle = []
    self.puzzleElements = []
    self.readInPuzzle()
    self.len = len(self.puzzle)
    self.sqrtLen = int(math.sqrt(self.len))
  def readInPuzzle(self):
    input = []
    for line in csv.reader(open(self.fileName)):
      input.append(line)
    self.puzzleElements = input[0]
    self.puzzle = input[1:]
    for row in range(len(self.puzzle)):
      for cell in range(len(self.puzzle[row])):
        if self.puzzle[row][cell] == 'x':
          self.puzzle[row][cell] = ' '
  def printPuzzle(self):
    output = ""
    for row in self.puzzle:
      for cell in row:
        output += cell + " "
      output += "\n"
    output = output[0:-1]
    print output
  def R(self, rowNum):
    return self.puzzle[rowNum]
  def C(self, colNum):
    output = []
    for row in self.puzzle:
      output.append(row[colNum])
    return output
  def B(self, boxNum):
    output = []
    divVal = int(boxNum / self.sqrtLen) * self.sqrtLen
    modVal = (boxNum % self.sqrtLen) * self.sqrtLen
    for r in range(divVal, divVal + self.sqrtLen):
      for c in range(modVal, modVal + self.sqrtLen):
        output.append(self.puzzle[r][c])
    return output
  def setCellValue(self, rowNum, colNum, value):
    self.puzzle[rowNum][colNum] = value
  def buildPoss(self):
    self.poss = []
    for i in range(self.len):
      self.poss.append([])
      for j in range(self.len):
        self.poss[i].append([])
    for i in range(self.len):
      for j in range(self.len):
        self.poss[i][j] = self.puzzleElements[:]



PUZZLE = puzzle(puzzleFile)

PUZZLE.printPuzzle()

print "Puzzle elements:"
print PUZZLE.puzzleElements
print "Rows:"
for i in range(len(PUZZLE.puzzle)):
  print PUZZLE.R(i)
print "Cols:"
for i in range(len(PUZZLE.puzzle)):
  print PUZZLE.C(i)
print "Boxes:"
for i in range(len(PUZZLE.puzzle)):
  print PUZZLE.B(i)

print "Testing poss:"
PUZZLE.buildPoss()
for row in PUZZLE.poss:
  print row

#PUZZLE.setCellValue(0, 0, 5)
#print "Did box 0 change?"
#print PUZZLE.B(0)

