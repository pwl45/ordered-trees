#!/bin/bash
make all
TIMEFORMAT="%Rs"
for i in {1..15}
do
    echo -n "testing n=$i..."
    # n-1 generates trees with n nodes
    time ./otree $(( $i - 1 )) > /dev/null 
    
done
