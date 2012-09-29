#!/usr/bin/python

import sys
import os 
import shutil # High-level file operations (to delete a non-empty directory) 
import math 

A = []
A.append( ('synthesis_rate', 1e-6, 1e3, 10) )
A.append( ('input_rate', 1e-10) )
A.append( ('output_rate', 1e-6, 1e3, 10) )
A.append( ('inactivation_rate', 1e-6, 1e3, 10) )
A.append( ('T', 120) )
A.append( ('death_limit', 30) )

file_path = 'const/'
file_cnt = 0
file_beg = 'const.in'

def exp_range3(start, stop, step):
  steps = int(math.ceil( math.log(stop,step) - math.log(start,step) ) + 1)
  return (start*step**exp for exp in range(0, steps))

def exp_range(s):
  if len(s)==1:
    return [s[0]]

  return exp_range3(s[0], s[1], s[2])

def rec_gen(lvl, s):
  global file_cnt

  if lvl >= len(A):
    print s[:-2]          
    with open( file_path + file_beg + '.' + str(file_cnt).zfill(4), 'w' ) as f:   # current file name
      f.write(s[:-2])           # without '\n' and ','
      file_cnt += 1
    return

  s += A[lvl][0] + '='
  for num in exp_range(A[lvl][1:4]):
    rec_gen(lvl+1, s+str(num)+',\n')

if __name__ == '__main__':
  file_cnt = 0

  if os.access(file_path, os.F_OK):
    shutil.rmtree(file_path)
    #os.removedirs(file_path)
  os.mkdir(file_path)

  rec_gen(0, "")
