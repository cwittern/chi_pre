ntif="zd090128a.zhdz.exp0.tif zd090128b.zhdz.exp0.tif zd090128c.zhdz.exp0.tif zd090129a.zhdz.exp0.tif zd090129b.zhdz.exp0.tif zd090129c.zhdz.exp0.tif zd090130a.zhdz.exp0.tif zd090130b.zhdz.exp0.tif zd090130c.zhdz.exp0.tif zd090131a.zhdz.exp0.tif zd090131b.zhdz.exp0.tif zd090131c.zhdz.exp0.tif zd090132a.zhdz.exp0.tif zd090132b.zhdz.exp0.tif zd090132c.zhdz.exp0.tif zd090133a.zhdz.exp0.tif zd090133b.zhdz.exp0.tif zd090133c.zhdz.exp0.tif zd090134a.zhdz.exp0.tif zd090134b.zhdz.exp0.tif zd090134c.zhdz.exp0.tif zd090135a.zhdz.exp0.tif zd190001a.zhdz.exp0.tif zd190001b.zhdz.exp0.tif zd190001c.zhdz.exp0.tif zd190002a.zhdz.exp0.tif zd190002b.zhdz.exp0.tif zd190002c.zhdz.exp0.tif zd190003a.zhdz.exp0.tif zd190003b.zhdz.exp0.tif zd190003c.zhdz.exp0.tif zd190048c.zhdz.exp0.tif zd190049a.zhdz.exp0.tif zd190049b.zhdz.exp0.tif zd190049c.zhdz.exp0.tif zd190050a.zhdz.exp0.tif zd190050b.zhdz.exp0.tif zd190050c.zhdz.exp0.tif zd190051a.zhdz.exp0.tif zd190051b.zhdz.exp0.tif zd190051c.zhdz.exp0.tif"

for t in $ntif
do
    echo $t
    b=`basename $t .tif`
    tesseract $t $b -l chi_zhdz makebox cjk
done
