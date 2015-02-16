# -*- coding: utf-8 -*-
import sys, codecs, os, math
try:
    from PIL import Image
    from PIL import ImageDraw
except:
    pass

class Tesseract3Box:

    text = u''

    left = None
    right = None
    top = None
    bottom = None
    height = None
    width = None
    page = None

    valid = False


    def make_string(self):
        """Constructs a box string from the box object"""
        string = u''

        string +=  u'%s %d %d %d %d %d' % (self.text, self.left, self.bottom, self.right, self.top, self.page)

        return string

    def set_text(self, string):
        if type(string) is str or type(string) is unicode:
            self.text = string
        else:
            raise TypeError(u"Box text must be a string, not " + str(type(string)))

    def __init__(self, string=None):

        if not string:
            return

        fields = string.split()

        if len(fields) == 6:
            try:

                self.left = int(fields[1])
                self.bottom = int(fields[2])
                self.right = int(fields[3])
                self.top = int(fields[4])
                self.height = abs(self.top - self.bottom)
                self.width = abs(self.right - self.left)
                self.page = int(fields[5])

                self.text = fields[0]

                self.valid = True

            except ValueError: 
                return

    def __repr__(self):
        return "Tesseract3Box: "+self.make_string()

    def __str__(self):
        return self.make_string()

    def __unicode__(self):
        return self.make_string()

class Tesseract3BoxFile:
    filename=None
    imgfile=None
    boxes=None
    img=None
    writdir=None
    imgwidth=None
    imgheight=None
    def __init__(self, filename=None):
        if not filename:
            return
        self.filename=filename
        try:
            self.boxes=parse_boxfile(filename)
        except:
            return None
        self.imgfile="%s.tif" % (filename[:-4])
        try:
            #print "reading %s" % (self.imgfile)
            self.img=Image.open(self.imgfile)
            self.imgwidth, self.imgheight=self.img.size
        except:
            pass
            #print "reading %s failed..." % (self.imgfile)
        self.writdir=self.getDirection()
        
    def getDirection(self):
        "try to guess the writing direction from the first two boxes"
        #eliminate small differences
        b1l = (self.boxes[0].left / 10 ) * 10
        b2l = (self.boxes[1].left / 10 ) * 10
        if b2l - b1l > 0:
            return "rtl"
        else:
            return "ltr"


    def makebins(self, step=1):
        """put the boxes in buckets of similar size.  Problem: find suitable size of step..."""
        bx=[[]]
        oldv=0
        b=[(i, math.sqrt(a.width*a.height)) for i, a in enumerate(self.boxes)]
        b=sorted(b, key=lambda x : x[1])
        for i in b:
            if i[1] - oldv < step:
                bx[-1].append(i)
            else:
                bx.append([i])
            oldv = i[1]
        #we put the first bin there, it should be empty...
        if len(bx[0]) > 0:
            self.bins=bx
        else:
            self.bins=bx[1:]
        
    def writebox(self, boxfile, box):
        bf=codecs.open(boxfile, 'w', 'utf-8')
        bf.write("%s 0 0 %d %d 0\n" % (box.text, box.width, box.height))
        bf.close()

    def writetext(self, out=None):
        if not out:
            f=codecs.getwriter('utf8')(sys.stdout)
        else:
            f=codecs.open(out, "w", "utf-8")
        f.write("\n")
        lastl=0
        for box in self.boxes:
            if self.writdir == "rtl":
                l=(box.left / 10) * 10
            else:
                l=(box.bottom / 10) * 10
            if l < lastl:
                f.write("\n")
                #f.write("# l, lastl %d %d\n" % (l, lastl)), 
            lastl = l
            f.write(box.text)
        f.write("\n")
        f.close()

    def cutbox(self, no, target=None):
        #boxes are 0 based
        fn=self.filename[:-4].split('.')
        fn.insert(-2, no)
        ret=False
        try:
            thisbox=self.boxes[int(no)-1]
        except:
            print "Box not found!", no
            return ret
        if self.img:
            try:
                #out=self.img[self.img.shape[0]-thisbox.top:self.img.shape[0]-thisbox.bottom,thisbox.left:thisbox.right]
                obox = thisbox.left, self.imgheight - thisbox.top, thisbox.right, self.imgheight - thisbox.bottom
                out= self.img.crop(obox)
            except:
                #print "Error cropping box %s %s" % (no, obox)
                return ret
        if not target:
            #target = "%s_%s_%s.tif" % (self.filename[:-4], no, thisbox.text)
            #target = "%s.tif" % (".".join(fn))
            #self.writebox("%s.box" % (target[:-4]), thisbox)
            return thisbox.text, out
        else:
            try:
                os.makedirs(target)
            except:
                pass
            tgfile = "%s/%s.tif" % (target, ".".join(fn))
            self.writebox("%s.box" % (tgfile[:-4]), thisbox)
            out.save(tgfile)
            return True
