#!/bin/bash
make all
for i in {1..10}
do
    echo -n "testing t=$i..."
    diff <(./clot $i) <(./coolDyck $i) && echo "done." || echo "Error: test failed for case t=$i"
done
