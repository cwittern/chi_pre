lang=chi_pre
log="../explog.txt"
code="../../code"
cwd=`pwd`
oneup=`dirname $cwd`
config=$1
export TESSDATA_PREFIX=`dirname $oneup`
rm tesseract-log.txt
echo "-------" >> $log
echo `basename $cwd`, $lang >> $log
echo "start: " `gdate "+%Y-%m-%d %H:%M:%S.%N %z"` >> $log
for img in *.tif
do
    filename=${img%%.*}
    echo $img >> tesseract-log.txt
    tesseract $img $filename -l $lang $config 2>> tesseract-rec-log.txt
    echo $img
    python $code/compare.py $filename.txt >> $log
    #echo "   Processed $img"
done
echo "done: " `gdate "+%Y-%m-%d %H:%M:%S.%N %z"` >> $log
