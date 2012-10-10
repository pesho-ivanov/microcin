#!/bin/sh

# evokes run.sh for every file in $ROOT/const/*
# writes as many result files in $ROOT/res/
CONSTS_DIR="./const"
RES_DIR="./res"
SCRIPT_DIR="./script"
TMP_DIR="./tmp"

TIME_FILE="time.txt"
CONSTS_FILE="consts.in"
CONSTS_TABLE_FILE="consts_table.txt"

rm $RES_DIR -r
mkdir $RES_DIR

cp $CONSTS_TABLE_FILE $RES_DIR/
#cp $CONSTS_DIR/$CONSTS_FILE

rm $TMP_DIR/$TIME_FILE
echo "start" >> $TMP_DIR/$TIME_FILE
date >> $TMP_DIR/$TIME_FILE

for f in $CONSTS_DIR/*; do
  num=$(echo "$f" | awk -F . '{print $NF}') # gives the number after the last dot
  echo "$num"
  cp "$f" $RES_DIR/
  cp "$f" $TMP_DIR/"const.in"
  $SCRIPT_DIR/run.sh
  mv $TMP_DIR/"res.out" "$RES_DIR/res.out.$num"
  date >> $TMP_DIR/$TIME_FILE
done

echo "finish" >> $TMP_DIR/$TIME_FILE
date >> $TMP_DIR/"time"
mv $TMP_DIR/"time" $RES_DIR/$TIME_FILE
