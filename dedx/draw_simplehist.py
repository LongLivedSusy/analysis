import os as os_
import sys
from ROOT import *
from shared_utils import *

gROOT.SetBatch(True)
gStyle.SetOptStat(True)

saveformat = 'png'
rebin = 1

def main(inputfile, hist, outputdir):
    if not os_.path.exists(inputfile) : print 'No input file exist, quit'; quit()
    infile = TFile(inputfile)
    
    outputdir = outputdir
    if not os_.path.exists(outputdir) : os_.system('mkdir -p '+outputdir)
    
    h = infile.Get(hist)
    
    c = mkcanvas()
    tl = mklegend()
    
    c.cd()
    h.Draw('HIST E SAME')
    c.SaveAs(outputdir+'/'+hist+'.png')


if __name__ == '__main__' :

    hists=[
	'hGenCharginoP',
	'hGenCharginoPt',
	'hGenCharginoEta',
	'hGenCharginoPhi',
	'hGenCharginoMass',
    	'hTrkPixelDedx_charginomatch_barrel',
    	'hTrkPixelDedx_charginomatch_endcap',
    	]
    
    # Run
    for hist in hists:
        #main(inputfile, hist, outputdir)
        main('output_chargino/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-2000.root', hist,'./plots_chargino_mStop2500_mLSP1800_fastsim/')

