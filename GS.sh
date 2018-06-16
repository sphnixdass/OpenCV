#!/bin/bash  
echo "This is a shell script"
gs -dNOPAUSE -dBATCH -dFirstPage=1 -dLastPage=1 -sDEVICE=png16m -r300x300 -sOutputFile="DInputPage1.png" "/home/dass/Coding/Python/CV/TempInput.pdf"



