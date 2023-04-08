
#!/bin/bash

while read line; do
  IFS='&' read -ra elements <<< "$line"
  directory="trome/${elements[0]:32:4}/${elements[0]:36:2}/${elements[0]:38:2}"
  filename="$directory/trome_${elements[0]:32:4}-${elements[0]:36:2}-${elements[0]:38:2}#${elements[1]:5}"
  echo "Downloading $line to $filename"
  mkdir -vp "$directory"
  wget "$line" -O "$filename"
done < final_list.txt
