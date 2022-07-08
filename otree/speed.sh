#!/bin/bash
TIMEFORMAT="%R"
for i in {1..22}
do
    echo "testing n=$i..."
    # n-1 generates trees with n nodes
    echo -n "noparent: "
    time ./otree-noparent $(( $i - 1 )) > /dev/null

    echo -n "parent: "
    time ./otree-standalone $(( $i - 1 )) > /dev/null 
    
    echo
    
done
