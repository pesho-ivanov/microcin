#!/bin/sh

CONSTS_DIR="./const"
RES_DIR="./res"

rm $RES_DIR -r
mkdir $RES_DIR

for f in $CONSTS_DIR/*; do
  num=$(echo "$f" | awk -F . '{print $NF}') # gives the number after the last dot
  echo "$num"
  mv "$f" "const.in"
  ./run
  mv "res.out" "$RES_DIR/res.out.$num"
done
