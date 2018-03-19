#!/bin/bash 

# Traitement pour obtenir une ligne = ID + une phrase du texte correspondant à l'ID
# Le nombre de lignes total est egal au nombre de lignes de l'ensemble des textes

# Tous les phrases sont traitees pour être :
# - sans parenthèses
# - sans crochets
# - sans nombres excepté l'ID en début de ligne
# - sans ponctuation a part les points et le || delimiter entre l'ID et la phrase
# - sans double espaces



sed -i -r 's/\([^)]*\)//g' $1
sed -i -r 's/\[[^]]*\]//g' $1
sed -i -r 's/[[:digit:]]*//2g' $1
sed -i -r 's/\. /mmm/g;s/\|\|/nnn/1;s/-/\ /g;s/[[:punct:]]//g;s/mmm/\. /g;s/nnn/\|\|/1' $1
sed -i -r 's/[ ]+/\ /g' $1 

tmp=`awk -F'[|]+' '{if (NR >1) {split($2,a,"."); for (i=1;i<=length(a);i++) {print $1"||"a[i]}} else {print $0}}' $1`
echo "$tmp" > $1
