#!/usr/bin/env python
import csv
import math

puzzleFile = 'puzzle1.csv'

class puzzle():

  def __init__(self, fileName):
    self.fileName = fileName
    self.puzzle = []
    self.puzzleElements = []
    self.poss = []
    self.indexer = {}

    self.buildPuzzle()

    self.len = len(self.puzzle)
    self.sqrtLen = int(math.sqrt(self.len))
    self.sqrtSqrtLen = int(math.sqrt(self.sqrtLen))

    self.buildIndexer()

    self.buildPoss()


  def buildPuzzle(self):
    input = []
    for line in csv.reader(open(self.fileName)):
      input.append(line)
    self.puzzleElements = input[0]
    for row in input[1:]:
      self.puzzle += row
    for i in range(len(self.puzzle)):
      if self.puzzle[i] not in self.puzzleElements:
        self.puzzle[i] = ' '


  def printPuzzle(self):
    output = ""
    for i in range(self.len):
      output += str(self.puzzle[i]) + " "
      if i % self.sqrtLen == self.sqrtLen - 1:
        output += "\n"
    output = output[0:-1]
    print output


  def buildIndexer(self):
    for i in range(self.len):
      self.indexer[i] = {
        'R' : int(i / self.sqrtLen),
        'C' : i % self.sqrtLen,
        'B' : int(i / self.sqrtSqrtLen ** 3) * 3 + (i % self.sqrtLen) / self.sqrtSqrtLen,
      }
    for k in ['R', 'C', 'B']:
      self.indexer[k] = []
      for i in range(self.sqrtLen):
        self.indexer[k].append([])
    for i in range(self.len):
      self.indexer['R'][int(i / self.sqrtLen)].append(i)
      self.indexer['C'][i % self.sqrtLen].append(i)
      self.indexer['B'][int(i / self.sqrtSqrtLen ** 3) * 3 + (i % self.sqrtLen) / self.sqrtSqrtLen].append(i)
    for i in range(self.len):
      self.indexer[i]['S'] = []
      for k in ['R', 'C', 'B']:
        for v in self.indexer[k][self.indexer[i][k]]:
          self.indexer[i]['S'].append(v)
        self.indexer[i]['S'].remove(i)
        self.indexer[i]['S'] = sorted(self.indexer[i]['S'])
      print self.indexer[i]['S']


  def printIndexer(self):
#    print self.indexer.keys()
    for i in self.indexer.keys():
      print str(i) + "===" + str(self.indexer[i])


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
    for i in range(self.len):
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
      if self.puzzle[i] in self.puzzleElements:
        self.poss.append([self.puzzle[i]])
      else:
        self.poss.append(self.puzzleElements[:])

  
  def printPoss(self):
    for i in range(self.len):
      print str(i) + ": " + str(self.poss[i])


  def stepPoss(self):
#    num = 0
    for i in range(self.len):
      print str(i) + " : " + str(self.poss[i])
      if len(self.poss[i]) == 1:
        for s in self.indexer[i]['S']:
          self.poss[s] = self.poss[s] not in [self.poss[i][0]]
#    return num

puzzle1 = puzzle(puzzleFile)
puzzle2 = puzzle(puzzleFile)

puzzle1.printPuzzle()

print "\nPuzzle elements:"
print puzzle1.puzzleElements

print "\nRows:"
for i in range(puzzle1.sqrtLen):
  print puzzle1.getR(i)

print "\nCols:"
for i in range(puzzle1.sqrtLen):
  print puzzle1.getC(i)

#print "Indexer:"
#puzzle1.printIndexer()

print "\nBoxes:"
for i in range(puzzle1.sqrtLen):
  print puzzle1.getB(i)

print "\npuzzle1.indexer['R'][0]"
print puzzle1.indexer['R'][0]
print "puzzle1.puzzle1[puzzle1.indexer['R'][0]] itteration"
output = ""
for i in puzzle1.indexer['R'][0]:
  output += str(puzzle1.puzzle[i]) + " "
print output

print "\npuzzle1.indexer['C'][0]"
print puzzle1.indexer['C'][0]
print "puzzle1.puzzle1[puzzle1.indexer['C'][0]] itteration"
output = ""
for i in puzzle1.indexer['C'][0]:
  output += str(puzzle1.puzzle[i]) + " "
print output

print "\npuzzle1.indexer['B'][0]"
print puzzle1.indexer['B'][0]
print "puzzle1.puzzle1[puzzle1.indexer['B'][0]] itteration"
output = ""
for i in puzzle1.indexer['B'][0]:
  output += str(puzzle1.puzzle[i]) + " "
print output

puzzle1.printPoss()

for i in range(3):
  print "===========================FIRE(" + str(i) + " = " + puzzle1.stepPoss() + ")========================="
  for row in range(puzzle1.len):
    print "row " + str(row) + ":"
    print puzzle1.poss[row]

print "\nOld puzzle:"
puzzle2.printPuzzle()

print "\nNew puzzle:"
puzzle1.printPuzzle()

#puzzle1.printIndexer()
#print puzzle1.indexer['R'][puzzle1.indexer[3]['R']]



#puzzle1.setCellValue(0, 0, 5)
#print "Did box 0 change?"
#print puzzle1.getB(0)

