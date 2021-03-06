#!/bin/sh
echo "ID DS MONO BOOT CLADE" | tr ' ' '\t' > clades.txt; cat orig | sed -e 's/.RAxML.\([^\t]*\)\t/\t/' | awk -vFS='\t' '{print $1"\t""AA""\t"$2"\t"$3"\t"$4}' >> clades.txt
echo "ID	DS	MONO	BOOT	CLADE"
sed -e "s/.raxmlboot./\t/" -e "s/.RAxML.*.rooted\(.75.*\)\?_[0-9][0-9]*//g" -e "s/^\([^\t]*\)\t\([^\t]*\)/\2\t\1/g" -e "s/.f25\t/\t25Xfilter-/g" -e "s/.c1c2\t\([^\t]*\)\t/\t\1.C12\t/g" $1
