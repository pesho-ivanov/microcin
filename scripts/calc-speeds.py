#!/usr/bin/python

import os 
import sys 
import math
import __builtin__

import simplejson

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

from unum.units import *
from unum import Unum

avogadro = 6.02214129e23

unit      = Unum.unit
cfu       = CFU  = unit("CFU", 0, "colony-forming unit")
molecule  = CFU  = unit("molecule", avogadro * mol, "molecule")
ul        = ul   = unit("ul", 10**-6 * L, "microliter")
ml        = ml   = unit("ml", 10**-3 * L, "milliliter")

def myplot(arr):
  fig = plt.figure()
  ax = fig.add_subplot(111)
  X, Y = xyxy2XY(arr)
  ax.plot(X, Y, 'o-')
  plt.savefig('tmp.png')

def approx(X, Y, polydeg, data_dir):
  logX = np.log(X)
  coefs = np.polyfit(X, Y, polydeg)
  poly = np.poly1d(coefs)

  xnew = np.linspace(__builtin__.min(X), __builtin__.max(X), 40)
 
  img_file = os.path.join(data_dir, 'polyfit-deg' + str(polydeg) + '.png')
  plt.subplot(111)
  plt.plot(X, Y, 'o', xnew, poly(xnew), '-')
  plt.legend(['data', 'deg'+str(polydeg)], loc='best')
  plt.savefig(img_file)
  print "A figure saved in ", img_file
  
  return coefs  ## todo coefs

def read_json(fn):
  #os.system(' '.join(['cat', fn]))
  with open(fn, 'r') as f:
    return simplejson.load(f)

desired_units = { "time" : s, "concentration": molecule/L }

def unit_array(data, variable):
  array_with_units = data[variable]
  res = eval(array_with_units[0]) * np.array(array_with_units[1])
  return res.asUnit( desired_units[variable] )

# takes a simplejson file with consts from lab experiments
if __name__ == '__main__': 
  assert( len(sys.argv)==2 )
  data_file = sys.argv[1]
  data_dir = os.path.dirname(data_file)
  
  A = read_json(data_file)
  if A.has_key('MccB'):
    data = A['MccB']
    #myplot(arr)
    X = unit_array(data, "time")
    Y = unit_array(data, "concentration")
    print X, Y
    MccB_of_t = approx(X.asNumber(), Y.asNumber(), 2, data_dir)
    print MccB_of_t
