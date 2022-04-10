#!/bin/bash
make all
for i in {1..14}
do
    echo -n "testing t=$i..."
    diff <(./otree $i $1) <(./coolDyck $i) && echo "done." || echo "Error: test failed for case t=$i"
done
