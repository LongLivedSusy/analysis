#!/bin/env python
import glob
import os
from optparse import OptionParser

parser = OptionParser()
(options, args) = parser.parse_args()

if len(args)>0:
    configurations = args
else:
    print "Run with \n$ ./www-create-pics.py path/to/folder/to/upload"
    quit()


outfolder = args[-1].split("/")[-1]
if outfolder[-1] == "/":
    outfolder = outfolder[:-1]

os.system("mkdir -p ~/www/track-shortening/%s" % outfolder)
os.system("cp -r %s/* ~/www/track-shortening/%s/" % (outfolder, outfolder))

html = ""
                
for ifile in sorted(glob.glob(outfolder + "/*.pdf")):
    print ifile
    outfile = ifile.split("/")[-1]
    
    os.system("convert ~/www/track-shortening/%s/%s ~/www/track-shortening/%s/%s" % (outfolder, outfile, outfolder, outfile.replace(".pdf", ".png")))
    
    html += """<a href="%s"><img src="%s" width="400"></a>\n""" % (outfile, outfile.replace(".pdf", ".png"))
    
with open("/afs/desy.de/user/k/kutznerv/www/track-shortening/%s/index.html" % outfolder, "w+") as fo:
    fo.write(html)

