#!/bin/bash

read input

while read line; do
  IFS='&' read -ra elements <<< "$line"
  year=${elements[0]:32:4}
  month=${elements[0]:36:2}
  day=${elements[0]:38:2}
  page=${elements[1]:5}
  echo $page
  echo "%05d" $page
  directory="trome/$year/$year-$month/$year-$month-$day" 


  filename="$directory/trome_$year-$month-$day#$page.png"
  echo "Downloading $directory to $filename"
  #mkdir -vp "$directory"
  #wget "$line" -O "$filename"
done < $input
