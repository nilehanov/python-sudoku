#!/usr/bin/env python

import os
import sys
import time
import pickle
import itertools
import sudokulib.sudoku as sudoku
from pybrain.tools.shortcuts import buildNetwork
#from pybrain.structure import TanhLayer
from pybrain.structure import SigmoidLayer
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

DATASET_FILE = 'dataset.pickle'
DATASET_SIZE = 10000
NETWORK_FILE = 'network.pickle'
SUDOKU_N = 3
HIDDEN_LAYERS = 1
EPOCHS = 10000

def format_puzzle(puz, format_type='input'):
    output = []
    mg = puz.masked_grid
    sol = puz.solution
    temp_puz = mg if format_type=='input' else sol
    for square in temp_puz:
        if square not in puz.possibles:
            output.extend(.1 for _ in puz.possibles)
        else:
            output.extend(0. if option != square else 1. for option in sorted(puz.possibles))
    return output

def make_guess(net_output):
    net_output = list(net_output)
    output = []
    n = SUDOKU_N ** 2
    for i in range(n ** 2):
        tmp = net_output[i * n:(i + 1) * n]
        tmp_ans = tmp.index(max(tmp))
        output.append(tmp_ans)
    return output

def string_puzzle_from_list(puz):
    output = ''
    n = SUDOKU_N ** 2
    for i in range(n):
        output += ' '.join(str(int(v)) for v in puz[i * n:(i + 1) * n])
        output += '\n'
    return output

def compare_strings(one, two):
    return ''.join(a if a==b else '_' for a, b in itertools.izip(one, two))

def save_network(net):
    with open(NETWORK_FILE, 'w') as f:
        pickle.dump(net, f)

def save_dataset(ds):
    with open(DATASET_FILE, 'w') as f:
        pickle.dump(ds, f)


if '--fresh' in sys.argv or NETWORK_FILE not in os.listdir('.'):
    print 'New network'
    net = buildNetwork(SUDOKU_N ** 6, HIDDEN_LAYERS, SUDOKU_N ** 6, bias=True, hiddenclass=SigmoidLayer)
else:
    print 'Loading network'
    with open(NETWORK_FILE) as f:
        net = pickle.load(f)
        net.sorted = False
        net.sortModules()

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
    time.sleep(.1)
    f_in  = format_puzzle(puzzle)
    f_out = format_puzzle(puzzle, format_type='output')
    ds.addSample(f_in, f_out)
    ds.addSample(f_out, f_out)
save_dataset(ds)

print 'Dataset size: {}'.format(len(ds))

puzzle = sudoku.Sudoku()
print 'Starting hits:'
known = make_guess(format_puzzle(puzzle, format_type='output'))
known_string = string_puzzle_from_list(known)
guess = make_guess(net.activate(format_puzzle(puzzle, format_type='output')))
guess_string = string_puzzle_from_list(guess)
print compare_strings(known_string, guess_string)

pre = 0
for i in range(EPOCHS):
    cur = trainer.train()
    delta = cur - pre
    pre = cur
    print 'Epoch: {:>5}\tError: {:9.7f}\tDelta: {:9.7f}'.format(i + 1, cur, delta)
    print 'Hits:'
    print compare_strings(known_string, string_puzzle_from_list(make_guess(net.activate(format_puzzle(puzzle, format_type='output')))))
    save_network(net)
