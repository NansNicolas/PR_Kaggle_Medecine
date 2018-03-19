#!/bin/bash 

# Traitement pour obtenir une suite de phrases :
# - sans parenthèses
# - sans crochets
# - sans nombres excepté l'ID en début de ligne
# - sans ponctuation a part les points et le || delimiter entre l'ID et le texte
# - sans double espaces

sed -i -r 's/\([^)]*\)//g' $1
sed -i -r 's/\[[^]]*\]//g' $1
sed -i -r 's/[[:digit:]]*//2g' $1
sed -i -r 's/\. /mmm/g;s/\|\|/nnn/1;s/-/\ /g;s/[[:punct:]]//g;s/mmm/\. /g;s/nnn/\|\|/1' $1
sed -i -r 's/[ ]+/\ /g' $1 
