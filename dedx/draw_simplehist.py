import os as os_
import sys
from ROOT import *
from shared_utils import *

gROOT.SetBatch(True)
gStyle.SetOptStat(True)

saveformat = 'png'
rebin = 1

def main(inputfile, hist, outputdir):
    #infile = TFile('output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1_TuneCUETP8M1.root')
    infile = TFile(inputfile)
    
    h = infile.Get(hist)
    
    c = mkcanvas()
    tl = mklegend()
    
    c.cd()
    h.Draw('HIST E SAME')
    #stamp()
    c.SaveAs(outputdir+'/'+hist+'.png')


if __name__ == '__main__' :

    #outputdir = './plots_chargino_mStop1300_mLSP1/'
    #outputdir = './plots_chargino_mStop1300_mLSP50/'
    #outputdir = './plots_chargino_mStop1300_mLSP200/'
    #outputdir = './plots_chargino_mStop1300_mLSP1100/'
    #outputdir = './plots_chargino_mStop2500_mLSP1200/'
    outputdir = './plots_chargino_mStop2500_mLSP1400/'
    if not os_.path.exists(outputdir) : os_.system('mkdir -p '+outputdir)
    
    #inputfile = 'output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1_TuneCUETP8M1.root'
    #inputfile = 'output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-50_TuneCUETP8M1.root'
    #inputfile = 'output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-200_TuneCUETP8M1.root'
    #inputfile = 'output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1100_TuneCUETP8M1.root'
    #inputfile = 'output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1200_TuneCUETP8M1.root'
    inputfile = 'output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1400_TuneCUETP8M1.root'
    
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
        main(inputfile, hist, outputdir)

