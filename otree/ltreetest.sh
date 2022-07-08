#!/bin/bash
make all
for i in {2..14}
do
    echo -n "testing t=$i..."
    diff <(./otree $i -l) <(./lukapull $i) && echo "done." || echo "Error: test failed for case t=$i"
done
