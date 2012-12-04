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
import scipy.optimize

import pylab

from unum import *
from unum.units import *
from unum import Unum

unit      = Unum.unit
avogadro  = 6.02214129e23

CFU       = unit("CFU",       0,              "colony-forming unit")
OD_unit   = unit("OD",        0,              "optical density unit")
molecule  = unit("molecule", mol / avogadro )
ml        = unit("ml",       10**-3 * L,     "milliliter")
#ul        = unit("ul",       10**-6 * L,     "microliter")

possible_unit_expressions = { s, molecule/L, CFU/L, OD_unit }

# all the equivalent to the lab-data units simple units
def convert_units(num):
  for u in possible_unit_expressions:
    try:
      res = num.asUnit(u)
    except IncompatibleUnitsError:
      pass
    else:
      return res

  print 'No possible unit conversion for ', res
  assert(False)

time_unit = convert_units(s)
from_time = convert_units(2.0*h)
to_time = convert_units(8.0*h)
time_steps = 300
grid = time_unit * np.linspace(from_time.asNumber(), to_time.asNumber(), time_steps)

def myplot(data, title, X=None, Y=None):
  img_file = os.path.join(data_dir, title + '.png')
  
  grid_h = grid.asUnit(h)

  if not X is None and not Y is None:
    pylab.plot(X.asUnit(h).asNumber(), Y.asNumber(), 'o')

  pylab.plot(grid_h.asNumber(), data.asNumber())
  pylab.ylabel(data.strUnit())
  pylab.xlabel(grid_h.strUnit())
  pylab.title(title)
  pylab.grid(True)
  pylab.savefig(img_file)
  #pylab.show()
  print "A figure saved in", img_file

  pylab.close()

""" returns a polynomial"""
def approx_poly(X, Y, polydeg, var_name):
  coefs = np.polyfit(X.asNumber(), Y.asNumber(), polydeg)
  poly = np.poly1d(coefs)
  data = Unum(Y._unit) * array( poly(grid.asNumber()) )

  return data

def sigmoid(p,x):
    x0,y0,c,k=p
    y = c / (1 + np.exp(-k*(x-x0))) + y0
    return y

def residuals(p,x,y):
  return y - sigmoid(p,x)

def approx_gompetz(X, Y):
  p_guess = (np.median(X.asNumber()), np.median(Y.asNumber()), 1.0, 0.001)
  p, cov, infodict, mesg, ier = scipy.optimize.leastsq(residuals, p_guess,
        args=(X.asNumber(),Y.asNumber()), full_output=1)  
  data = Unum(Y._unit) * [ sigmoid(p, x) for x in grid.asNumber() ]
 
  print p
  return data

def read_json(fn):
  with open(fn, 'r') as f:
    return simplejson.load(f)

def unit_array(arr):
  num = eval(arr[0]) * np.array(arr[1])
  return convert_units(num)

""" returns a polynomial """
def extract(var_name, deg):
  if all_data.has_key(var_name):
    data = all_data[var_name]
    X = unit_array(data["time"])
    Y = unit_array(data["value"])
    
    if var_name == 'OD':
      func = approx_gompetz(X, Y)
    else:
      func = approx_poly(X, Y, deg, var_name)

    title = var_name + '-polyfit-deg' + str(deg)
    myplot(func, title, X, Y)

    return func
  else:
    print 'No %s data.' % variable
    assert(False)
  
def central_derivative(B):
  A = B.asNumber()

  dt          = grid[1].asNumber() - grid[0].asNumber()

  first_prim  = (A[1] - A[0]) / dt
  A_prim      = [ (A[t+1] - A[t-1]) / (2*dt) for t in range(1, len(A)-1) ]
  last_prim   = (A[-1] - A[-2]) / dt

  return Unum(B._unit) / time_unit * array([first_prim] + A_prim + [last_prim])

def calc_per_cell(product, cells, product_name):
  product_per_cell = product / cells
  myplot(product_per_cell, product_name)

def calc_per_cell_per_time(product, cells, product_name):
  product_per_cell = product / cells
  product_per_cell_per_time = central_derivative(product_per_cell)
  myplot(product_per_cell_per_time, product_name)

def process():
  #MccB    = extract('MccB', 2)
  extMcC  = extract('extMcC', 1)
  cells   = extract('cells', 1)
  OD      = extract('OD', 1)

  calc_per_cell(extMcC, cells, 'extMcC_per_cell')
  calc_per_cell_per_time(extMcC, cells, 'extMcC_per_cell_per_time')

  calc_per_cell(extMcC, OD, 'extMcC_per_OD')
  calc_per_cell_per_time(extMcC, OD, 'extMcC_per_OD_per_time')

if __name__ == '__main__': 
  if len(sys.argv) != 2:
    print 'One argument needed: simplejson file with consts from lab experiments'
  else:
    data_file = sys.argv[1]
    data_dir = os.path.dirname(data_file)
    all_data = read_json(data_file)
    process()
