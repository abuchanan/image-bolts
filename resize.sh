#!/bin/bash

for p in $(ls -1 images/original/*.jpg)
do
  n=$(basename $p)
  convert $p -resize 40% images/resized/$n
done
