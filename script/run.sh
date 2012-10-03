#!/bin/sh

SRC_DIR="./src"
TMP_DIR="./tmp"
MODEL_FILE=$SRC_DIR/"microcin.pm"         # CTMC model 
PROPERTIES_FILE=$SRC_DIR/"microcin.csl"   # tested properties over the model
CONSTS_FILE=$TMP_DIR/"const.in"          # unknown parameters from MODEL and PROPERTIES files
RESULTS_FILE=$TMP_DIR/"res.out"           # simulation/verification results

#if [ $# -ge 1 ]; then MODEL_FILE=$1; fi
#if [ $# -ge 2 ]; then PROPERTIES_FILE=$2; fi
#if [ $# -ge 3 ]; then CONSTS_FILE=$3; fi
#if [ $# -ge 4 ]; then RESULTS_FILE=$4; fi

CONSTS="-const $(cat $CONSTS_FILE | tr -d '\n')"
RESULTS="-exportresults $RESULTS_FILE"
OTHER="-sor -fixdl"
#ADDITIONAL=${*:5}         # additional command line arguments
ADDITIONAL=$@               # additional command line arguments

ARGS="$MODEL_FILE $PROPERTIES_FILE $CONSTS $RESULTS $OTHER $ADDITIONAL"

echo "prism "$ARGS
prism $ARGS

awk -v res_file=$RESULTS_FILE 'BEGIN{RS="\n\n"; ORS=""} { cnt++; print $0 > res_file"."cnt }' $RESULTS_FILE