class TessTiffBoxFile:
    #a list of tuples: (box, img)
    boxes=[]
    imgwidth=None
    imgheight=None
    writdir=None
    def __init__(self, size, writdir="ltr"):
        #size is a tuple (x,y)
        self.imgwidth, self.imgheight = size
        self.writdir=writdir
        self.img=Image.new('RGB', size, "white")
        
    def addbox(self, boximg):
        self.boxes.append(boximg)

    def write(self, filename, dx=10):
        #before we go, we need to find the max dimensions of the boxes
        draw=ImageDraw.Draw(self.img)
        maxx = max([a[1].size[0] for a in self.boxes])
        maxy = max([a[1].size[1] for a in self.boxes])
        bs=[(i, math.sqrt(a[1].size[0]*a[1].size[1])) for i, a in enumerate(self.boxes)]
        bs=sorted(bs, key=lambda x : x[1])
        xo=yo=dx
        fn=1
        boxfile=codecs.open("%s%2.2d.box" % (filename, fn), 'w', 'utf-8')
        for ix in bs:
            b, i = self.boxes[ix[0]]
            boxfile.write("%s %d %d %d %d 0\n" % (b, xo, self.imgheight - yo - maxy , xo+i.size[0], self.imgheight - yo + i.size[1] - maxy))
            self.img.paste(i, (xo, yo + maxy - i.size[1]))
            xo += dx + i.size[1]
            if xo + dx + maxx > self.imgwidth:
                yo += dx + maxy
                #draw.line(((0, yo), (self.imgwidth, yo)), fill=128)
                yo += 10
                if yo + dx + maxy > self.imgheight:
                    self.img.save("%s%2.2d.tif" % (filename, fn))
                    self.img=Image.new('RGB', (self.imgwidth, self.imgheight), "white")
                    draw=ImageDraw.Draw(self.img)
                    boxfile.close()
                    fn += 1
                    boxfile=codecs.open("%s%2.2d.box" % (filename, fn), 'w', 'utf-8')
                    yo = dx
                xo = dx
            
        self.img.save("%s%2.2d.tif" % (filename, fn))
        self.img=Image.new('RGB', (self.imgwidth, self.imgheight), "white")
        boxfile.close()
            

def parse_boxfile(file_path):
    """Read in a boxfile, return an array of Tesseract3Box objects"""

    with codecs.open(file_path,mode='r',encoding='utf-8') as ifile:
        boxes = list()

        for line in ifile:
            boxes.append(Tesseract3Box(line))

    return boxes

def separation_x(box1,box2):
    """Return the horizontal separation of the boxes."""
    # We don't know which is left and which is right, so calc both and return
    # the smallest value, which will be the inside separation.
    sep1 = abs(box1.right - box2.left)
    sep2 = abs(box2.right - box1.left)
    
    return min(sep1,sep2)

def separation_y(box1,box2):
    """Return the vertical separation of the boxes."""
    sep1 = abs(box1.top - box2.bottom)
    sep2 = abs(box2.top - box1.bottom)

    return min(sep1,sep2)

def merge_two_boxes(box1,box2):
    merged = Tesseract3Box()

    if box1.page != box2.page:
        raise ValueError("Can't merge boxes on different pages.")

    merged.left     = min(box1.left,box2.left)
    merged.right    = max(box1.right,box2.right)
    merged.bottom   = min(box1.bottom,box2.bottom)
    merged.top      = max(box1.top,box2.top)

    merged.page = box1.page
    merged.text = box1.text + box2.text

    merged.valid = True
    #Ignore italic, uline, and bold -- they are meaningless to merged
    #boxes, so leave them false.
    return merged
