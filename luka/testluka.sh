#!/usr/bin/env bash

# list of test cases
declare -a tests=(
"2,0,1"
"4,0,0,1"
"2,2,1"
"0,1,1,1,1" # multiset permutations
"0,1,2,3,2" # multiset permutations
"3,1,2,1,2" # almost lukasiewicz
"3,0,2"
"3,2,2"
"4,2,3"
"8,2,7"
# "8,4,7" # too slow
"6,0,0,0,0,0,1"
"3,3,0,1"
"11,1,1,1,1,1"
"10,3,0,1,1,1"
"13,0,13" # big dyck test: C_13
"7,5,2,2"
"8,3,3,2"
"12,2,2,1,1,1"
"13,0,0,0,1,1,1"
"202,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1"
"0,666,0" # will only have one permutation
)

ret=0
# simplifies things, 
if [ -z "$1" ]; then 
	ref="balanced_permutations.py"
	refargs="-anpd"
	luka="luka"
	lukaargs=""
else
	ref=$1
	refargs=$2
	luka=$3
	lukaargs=$4
fi
echo "Comparing results of ./$ref $refargs to ./$luka"
for test in "${tests[@]}"
do 
	echo "Testing $test..."
	# still bad, don't feel like changing
	./$ref $test $refargs > outfile1
	./$luka $test $lukaargs> outfile2
	diff outfile1 outfile2 > difffile
	if [ $? -ne 0 ]; then
		echo "Test results differ. Diff:"
		# cat difffile
		ret=1
	fi
	echo
done

if [ $ret -ne 0 ]; then
	echo "At least one test failed. See above output."
else
	echo "All tests passed."
fi

rm outfile1
rm outfile2
rm difffile




