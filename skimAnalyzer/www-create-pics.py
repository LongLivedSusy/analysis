#!/bin/env python
import glob
import os
#import ddbg_eventloop
from pygments import highlight
from pygments import lexers
from pygments.formatters import HtmlFormatter
from optparse import OptionParser

parser = OptionParser()
(options, args) = parser.parse_args()

if len(args)>0:
    configurations = args
else:
    print "Run with \n$ ./www-create-pics.py path/to/folder/to/upload"
    quit()

def conv_python_to_html(filename):
    
    lex = lexers.get_lexer_by_name("python") 
    code = ""
    
    formatter = HtmlFormatter(full=True, style="colorful")
    
    with open(filename, "r") as fin:
        code = fin.read()
    
    with open(filename.replace(".py", ".html"), "w") as fout:
        highlight(code, lex, formatter, outfile=fout)


for configuration in configurations:

    os.system("mkdir -p ~/www/DisappearingTracks/%s" % configuration)
    os.system("cp -r %s_plots/* ~/www/DisappearingTracks/%s/" % (configuration, configuration))
    #os.system("cp %s/taginfo.html ~/www/DisappearingTracks/%s/" % (configuration, configuration))
    #os.system("cp %s/skimmer.py ~/www/DisappearingTracks/%s/" % (configuration, configuration))
    
    #conv_python_to_html("/afs/desy.de/user/k/kutznerv/www/DisappearingTracks/%s/skimmer.py" % configuration)
    
    for subfolder in glob.glob("/afs/desy.de/user/k/kutznerv/www/DisappearingTracks/%s/*" % configuration):
        for subsubfolder in sorted(glob.glob(subfolder + "/*")):
    
            print subsubfolder
            
            if not os.path.isdir(subsubfolder):
                continue
            
            html = ""
            region_name = subsubfolder.split("/")[-1]
            
            html += "<h1><a href=..>..</a>/%s</h1>" % region_name
            
            #if region_name in ddbg_eventloop.event_selections["analysis"]:
            #    cuts = ddbg_eventloop.event_selections["analysis"][region_name]
            #    html += "<p>Event cuts of this region: <tt>%s</tt><br> <a href=../taginfo.html>track tag</a>, <a href=../skimmer.html>ntuple skimmer</a><br>" % (cuts)
                
            #for datamc in ["Run2016", "Summer16"]:
            
            #if len(glob.glob(subfolder + "/%s*png")) > 0:
            
                #if "Run201" in datamc:
                #    html += "<h2>Run2016 data:</h2>"
                #if "Summer16" in datamc:
                #    html += "<h2>MC:</h2>"
            
                            
            for ifile in sorted(glob.glob(subsubfolder + "/*.png")):
            
                print ifile
                outfile = ifile.split("/")[-1]
                html += """<a href="%s"><img src="%s" width="400"></a>""" % (outfile, outfile)
                #html += """<a href="%s"><object data="%s" type="application/x-pdf" width="400"></a>""" % (outfile, outfile)
                #<object data="YourFile.pdf" type="application/x-pdf" title="SamplePdf" width="500" height="720">
                            
            with open("%s/index.html" % subsubfolder, "w+") as fo:
                fo.write(html)

