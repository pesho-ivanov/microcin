microcin
========

Microcin bacterial system simulation and verification 

PRISM model checker: http://www.prismmodelchecker.org/

run
===

cd microcin
chmod +x run
./run \
  [ MODEL_FILE = microcin.pm \
  [ PROPERTIES_FILE = microcin.csl \
  [ CONSTS_FILE = const.txt \
  [ RESULTS_FILE = res.txt \
  [ additional prism arguments ] ] ] ] ]

where
  CONSTS_FILE must be in the format '-const VAR=[value] | [from]:[step]:[to] [, ...]

