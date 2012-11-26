#!/usr/bin/python

import os 
import re
import sys 
import math
import __builtin__

import simplejson

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

import pylab

from unum import *
from unum.units import *
from unum import Unum

unit      = Unum.unit
avogadro  = 6.02214129e23

CFU       = unit("CFU",      0,              "colony-forming unit")
molecule  = unit("molecule", mol / avogadro )
ul        = unit("ul",       10**-6 * L,     "microliter")
ml        = unit("ml",       10**-3 * L,     "milliliter")

# all the equivalent to the lab-data units simple units
possible_units = {
    h,
    molecule/L,
    CFU/L,
}

grid = np.arange(2.0, 8.0+0.1, 0.1)

def myplot(Y, data_dir):
  img_file = os.path.join(data_dir, Y[2] + '.png')
  pylab.plot(grid, Y[0].asNumber())
  pylab.ylabel(Y[0].strUnit())
  pylab.xlabel(Y[1].strUnit())
  pylab.title(Y[2])
  pylab.grid(True)
  pylab.savefig(img_file)
  #pylab.show()
  print "A figure saved in ", img_file

  pylab.close()

""" returns a polynomial"""
def approx(X, Y, polydeg, data_dir, var_name):
  logX = np.log(X)
  coefs = np.polyfit(X, Y, polydeg)
  poly = np.poly1d(coefs)

  img_file = os.path.join(data_dir, 'polyfit-' + var_name + '-deg' + str(polydeg) + '.png')
  plt.subplot(111)
  plt.plot(X, Y, 'o', grid, poly(grid), '-')
  plt.legend(['data', 'deg'+str(polydeg)], loc='best')
  pylab.title(var_name)
  plt.savefig(img_file)
  plt.close()
  print "A figure saved in ", img_file
  
  return array(poly(grid))

def read_json(fn):
  with open(fn, 'r') as f:
    return simplejson.load(f)

def unit_array(arr):
  num = eval(arr[0]) * np.array(arr[1])

  for u in possible_units:
    try:
      res = num.asUnit(u)
    except IncompatibleUnitsError:
      pass
    else:
      return res

  print 'No possible unit conversion for ', res
  assert(False)

""" returns a polynomial """
def extract(all_data, var_name):
  if all_data.has_key(var_name):
    data = all_data[var_name]
    X = unit_array(data["time"])
    Y = unit_array(data["concentration"])
    return Unum(Y._unit) * approx(X.asNumber(), Y.asNumber(), 2, data_dir, var_name), X[0], var_name
  else:
    print 'No %s data.' % variable
    assert(False)
  
def central_derivative(A):
  dt          = grid[1] - grid[0] 

  first_prim  = (A[1] - A[0]) / dt
  A_prim      = [ (A[t+1] - A[t-1]) / (2*dt) for t in range(1, len(A)-1) ]
  last_prim   = (A[-1] - A[-2]) / dt

  return array([first_prim] + A_prim + [last_prim])

if __name__ == '__main__': 
# takes a simplejson file with consts from lab experiments
  assert( len(sys.argv)==2 )
  data_file = sys.argv[1]
  data_dir = os.path.dirname(data_file)

  all_data = read_json(data_file)

  MccB    = extract(all_data, 'MccB')
  extMcC  = extract(all_data, 'extMcC')
  cells   = extract(all_data, 'cells')

  MccB_per_cell = MccB[0]/cells[0], MccB[1], 'MccB_per_cell'
  MccB_per_cell_per_h = central_derivative(MccB_per_cell[0].asNumber()), MccB_per_cell[1], 'MccB_per_cell_per_h'
  MccB_per_cell_per_h = Unum(MccB_per_cell[0]._unit) / h * central_derivative(MccB_per_cell[0].asNumber()), MccB_per_cell[1], 'MccB_per_cell_per_h'

  myplot(MccB_per_cell, data_dir)
  myplot(MccB_per_cell_per_h, data_dir)

