#!/bin/env bash
# nice oneliner
# cat tikz_header <( ./bintree-standalone $1 ) tikz_footer | pdflatex
# cat tikz_header <( ./bintree-standalone $1) tikz_footer > trees.tex # uncomment if you want to save to tex file
cat tikz_header <( ./bintree-standalone ) tikz_footer > $1.tex # uncomment if you want to save to tex file
