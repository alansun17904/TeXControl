#!/bin/bash
# Alan Sun (12/24/21)
# Testing program for TeXControl

# Testing project creation
# Normal cases
txctrl project proj.test1
txctrl project proj.test2
txctrl project proj.test3

# No project name provided 
txctrl project 

# Creating template files 
echo "\documentclass[12pt]{article}
\usepackage[margin=1in]{geometry}
\title{Template 1}
\author{Alan Sun}
\date{\today}
\begin{document}
\maketitle

\section{Problem}

\section{Solution}

\end{docment}" >> proj.test1/templates/template1.tex
