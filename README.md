microcin
========

Microcin bacterial system simulation/verification

Continuous-Time Markov-Chain (CTMC) model

PRISM model checker: http://www.prismmodelchecker.org/

run
===
    cd microcin
    chmod +x run
    ./run \
      [ MODEL_FILE = microcin.pm \
      [ PROPERTIES_FILE = microcin.csl \
      [ CONSTS_FILE = const.in \
      [ RESULTS_FILE = res.out \
      [ additional prism arguments ] ] ] ] ]

where
-----
  CONSTS_FILE must be in the format '-const VAR=[value] | [from]:[step]:[to] [, ...]
  RESULTS_FILE will contain a table for each property with a line for each constants combination
