#!/bin/bash
make all
for i in {1..13}
do
    echo -n "testing t=$i..."
    diff <(./otree $i) <(./coolDyck $i) && echo "done." || echo "Error: test failed for case t=$i"
done
