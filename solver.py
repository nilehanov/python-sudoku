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
    self.sqrtSqrtLen = int(math.sqrt(self.sqrtLen))
    self.indexer = {}
    self.buildIndexer()
    self.buildPoss()
  def readInPuzzle(self):
    input = []
    for line in csv.reader(open(self.fileName)):
      input.append(line)
    self.puzzleElements = input[0]
    for row in input[1:]:
      self.puzzle += row
    for i in range(len(self.puzzle)):
      if self.puzzle[i] not in self.puzzleElements:
        self.puzzle[i] = ' '
  def buildIndexer(self):
    for i in range(self.len):
      self.indexer[i] = {
        'R' : int(i / self.sqrtLen),
        'C' : i % self.sqrtLen,
        'B' : int(i / self.sqrtSqrtLen ** 3) * 3 + int(i / self.sqrtLen) % self.sqrtSqrtLen,
      }
    self.indexer['R'] = {}
    self.indexer['C'] = {}
    self.indexer['B'] = {}
    for ######################################## bed time    
 in self.indexer[i] if val['R'] == i]
    self.indexer['C'][i] = [val['C'] for val in self.indexer[i] if val['C'] == i]
    self.indexer['B'][i] = [val['B'] for val in self.indexer[i] if val['B'] == i]
  def printIndexer(self):
    print self.indexer.keys()
    for i in self.indexer.keys():
      print self.indexer[i]
  def printPuzzle(self):
    output = ""
    for i in range(self.len):
      output += str(self.puzzle[i]) + " "
      if i % self.sqrtLen == self.sqrtLen - 1:
        output += "\n"
    output = output[0:-1]
    print output
  def getR(self, rowNum):
    return self.puzzle[rowNum * self.sqrtLen : rowNum * self.sqrtLen + self.sqrtLen]
  def getC(self, colNum):
    output = []
    for i in range(self.len):
      if i % self.sqrtLen == colNum:
        output.append(self.puzzle[i])
    return output
  def getB(self, boxNum):
    output = []
    for i in self.indexer.keys():
      print self.indexer[i]
      if self.indexer[i]['B'] == boxNum:
        output.append(self.puzzle[i])
    return output
  def getBoxNum(self, index):
    target = int(boxNum / 3) * self.sqrtLen ** 3 + boxNum % self.sqrtLen
    return index / self.sqrtLen
  def setCellValue(self, rowNum, colNum, value):
    self.puzzle[rowNum * self.sqrtLen + colNum] = value
  def setIndexValue(self, index, value):
    self.puzzle[index] = value
  def buildPoss(self):
    self.poss = []
    for i in range(self.len):
      self.poss.append([])
    for i in range(self.len):
      self.poss[i] = self.puzzleElements[:]
    for i in range(self.len):
      if self.puzzle[i] in self.puzzleElements:
        self.poss[i] = [self.puzzle[i]]
  def stepPoss(self):
    num = 0
    for i in range(self.len):
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
#    for box in range(self.len):
      
#    return num

puzzle1 = puzzle(puzzleFile)
puzzle2 = puzzle(puzzleFile)

puzzle1.printPuzzle()

print "Puzzle elements:"
print puzzle1.puzzleElements

print "Rows:"
for i in range(puzzle1.sqrtLen):
  print puzzle1.getR(i)
print "Cols:"
for i in range(puzzle1.sqrtLen):
  print puzzle1.getC(i)

print "Indexer:"
puzzle1.printIndexer()

print "Boxes:"
for i in range(puzzle1.sqrtLen):
  print puzzle1.getB(i)

#for i in range(3):
#  print "===========================FIRE(" + str(i) + " = " + str(puzzle1.stepPoss()) + ")========================="
#  for row in range(puzzle1.len):
#    print "row " + str(row) + ":"
#    print puzzle1.poss[row]

print "Old puzzle:"
puzzle2.printPuzzle()

print "New puzzle:"
puzzle1.printPuzzle()




#puzzle1.setCellValue(0, 0, 5)
#print "Did box 0 change?"
#print puzzle1.getB(0)

