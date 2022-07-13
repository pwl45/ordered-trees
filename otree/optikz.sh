#!/bin/env bash
# nice oneliner
cat tikz_header <( ./otree $1 $2 ) tikz_footer | pdflatex
# cat tikz_header <( ./otree $1 $2 ) tikz_footer > trees.tex # uncomment if you want to save to tex file
