import sys

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

import collect_results as cr

death_tag = '"cell_death_prob": P=? [ F<=T McCin>=DEATH_LIMIT ]:'
ext_mcc_tag = '"externalMcC": R{"out"}=? [ I=T ]:'
int_mcc_tag = '"internalMcC": R{"in"}=? [ I=T ]:'

params = [ 'synthesis_rate', 'output_rate', 'inactivation_rate' ]

def randrange(n, vmin, vmax):
    return (vmax-vmin)*np.random.rand(n) + vmin

def to_array(data, var):
  arr = []

  for d in data:
    const = d['const']
    res = d['res']
  
    print res[death_tag]
    if res[death_tag] > 1e-80:
      print '+',
      arr.append( const[var] )

  return arr

if __name__ == "__main__":
  reload(cr)

  assert( len(sys.argv)>=2 )
  data = cr.collect_results(sys.argv[1])

  x, y, z = [ np.log2(to_array(data, tag)) for tag in params ]
  
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  #ax.set_xscale('log')
  ax.scatter(x, y, z, c='r', marker='o')

  ax.set_xlabel(params[0])
  ax.set_ylabel(params[1])
  ax.set_zlabel(params[2])

  plt.show()
