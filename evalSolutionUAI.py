#!/usr/bin/python
"""
evalSolutionUAI.py
by Lars Otten <lotten@ics.uci.edu>, 2011

Computes likelihood/cost of an assignment for a given graphical model.

First argument: UAI file name with graphical model specification.
Further arguments: Discarded until number of problem variables is
found, after which the assignment will be read.

Copyright (c) 2011 by Lars Otten
Licensed under MIT License:

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os, sys
from math import log10, pow


INFINITY = float("inf")

def to_log10(d):
  if d == 0:
    return -INFINITY
  else:
    return log10(d)

def from_log10(d):
  if d == -INFINITY:
    return 0.0
  else:
    return pow(10.0, d)
  

class Function:
  """Represents a function in the graphical model"""
  def __init__(self, id, scope, table):
    self.id = id
    self.scope = scope
    self.table = table

  def __str__(self):
    s = "Function %i with scope [" % self.id
    s += ",".join(map(str, self.scope))
    s += "] and table size %i" % len(self.table)
    return s


class ModelInstance:
  """Represents a graphical model instances"""

  def __init__(self):
    self.num_vars = -1
    self.domains = []
    self.num_funs = -1
    self.functions = []

  def read_model_uai(self, filename):
    """Reads a graphical from UAI file"""
    with open(filename, "r") as f:
      T = f.read().strip().split()
  
    i = 0  # poor man's tokenizer
    type = T[i]
    i += 1
    print "Reading %s network from file %s" % (type, filename)

    # Read variables and domain sizes
    self.num_vars = int(T[i])
    i += 1
    print "Number of problem variables: %i" % self.num_vars
    self.domains = map(int, T[i : i + self.num_vars])
    i += self.num_vars

    # Read function scopes
    self.num_funs = int(T[i])
    i += 1
    print "Number of problem functions: %i" % self.num_funs
    fun_scopes = [[]] * self.num_funs
    for j in range(self.num_funs):
      scope_size = int(T[i])
      i += 1
      fun_scopes[j] = map(int, T[i : i + scope_size])
      i += scope_size
      
    # Read function tables
    for j in range(self.num_funs):
      table_size = int(T[i])
      i += 1
      table = map(float, T[i : i + table_size])
      table = map(to_log10, table)
      i += table_size
      self.functions.append(Function(j, fun_scopes[j], table))

  def evaluate_assignment(self, assignment):
    """Calculates the cost of a given assignment"""
    return 0.0  # TODO calculate assignment cost


def parse_assignments(num_vars, args):
  """parses full assignments from command line arguments"""
  i = 0
  assignments = []
  while i < len(args):
    if args[i] == str(num_vars):
      assignments.append(map(int, args[i : i + num_vars]))
      i += num_vars
    else:
      i += 1
  print "Found %i assignment(s)" % len(assignments)
  return assignments
  

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print "Specify model file"
    sys.exit(1)

  model = ModelInstance()
  model.read_model_uai(sys.argv[1])

  assignments = parse_assignments(model.num_vars, sys.argv[2:])
  for i, assignment in enumerate(assignments):
    cost = model.evaluate_assignment(assignment)
    print "Assignment %i cost:\t%f" % (i, cost)
