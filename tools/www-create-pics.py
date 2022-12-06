#!/bin/env python
import glob
import os
from optparse import OptionParser
from os.path import expanduser

parser = OptionParser()
(options, args) = parser.parse_args()

if len(args)>0:
    configurations = args
else:
    print "Run with \n$ ./www-create-pics.py www-subfolder path/to/folder/to/upload"
    quit()

label = args[0]

outfolder = args[-1].split("/")[-1]
if outfolder[-1] == "/":
    outfolder = outfolder[:-1]

os.system("mkdir -p ~/www/%s/%s" % (label, outfolder))
os.system("cp -r %s/* ~/www/%s/%s/" % (outfolder, label, outfolder))

html = ""
                
for ifile in sorted(glob.glob(outfolder + "/*.pdf")):
    print ifile
    outfile = ifile.split("/")[-1]
    
    os.system("convert ~/www/%s/%s/%s ~/www/%s/%s/%s" % (label, outfolder, outfile, label, outfolder, outfile.replace(".pdf", ".png")))
        
    html += """
    <table width="400" class="tg" style="display: inline-block;">
    <thead>
      <tr>
        <th class="tg-0lax"><center>%s</center><br><a href="%s"><img src="%s" width="100%%"></a></th>
      </tr>
    </thead>
    </table>
    """ % (outfile.replace(".pdf", ""), outfile, outfile.replace(".pdf", ".png"))
    
    
home = expanduser("~")

with open("%s/www/%s/%s/index.html" % (home, label, outfolder), "w+") as fo:
    fo.write(html)

