#!/usr/bin/env python
import csv
import math

puzzleFile = 'puzzle.csv'

class puzzle():
  def __init__(self, fileName):
    self.fileName = fileName
    self.puzzle = []
    self.readInPuzzle()
    self.sqrtLen = int(math.sqrt(len(self.puzzle)))
  def readInPuzzle(self):
    self.puzzle = []
    for line in csv.reader(open(self.fileName)):
      self.puzzle.append(line)
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



PUZZLE = puzzle(puzzleFile)

PUZZLE.printPuzzle()

print "Rows:"
for i in range(len(PUZZLE.puzzle)):
  print PUZZLE.R(i)
print "Cols:"
for i in range(len(PUZZLE.puzzle)):
  print PUZZLE.C(i)
print "Boxes:"
for i in range(len(PUZZLE.puzzle)):
  print PUZZLE.B(i)

#PUZZLE.setCellValue(0, 0, 5)
#print "Did box 0 change?"
#print PUZZLE.B(0)
