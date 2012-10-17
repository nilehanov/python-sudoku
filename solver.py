#!/usr/bin/env python
import csv
import math

puzzleFile = 'puzzle1.csv'

class puzzle():
  def __init__(self, fileName):
    self.fileName = fileName
    self.puzzle = []
    self.puzzleElements = []
    self.readInPuzzle()
    self.len = len(self.puzzle)
    self.sqrtLen = int(math.sqrt(self.len))
    self.buildPoss()
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
#  def whichBox(self, row, cell):
#    return 
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
    for row in range(self.len):
      for cell in range(self.len):
        if self.puzzle[row][cell] in self.puzzleElements:
          self.poss[row][cell] = [self.puzzle[row][cell]]
  def stepPoss(self):
    num = 0
    for row in range(self.len):
      for cell in range(self.len):
        if len(self.poss[row][cell]) == 1:
          for rowPop in range(self.len):
            if rowPop != row:
              self.poss[rowPop][cell] = [item for item in self.poss[rowPop][cell] if item not in self.poss[row][cell]]
          for cellPop in range(self.len):
            if cellPop != cell:
              self.poss[row][cellPop] = [item for item in self.poss[row][cellPop] if item not in self.poss[row][cell]]
    for row in range(self.len):
      for cell in range(self.len):
        if len(self.poss[row][cell]) == 1 and self.puzzle[row][cell] not in self.puzzleElements:
          num += 1
          #print "Found row:" + str(row) + " cell:" + str(cell) + " equals:" + str(self.poss[row][cell][0])
          self.puzzle[row][cell] = self.poss[row][cell][0]
    for box in range(self.len):
      
    return num

puzzle1 = puzzle(puzzleFile)
puzzle2 = puzzle(puzzleFile)

puzzle1.printPuzzle()

print "Puzzle elements:"
print puzzle1.puzzleElements
print "Rows:"
for i in range(len(puzzle1.puzzle)):
  print puzzle1.R(i)
print "Cols:"
for i in range(len(puzzle1.puzzle)):
  print puzzle1.C(i)
print "Boxes:"
for i in range(len(puzzle1.puzzle)):
  print puzzle1.B(i)

for i in range(3):
  print "===========================FIRE(" + str(i) + " = " + str(puzzle1.stepPoss()) + ")========================="
  for row in range(puzzle1.len):
    print "row " + str(row) + ":"
    print puzzle1.poss[row]

print "Old puzzle:"
for row in range(puzzle2.len):
  print puzzle2.puzzle[row]

print "New puzzle:"
for row in range(puzzle1.len):
  print puzzle1.puzzle[row]




#puzzle1.setCellValue(0, 0, 5)
#print "Did box 0 change?"
#print puzzle1.B(0)

