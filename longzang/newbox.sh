export TESSDATA_PREFIX=/Users/chris/projects/chi_pre/xp/lzfull

ntif="L028-013b.tif L028-014a.tif L028-014b.tif L028-015a.tif L028-015b.tif L028-016a.tif L028-016b.tif L028-017a.tif L028-017b.tif L028-018a.tif L028-018b.tif L028-019a.tif L028-019b.tif L028-020a.tif L028-020b.tif L028-021a.tif L028-021b.tif L028-025a.tif L028-025b.tif L028-028a.tif L028-028b.tif L028-029a.tif L028-029b.tif L028-031a.tif L028-031b.tif L028-033a.tif L028-033b.tif L028-034a.tif L028-034b.tif L028-035a.tif L028-035b.tif L028-036a.tif L028-036b.tif L028-037a.tif L028-037b.tif L028-038a.tif L028-038b.tif L028-039a.tif L028-039b.tif L028-040a.tif L028-040b.tif"

for t in $ntif
do
    echo $t
    b=`basename $t .tif`
    tesseract $t $b -l chi_zhdz makebox cjk
done
