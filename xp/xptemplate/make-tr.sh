lang=chi_pre.
files="inttemp pffmtable shapetable normproto"
#remove old training files.
for f in $files
do
    rm $lang$f
done   
rm tesseract-train-log.txt


for b in *.box
do
    echo $b
    echo $b >> tesseract-train-log.txt
    t=`basename $b .box`.tif
    tesseract $t $b nobatch box.train 2>> tesseract-train-log.txt
done

unicharset_extractor *.box
echo "mftraining"
mftraining -F chi_zhdz.font_properties -U unicharset -O chi_zhdz.unicharset *.tr 2>> tesseract-train-log.txt
echo "cntraining"
cntraining *.tr 2>> tesseract-train-log.txt
for f in $files
do
    mv $f $lang$f
done   
combine_tessdata $lang
mv ${lang}traineddata tessdata
