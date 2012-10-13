#!/usr/bin/env python

puzzleFile = 'puzzle.txt'

class puzzle():
  def __init__(self, fileName):
    self.fileName = fileName
    self.puzzle = []
    self.readInPuzzle()
  def readInPuzzle(self):
    self.file = open(self.fileName)
    self.puzzle = []
    for line in self.file:
      self.puzzle.append(line.strip().split(' '))
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
  def R1(self):
    return self.puzzle[0]

PUZZLE = puzzle(puzzleFile)

PUZZLE.printPuzzle()

print PUZZLE.R1()
