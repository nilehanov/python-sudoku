#!/usr/bin/env python

import os
import sys
import pickle
import sudokulib.sudoku as sudoku
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import TanhLayer
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

DATASET_FILE = 'dataset.pickle'
DATASET_SIZE = 10000
NETWORK_FILE = 'network.pickle'
SUDOKU_N = 3
HIDDEN_LAYERS = 5
EPOCHS = 10000

def format_puzzle(puz, format_type='input'):
    output = []
    temp_puz = puz.masked_grid if format_type=='input' else puz.solution
    for square in temp_puz:
        if square not in puz.possibles:
            output.extend(0 for _ in puz.possibles)
        else:
            output.extend(-1 if option != square else 1 for option in sorted(puz.possibles))
    return output

def save_network(net):
    with open(NETWORK_FILE, 'w') as f:
        pickle.dump(net, f)

def save_dataset(ds):
    with open(DATASET_FILE, 'w') as f:
        pickle.dump(ds, f)

#puzzle = sudoku.Sudoku()
#puzzle.print_masked()
#fp = format_puzzle(puzzle)
#fp_solved = format_puzzle(puzzle, format_type='output')
#
#print
#print fp
#print
#print len(fp)
#print
#print fp_solved
#print
#print len(fp_solved)
#ds.addSample(fp, fp_solved)

if '--fresh' in sys.argv or NETWORK_FILE not in os.listdir('.'):
    print 'New network'
    net = buildNetwork(SUDOKU_N ** 6, HIDDEN_LAYERS, SUDOKU_N ** 6, bias=True, hiddenclass=TanhLayer)
else:
    print 'Loading network'
    with open(NETWORK_FILE) as f:
        net = pickle.load(f)

if DATASET_FILE not in os.listdir('.'):
    print 'New dataset'
    ds = SupervisedDataSet(SUDOKU_N ** 6, SUDOKU_N ** 6)
else:
    print 'Loading dataset'
    with open(DATASET_FILE) as f:
        ds = pickle.load(f)
trainer = BackpropTrainer(net, ds)

while len(ds) < DATASET_SIZE:
    puzzle = sudoku.Sudoku()
    ds.addSample(format_puzzle(puzzle), format_puzzle(puzzle, format_type='output'))

print len(ds)

puzzle = sudoku.Sudoku()
print format_puzzle(puzzle)[:9]
print net.activate(format_puzzle(puzzle))[:9]
print
for i in range(EPOCHS):
    print trainer.train()
    print ' '.join('{:6.3f}'.format(x) for x in net.activate(format_puzzle(puzzle))[:9])
    print ' '.join('{:6.3f}'.format(float(x)) for x in format_puzzle(puzzle, format_type='output')[:9])
    save_network(net)
    save_dataset(ds)
