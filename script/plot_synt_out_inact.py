import sys
import os 
import shutil 
import re

# visualization code
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import pyplot, mpl

# my code
import collect_results as cr
from gen_exp_const import custom_range
reload(cr)

# all possible properties to check
death_tag = '"cell_death_prob": P=? [ F<=T McCin>=DEATH_LIMIT ]'
ext_mcc_tag = '"externalMcC": R{"out"}=? [ I=T ]'
int_mcc_tag = '"internalMcC": R{"in"}=? [ I=T ]'
#all_tags = [ death_tag, ext_mcc_tag, int_mcc_tag ]
all_tags = [ ext_mcc_tag, int_mcc_tag ]

params = [ 'synthesis_rate', 'output_rate', 'inactivation_rate' ]

def const_to_array(record, var, test):
# returns all the 'var' values of parameters for which the 'test' is satisfied
  return [ d['const'][var] for d in record if test(d['res']) ] 

def res_to_array(record, tag, test):
  return [ d['res'][tag] for d in record if test(d['res']) ] 
  
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
  
def plot_synt_out_inact(records, test_tag_name, val, image_dir):
  test_tag = eval(test_tag_name)

  plt.clf()
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  
  # set min/max limits
  testall = make_test(test_tag, '>-inf')
  xall, yall, zall = [ np.log10(const_to_array(records, var, testall)) for var in params ]
  ax.set_xlim3d([min(xall), max(xall)])
  ax.set_ylim3d([min(yall), max(yall)])
  ax.set_zlim3d([min(zall), max(zall)])
 
  # collect needed points
  #test = make_test(test_tag, val)
  test = make_test(test_tag, '>-inf')
  x, y, z = [ np.log10(const_to_array(records, var, test)) for var in params ]
  
  c = res_to_array(records, test_tag, test)
  max_c = max(c)
  volume = [ 200.0*(cc/max_c) for cc in c ]

  scat = ax.scatter(x, y, z, c=c, cmap=mpl.cm.jet, marker='o', s=volume, alpha=1, linewidths=None)
  
  # add axes labels
  ax.set_xlabel('log10('+params[0]+')')
  ax.set_ylabel('log10('+params[1]+')')
  ax.set_zlabel('log10('+params[2]+')')

  #ax.set_xticks([1,2])
  #pyplot.yticks([1,2], ['a', 'b'])

  time = int(records[0]['const']['T'])
  property_name = re.search(r'"[^"]*"', test_tag).group().strip('"')
  image_file = os.path.join(image_dir, test_tag_name + '-T' + str(time).zfill(8) + '.png')
  
  # add colorbar
  colbar = fig.colorbar(scat, shrink=0.5, aspect=20)
  colbar.set_label( property_name + ' (#molecules)' )

  # add title
  plt.title( property_name + ' (T=' + str(time) + ')' )

  # show and save
  plt.savefig(image_file)
  #plt.show()
  #plt.close()
  #ax.clear()

  return image_file

def load_data(res_dir):
  # collect the const&res data
  data = cr.collect_results(res_dir)
  records = data['records']

  # assert that the global tags in the script are the same as the tags in 'records'
  assert(len(records[0]['res']) == len(all_tags))
  for tag in all_tags:
    assert(records[0]['res'].has_key(tag)) 

  return data

def records_slice(records, var, val):
  return [ r for r in records if r['const'][var]==val ] 

if __name__ == "__main__":
  if len(sys.argv)<2:
    print 'An argument with the results directory needed'
    assert(False)

  res_dir = sys.argv[1]

  data = load_data(res_dir)
  records = data['records']
  consts_table = data['consts_table']

  basename = os.path.basename(res_dir.strip('/'))
  image_dir = os.path.join('images/', basename)
  if os.access(image_dir, os.F_OK):
    shutil.rmtree(image_dir)
  os.mkdir(image_dir)
  print 'Output dir: ', image_dir
  
  for t in custom_range(consts_table['T']):
    if t>200000: continue
    r = records_slice(records, var='T', val=t)
    int_fn = plot_synt_out_inact(r, 'int_mcc_tag', '>2', image_dir)
    ext_fn = plot_synt_out_inact(r, 'ext_mcc_tag', '>2', image_dir)
    joint_fn = ' '.join(['convert', int_fn, ext_fn, '+append', os.path.join(image_dir, 'T'+str(int(t)).zfill(8)+'.png')])
    os.system(joint_fn)

  os.system(' '.join(['convert', '-delay 100', os.path.join(image_dir, 'T*.png'), os.path.join(image_dir, basename+'.gif')]))

  #plot_synt_out_inact(records, death_tag, '>0.01')
  #plot_synt_out_inact(r1, ext_mcc_tag, '>2')
  #plot_synt_out_inact(r1, int_mcc_tag, '>2')


