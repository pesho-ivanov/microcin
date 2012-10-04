#!/bin/sh

# evokes run.sh for every file in $ROOT/const/*
# writes as many result files in $ROOT/res/
CONSTS_DIR="./const"
RES_DIR="./res"
SCRIPT_DIR="./script"
TMP_DIR="./tmp"

rm $RES_DIR -r
mkdir $RES_DIR

echo "start" >> $TMP_DIR/"time"
date >> $TMP_DIR/"time"

for f in $CONSTS_DIR/*; do
  num=$(echo "$f" | awk -F . '{print $NF}') # gives the number after the last dot
  echo "$num"
  cp "$f" $RES_DIR
  mv "$f" $TMP_DIR/"const.in"
  $SCRIPT_DIR/run.sh
  mv $TMP_DIR/"res.out" "$RES_DIR/res.out.$num"
done

echo "finish" >> $TMP_DIR/"time"
date >> $TMP_DIR/"time"
mv $TMP_DIR/"time" $RES_DIR/"time"
