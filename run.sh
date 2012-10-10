#!/bin/sh

if [ $# -ne 1 ]
then
  echo "Usage: <res_dir>"
  exit 1
fi

ROOT_DIR="./"
SRC_DIR=$ROOT_DIR"src/"
SCRIPTS_DIR=$ROOT_DIR"scripts/"
ARCHIVE_DIR=$ROOT_DIR"archive/"
RES_DIR=$ARCHIVE_DIR$1"/"
CONSTS_DIR=$RES_DIR"const/"
OUT_DIR=$RES_DIR"out/"
IMG_DIR=$RES_DIR"images/"

CONSTS_TABLE_FN="consts_table.txt" # input grid parameters
MODEL_FN="microcin.pm"          # CTMC model 
PROPERTIES_FN="microcin.csl"    # properties to test
TIME_FN="time.txt"              # time stamps for every prism run
LOG_FN="prism.log"              # what prism said

GEN_SCRIPT=$SCRIPTS_DIR"gen.py"        # generate consts
PLOT_SCRIPT=$SCRIPTS_DIR"plot.py"       # plot graphics

# READ
CONSTS_TABLE_FILE=$ROOT_DIR$CONSTS_TABLE_FN
MODEL_FILE=$SRC_DIR$MODEL_FN                  
PROPERTIES_FILE=$SRC_DIR$PROPERTIES_FN        

# WRITE
TIME_FILE=$RES_DIR$TIME_FN
LOG_FILE=$RES_DIR$LOG_FN

DEFAULT_ARGS="-sor -fixdl"
#CMD_LINE_ARGS=$@                             # additional command line arguments

if [ -d $RES_DIR ]
then
  rm $RES_DIR -r
fi
mkdir $RES_DIR
mkdir $CONSTS_DIR
mkdir $OUT_DIR

# run the generative script
$SCRIPT_DIR$GEN_SCRIPT $CONSTS_DIR $CONSTS_TABLE_FILE

if [ ! -f $CONSTS_TABLE_FILE ] # || (! -f $MODEL_FILE) || (! -f $PROPERTIES_FILE) ]]
then
  echo 'One of the following files is missing'
  echo $CONSTS_TABLE_FILE
  echo $MODEL_FILE
  echo $PROPERTIES_FILE
  exit 1
fi

cp $CONSTS_TABLE_FILE $RES_DIR
cp $MODEL_FILE $RES_DIR
cp $PROPERTIES_FILE $RES_DIR

if [ -f $TIME_FILE ]
then
  rm $TIME_FILE
  touch $TIME_FILE
fi
echo "start" >> $TIME_FILE
date >> $TIME_FILE

for f in $CONSTS_DIR/*; do
  num=$(echo "$f" | awk -F . '{print $NF}') # gives the number after the last dot
  echo "$num"
  
  CONSTS="-const $(cat $f | tr -d '\n')"
  RES_FN="res.out.$num"
  RESULTS="-exportresults $OUT_DIR$RES_FN"
  ARGS="$MODEL_FILE $PROPERTIES_FILE $CONSTS $RESULTS $DEFAULT_ARGS"
  
  #$SCRIPT_DIR/run.sh "$f"
  echo "prism "$ARGS
  prism $ARGS | tee --append --ignore-interrupts $LOG_FILE

  #awk -v res_file=$RESULTS_FILE 'BEGIN{RS="\n\n"; ORS=""} { cnt++; print $0 > res_file"."cnt }' $RESULTS_FILE
  
  date >> $TIME_FILE
done

echo "finish" >> $TIME_FILE

$SCRIPT_DIR$PLOT_SCRIPT $RES_DIR $OUT_DIR $IMG_DIR       # run the plot script
