#export TESSDATA_PREFIX=/Users/chris/projects/chi_pre/xp/lzfull
export TESSDATA_PREFIX=/usr/local/Cellar/tesseract/HEAD/share/

ntif="AC34-p014.tif AC35a-p090.tif AC43-p0016.tif AC58-p0001.tif ICSH01-p007.tif AC26-p031.tif AC26-p032.tif AC26-p033.tif AC26-p034.tif AC27-p037.tif AC27-p038.tif AC27-p039.tif AC27-p040.tif AC27-p041.tif AC29-p083.tif AC29-p084.tif AC29-p085.tif AC29-p086.tif AC30-p031.tif AC30-p032.tif AC30-p033.tif AC30-p034.tif AC33-p015.tif AC33-p016.tif AC33-p017.tif AC33-p018.tif AC34-p015.tif AC34-p016.tif AC34-p017.tif AC34-p018.tif AC35a-p091.tif AC35a-p092.tif AC35a-p093.tif AC35a-p094.tif AC43-p0017.tif AC43-p0018.tif AC43-p0019.tif AC43-p0020.tif AC43-p0021.tif AC58-p0002.tif AC58-p0003.tif AC58-p0004.tif AC58-p0005.tif ICSH01-p008.tif ICSH01-p009.tif"

for t in $ntif
do
    echo $t
    b=`basename $t .tif`
    tesseract $t $b -l chi_zhdz makebox cjk
done
