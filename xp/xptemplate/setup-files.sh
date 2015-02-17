#!bin/sh
dir=$1
td=../../$dir

for f in `cat ${td}/finished.txt`
do
    t=`basename $f .tif`
    echo $t
    cp $td/$t.tif .
    cp $td/$t.box .
done
