#!/usr/bin/env bash

# list of test cases
declare -a tests=(
"2,0,1"
"2,2,1"
"3,0,2"
"3,2,2"
"6,0,0,0,0,0,1"
"3,3,0,1"
"11,1,1,1,1,1"
"10,3,0,1,1,1"
"7,5,2,2"
"8,3,3,2"
# "12,2,2,1,1,1" # this one works, but takes sort of a while
)

ret=0
for test in "${tests[@]}"
do 
	echo "Testing $test..."
	./$1 $test -dp > outfile1
	./$1 $test -fdp > outfile2
	diff outfile1 outfile2 > difffile
	if [ $? -ne 0 ]; then
		echo "Test results differ. Diff:"
		cat difffile
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




