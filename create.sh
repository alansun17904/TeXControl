#!/bin/bash
# Alan Sun
# 12/14/2021
# Writeups TeX Generator

filename=$1
title=$2 

# Check argument validity
if [ $# -lt 2 ]; then 
  echo "Usage ./create.sh [filename] [title] [tag1] [tag2] [tag3] ... "
  exit 1
fi

# Create TeX directory and file
mkdir $filename
touch "$filename/$filename.tex"


# Add template to TeX file
echo "\documentclass[12pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{hyperref}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{soul}
\usepackage{indentfirst}
\usepackage{minted}
\usepackage{longtable}
\title{\vspace{-0.7in}$title}
\author{Alan Sun}
\date{$(date +"%B %d, %Y")}
\begin{document}
  \maketitle
  \section{Problem Description}

  \section{Solution}

\end{document}
" >> "$filename/$filename.tex"

# Create tags
for ((i=3; i<=$#; i++)) do
    touch "$filename/.${!i}"
done

# Open file with TeXShop
cd $filename
mkdir static
vi "$filename.tex"
