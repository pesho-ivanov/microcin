import sys

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import pyplot, mpl

import collect_results as cr

# all possible properties to check
death_tag = '"cell_death_prob": P=? [ F<=T McCin>=DEATH_LIMIT ]'
ext_mcc_tag = '"externalMcC": R{"out"}=? [ I=T ]'
int_mcc_tag = '"internalMcC": R{"in"}=? [ I=T ]'
all_tags = [ death_tag, ext_mcc_tag, int_mcc_tag ]

params = [ 'synthesis_rate', 'output_rate', 'inactivation_rate' ]

def const_to_array(data, var, test):
# returns all the 'var' values of parameters for which the 'test' is satisfied
  return [ d['const'][var] for d in data if test(d['res']) ] 

def res_to_array(data, tag, test):
  return [ d['res'][tag] for d in data if test(d['res']) ] 
  
def make_test(tag, s):
# make a lambda that tests whether the 'tag'-parameter is less/greater than a number
# s is a string '<[num]' or '>[num]'
  assert(type(s)==str)

  val = float(s[1:])

  if s[0] == '<':
    return lambda res: res[tag] < val
  elif s[0] == '>':  
    return lambda res: res[tag] > val
  else:
    assert(False)
  
def plot_3d(data, test_tag, val):
  # collect needed points
  test = make_test(test_tag, val)
  x, y, z = [ np.log2(const_to_array(data, var, test)) for var in params ]
  
  #testall = make_test(test_tag, '>-inf')
  #x, y, z = [ np.log2(const_to_array(data, var, testall)) for var in params ]
  c = res_to_array(data, test_tag, test)

  # plot them
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  scat = ax.scatter(x, y, z, c=c, cmap=mpl.cm.jet, marker=',', s=50)
  #ax.scatter(x, y, z, c='r', marker='o')
  
  fig.colorbar(scat, shrink=0.5, aspect=5)

  # add axes labels
  ax.set_xlabel(params[0])
  ax.set_ylabel(params[1])
  ax.set_zlabel(params[2])

  # set min/max limits
  testall = make_test(test_tag, '>-inf')
  xall, yall, zall = [ np.log2(const_to_array(data, var, testall)) for var in params ]
  ax.set_xlim3d([min(xall), max(xall)])
  ax.set_ylim3d([min(yall), max(yall)])
  ax.set_zlim3d([min(zall), max(zall)])
 
  # add title and show
  plt.title(test_tag + ' ' + val)
  plt.show()

if __name__ == "__main__":
  reload(cr)
  
  assert( len(sys.argv)>=2 )

  # collect the const&res data
  data = cr.collect_results(sys.argv[1])

  # assert that the global tags in the script are the same as the tags in 'data'
  assert(len(data[0]['res']) == len(all_tags))
  for tag in all_tags:
    assert(data[0]['res'].has_key(tag)) 

  plot_3d(data, death_tag, '>0.01')
  plot_3d(data, ext_mcc_tag, '>2')
  plot_3d(data, int_mcc_tag, '>2')

