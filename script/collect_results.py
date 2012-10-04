#!/usr/bin/python

import sys
import os 
from pprint import pprint

def read_const(fn):
  with open(fn, 'r') as f:
    X = [ line.strip(' ,\n').split('=') for line in f.readlines() ]
    const = dict([ (x[0], float(x[1])) for x in X ])
    return const

def read_res(fn): 
  with open(fn, 'r') as f:
    X = [ line.strip(' :\n') for line in f.readlines() if line.strip()!='' and line.strip()!='Result' ]
    assert( len(X)%2 == 0 )
    res = dict([ (X[i],float(X[i+1])) for i in xrange(0,len(X),2) ])
    return res

def collect_results(path):
  path = path.strip('/') + '/'
  print path

  S = []
  file_cnt = 0
  file_const_beg = 'const.in'
  file_res_beg = 'res.out'

  data = []

  while True:
    fn_const = path + file_const_beg + '.' + str(file_cnt).zfill(4)
    fn_res = path + file_res_beg + '.' + str(file_cnt).zfill(4)
    file_cnt = file_cnt+1

    #print fn_const, fn_res
    if not os.path.isfile(fn_const) or not os.path.isfile(fn_res):
        break
  
    const = read_const(fn_const)
    res = read_res(fn_res)

    #pprint(const)
    #pprint(res)

    data.append( { 'const': const, 'res': res } )

  print "Results and constants collected from %d files." % (len(data))
  return data

if __name__ == "__main__":
  assert( len(sys.argv)>=2 )
  collect_results( sys.argv[1] )
