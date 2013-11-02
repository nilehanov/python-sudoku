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
DATASET_SIZE = 200
NETWORK_FILE = 'network.pickle'
SUDOKU_N = 3
HIDDEN_LAYERS = 1
EPOCHS = 10000

class Sudoku(sudoku.Sudoku):
    def __init__(self, *args, **kwargs):
        super(Sudoku, self).__init__(*args, **kwargs)
        # force population of instance vars
        _ = self.masked_grid

    @property
    def input_format(self):
        return self.format_puzzle(self.masked_grid)

    @property
    def output_fmt(self):
        return self.format_puzzle(self.solution)

    @classmethod
    def format_puzzle(cls, puz):
        output = []
        possibles = range(SUDOKU_N ** 2)
        for square in puz:
            if square not in possibles:
                output.extend(.1 for _ in possibles)
            else:
                output.extend(0. if option != square else 1. for option in possibles)
        return output

    @property
    def input_string(self):
        return self.to_string(self.masked_grid)

    @property
    def output_string(self):
        return self.to_string(self.solution)

    @classmethod
    def to_string(cls, grid):
        output = ''
        n = SUDOKU_N ** 2
        for i in range(n):
            output += ' '.join('_' if v == '_' else str(int(v)) for v in grid[i * n:(i + 1) * n])
            output += '\n'
        return output

    def __str__(self):
        return self.to_string(self.masked_grid)

    @classmethod
    def guess_string_from_net_output(cls, net_output):
        return cls.to_string(cls.guess_from_net_output(net_output))

    @classmethod
    def guess_from_net_output(cls, net_output):
        # de-numpy for slicing
        net_output = list(net_output)
        output = []
        n = SUDOKU_N ** 2
        for i in range(n ** 2):
            tmp = net_output[i * n:(i + 1) * n]
            tmp_ans = tmp.index(max(tmp))
            output.append(tmp_ans)
        return output

    @classmethod
    def guess_to_string(cls, puz):
        output = []
        n = SUDOKU_N ** 2
        for i in range(n):
            output.append(' '.join(str(int(v)) for v in puz[i * n:(i + 1) * n]))
        return '\n'.join(output) + '\n'

    def compare_guess_to_actual(self, guess):
        return self.compare_two_puzzle_strings(self.guess_to_string(guess), self.output_string)

    @classmethod
    def compare_two_puzzle_strings(cls, one, two):
        return ''.join(o if o==t else '_' for o, t in itertools.izip(one, two))


def save_network(net):
    with open(NETWORK_FILE, 'w') as f:
        pickle.dump(net, f)

def save_dataset(ds):
    with open(DATASET_FILE, 'w') as f:
        pickle.dump(ds, f)


if __name__ == '__main__':
    # setup network
    if '--new-net' in sys.argv or NETWORK_FILE not in os.listdir('.'):
        print 'New network'
        net = buildNetwork(SUDOKU_N ** 6, HIDDEN_LAYERS, SUDOKU_N ** 6, bias=True, hiddenclass=SigmoidLayer)
    else:
        print 'Loading network'
        with open(NETWORK_FILE) as f:
            net = pickle.load(f)
            net.sorted = False
            net.sortModules()

    # setup dataset
    if '--new-ds' in sys.argv or DATASET_FILE not in os.listdir('.'):
        print 'New dataset'
        ds = SupervisedDataSet(SUDOKU_N ** 6, SUDOKU_N ** 6)
    else:
        print 'Loading dataset'
        with open(DATASET_FILE) as f:
            ds = pickle.load(f)

    # setup trainer
    trainer = BackpropTrainer(net, ds)

    # ensures dataset is at least this big
    while len(ds) < DATASET_SIZE:
        puzzle = Sudoku()
        ds.addSample(puzzle.input_fmt, puzzle.output_fmt)
        ds.addSample(puzzle.output_fmt, puzzle.output_fmt)
    # stash it
    print 'Dataset size: {}'.format(len(ds))
    save_dataset(ds)

    # see what it looks like to start
    print 'Starting hits:'
    puzzle = Sudoku()

    print puzzle
    #print puzzle.output_fmt
    res = net.activate(puzzle.output_fmt)
    print puzzle.guess_string_from_net_output(res)

    #known = make_guess(format_puzzle(puzzle, format_type='output'))
    #known_string = string_puzzle_from_list(known)
    #guess = make_guess(net.activate(format_puzzle(puzzle, format_type='output')))
    #guess_string = string_puzzle_from_list(guess)
    #print compare_strings(known_string, guess_string)

    #pre = 0
    #pre_time = time.time()
    #for i in range(EPOCHS):
    #    puzzle = Sudoku()
    #    cur = trainer.train()
    #    delta = cur - pre
    #    pre = cur
    #    cur_time = time.time()
    #    time_delta = cur_time - pre_time
    #    pre_time = cur_time
    #    print 'Epoch: {:>5}\tError: {:9.7f}\tDelta: {:9.7f}\tTime delta: {}'.format(i + 1, cur, delta, time_delta)
    #    puzzle.print_masked()
    #    print 'Hits:'
    #    known = make_guess(format_puzzle(puzzle, format_type='output'))
    #    known_string = string_puzzle_from_list(known)
    #    print compare_strings(known_string, string_puzzle_from_list(make_guess(net.activate(format_puzzle(puzzle, format_type='output')))))
    #    save_network(net)
