from Tesseract3Box import *
import sys

if len(sys.argv) > 2:
    bf= Tesseract3BoxFile(sys.argv[1])
    if sys.argv[2] == "text":
        bf.writetext("%s.txt" % (sys.argv[1][:-4]))
    else:
        bf.writetext(sys.argv[2])
else:
    tff = TessTiffBoxFile((2000, 3000))
    for line in codecs.open(sys.argv[1], 'r', 'utf-8'):
        if ".box" in line:
            boxfile = line[:-1]
            bf= Tesseract3BoxFile(boxfile)
        elif "Couldn't find a matching blob" in line:
            n = line.split('/')[0].split()[-1]
            tff.addbox(bf.cutbox(n))
    tff.write("/tmp/ttfbox/test", dx=30)

