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
molecule  = unit("molecule",  mol / avogadro )
ml        = unit("ml",        10**-3 * L,     "milliliter")
#ul        = unit("ul",       10**-6 * L,     "microliter")

possible_unit_expressions = { s, molecule/L, CFU/L, OD_unit, kg/L }
mols_in_kg = 1 / 1.178

# all the equivalent to the lab-data units simple units
def convert_units(num):
  for u in possible_unit_expressions:
    try:
      res = num.asUnit(u)
    except IncompatibleUnitsError:
      pass
    else:
      if res.strUnit() == '[kg/L]':
        res = (mol/L) * (res.asNumber() * mols_in_kg)
        return res.asUnit(molecule/L)
      else:
        return res

  print 'No possible unit conversion for ', num
  assert(False)

time_unit = convert_units(s)
#from_time = convert_units(2.5*h)
from_time = convert_units(4.5*h)
#to_time = convert_units(8.0*h)
to_time = convert_units(20.0*h)
time_steps = 300
grid = time_unit * np.linspace(from_time.asNumber(), to_time.asNumber(), time_steps)

def myplot(data, title, X=None, Y=None):
  img_file = os.path.join(data_dir, title + '.png')
  
  grid_h = grid.asUnit(h)

  if not X is None and not Y is None:
    pylab.plot(X.asUnit(h).asNumber(), Y.asNumber(), 'o')

  #pylab.ticklabel_format(useOffset=False)
  #plt.autoscale()
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
  arr = [ sigmoid(p, x) for x in grid.asNumber() ]
  data = Unum(Y._unit) * np.array(arr)

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
    
    if deg == 'gompetz':
      func = approx_gompetz(X, Y)
      print 'gompetz'
    else:
      func = approx_poly(X, Y, deg, var_name)

    title = var_name + '-polyfit-deg' + str(deg)
    myplot(func, title, X, Y)

    return func
  else:
    print 'No %s data.' % var_name
    #assert(False)
  
def deriv(B):
  A = B.asNumber()

  dt          = grid[1].asNumber() - grid[0].asNumber()

  first_prim  = (A[1] - A[0]) / dt
  A_prim      = [ (A[t+1] - A[t-1]) / (2*dt) for t in range(1, len(A)-1) ]
  last_prim   = (A[-1] - A[-2]) / dt

  return Unum(B._unit) / time_unit * array([first_prim] + A_prim + [last_prim])

def process():
  cells               = extract('cells',                1)
  #cells               = extract('cells',        'gompetz') 
  OD                  = extract('OD',                   1)
  #OD                  = extract('OD',           'gompetz')

  extMcC_WT           = extract('extMcC_WT',            1)
  intMcC_WT           = extract('intMcC_WT',            1)
  extMcC_import       = extract('extMcC_import',        1)
  intMcC_import       = extract('intMcC_import',        1)
  extMcC_inact_import = extract('extMcC_inact_import',  1)
  intMcC_inact_import = extract('intMcC_inact_import',  1)

  # useless
  extMcC_inact        = extract('extMcC_inact',         1)
  intMcC_inact        = extract('intMcC_inact',         1)
  extMcC_inact        = extMcC_inact / cells
  intMcC_inact        = intMcC_inact / cells
  myplot(extMcC_inact, 'extMcC_WT')
  myplot(intMcC_inact, 'intMcC_WT')

  try:
    extMcC_WT           = extMcC_WT / cells
    intMcC_WT           = intMcC_WT / cells
    extMcC_import       = extMcC_import / cells
    intMcC_import       = intMcC_import / cells
    extMcC_inact_import = extMcC_inact_import / cells
    intMcC_inact_import = intMcC_inact_import / cells

    # (1)-import
    # [ molecule / s ] = [ molecule / s ] / [ molecule ]
    export_rate = deriv(extMcC_import) / intMcC_import
    export_rate.asUnit( 1 / s )
    
    #export_rate2 = deriv(extMcC_import) / intMcC_import
    
    # (2)WT
    import_rate = ( export_rate * intMcC_WT - deriv(extMcC_WT)) / extMcC_WT
    import_rate.asUnit( 1 / s )

    # (2)-inact-import
    synth_rate = deriv(intMcC_inact_import) + export_rate * intMcC_inact_import
    synth_rate.asUnit( molecule / (CFU * s) )

    # (2)-import
    inactivation_rate = ( synth_rate - export_rate * intMcC_import - deriv(intMcC_import) ) / intMcC_import
    inactivation_rate.asUnit( 1 / s )
    
    export_rate[0] *= 0.9999999
    
    myplot(extMcC_import, 'extMcC_import')
    myplot(intMcC_WT, 'intMcC_WT')
    myplot(extMcC_WT, 'extMcC_WT')
    
    myplot(export_rate, 'export_rate')
    myplot(import_rate, 'import_rate')
    myplot(synth_rate, 'synth_rate')
    myplot(inactivation_rate, 'inactivation_rate')
  except:
    print 'Calculation error!'
    pass
  else:
    return

if __name__ == '__main__': 
  if len(sys.argv) != 2:
    print 'One argument needed: simplejson file with consts from lab experiments'
  else:
    data_file = sys.argv[1]
    data_dir = os.path.dirname(data_file)
    all_data = read_json(data_file)
    process()
