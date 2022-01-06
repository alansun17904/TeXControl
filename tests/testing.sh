#!/bin/bash
# Alan Sun
# 12/25/21
# Testing program for TeXControl

# Create project
txctrl project proj1

# Create template document
echo "\documentclass[12pt]{article}
\title{Template 1}
\begin{document}
\maketitle
\section{Section}

\section{Section}

\section{Section}

\end{document}" > proj1/templates/temp1.tex

# Create several new chapters
cd proj1
txctrl create climbingStairs "Ways to climb stairs" temp1 leetcode dp
txctrl create equalPartitionSum "Equal Partition Sum" temp1 leetcode dp algo
txctrl create search2DMatrix "Searching a 2D matrix" temp1 leetcode binarysearch algo
txctrl create majorityElement "Finding the majority element in an array" temp1 leetcode algo
txctrl create levenshtein "Levenshtein Distance" temp1 dp

