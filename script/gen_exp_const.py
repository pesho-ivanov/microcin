#!/usr/bin/python

import sys
import os 
import shutil # High-level file operations (to delete a non-empty directory) 
import math 
import simplejson

A = {}
A['MAX_MCC_OUT'] = ( 'const', (100,) )
A['DEATH_LIMIT'] = ( 'const', (10,) )
A['input_rate'] = ( 'const', (0,) )
A['synthesis_rate'] = ( 'exp', (1e-3, 1e2, 10) )
A['output_rate'] = ( 'exp', (1e-8, 1e2, 10) )
A['inactivation_rate'] = ( 'exp', (1e-12, 1e0, 100) )
A['T'] = ( 'const', (10, 10*10, 10*10*10, ) )

file_path = 'const/'
file_cnt = 0
file_beg = 'const.in'
file_consts_table = 'consts_table.txt'

def exp_range(start, stop, step):
  steps = int(math.ceil( math.log(stop,step) - math.log(start,step) ) + 1)
  return (start*step**exp for exp in range(0, steps))

def custom_range(interval):
  distr = interval[0]
  arr = interval[1]

  if distr=='const':
    return arr
  elif distr=='exp':
    return exp_range(arr[0], arr[1], arr[2])

def rec_gen(B, lvl, s):
  global file_cnt

  if lvl >= len(B):
    fn = os.path.join(file_path, file_beg + '.' + str(file_cnt).zfill(4))
    with open(fn, 'w') as f:   # current file name
      os.chmod(fn, 0664)
      f.write(s[:-2])           # without '\n' and ','
      file_cnt += 1
    return

  s += B[lvl] + '='
  for num in custom_range(A[ B[lvl] ]):
    rec_gen(B, lvl+1, s+str(num)+',\n')

def cleardir():
  if os.access(file_path, os.F_OK):
    shutil.rmtree(file_path)
  os.mkdir(file_path)

def gen():
  rec_gen(list(A), 0, "")
  print str(file_cnt) + ' const files generated in ' + file_path

def serialize():
  fn = os.path.join(file_path, file_consts_table)
  with open(fn, 'w') as f:
    os.chmod(fn, 0664)
    simplejson.dump(A, f)

if __name__ == '__main__': 
  cleardir()
  serialize()
  gen()
