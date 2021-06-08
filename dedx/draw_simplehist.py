import os as os_
import sys
from glob import glob
from ROOT import *
from shared_utils import *

gROOT.SetBatch(True)
gStyle.SetOptStat(True)

format_c = 'png'
rebin = 1

def main(inputfile, hist, outputdir, outputfile):
    if not os_.path.exists(inputfile) : print 'Cannot found input file : {}, quit'.format(inputfile); quit()
    
    infile = TFile(inputfile)

    outputdir = outputdir
    if not os_.path.exists(outputdir) : os_.system('mkdir -p '+outputdir)
   
    h = infile.Get(hist)
    
    c = mkcanvas()
    tl = mklegend()
    
    c.cd()
    h.Draw('HIST E SAME')
    c.SaveAs(outputdir+'/'+outputfile)


if __name__ == '__main__' :

    hists=[
	'hGenCharginoP',
	'hGenCharginoPt',
	'hGenCharginoEta',
	'hGenCharginoPhi',
	'hGenCharginoMass',
	'hGenCharginoP_trackmatch',
	'hGenCharginoPt_trackmatch',
	'hGenCharginoEta_trackmatch',
	'hGenCharginoPhi_trackmatch',
	'hTrkP_charginomatch',
	'hTrkPt_charginomatch',
	'hTrkEta_charginomatch',
	'hTrkPhi_charginomatch',
    	'hTrkPixelDedx_charginomatch',
    	'hTrkPixelDedx_charginomatch_SR',
    	'hTrkPixelDedx_charginomatch_barrel',
    	'hTrkPixelDedx_charginomatch_endcap',
    	'hTrkPixelDedxScale_charginomatch_barrel',
    	'hTrkPixelDedxScale_charginomatch_endcap',
    	'hTrkPixelDedxScale_charginomatch_SR',
    	]
    
    # Run
    for hist in hists:
        main(inputfile='./output_smallchunks_T2btLL_mstop1300_mlsp200/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-200_TuneCUETP8M1.root', hist=hist, outputdir='./plots_chargino_mStop1300_mLSP200/', outputfile='RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-200_'+hist+'.'+format_c)
        #main(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp1200/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1200_TuneCUETP8M1.root', hist=hist, outputdir='./plots_chargino_mStop2500_mLSP1200/', outputfile='RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1200_'+hist+'.'+format_c)
        #main(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp1400/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1400_TuneCUETP8M1.root', hist=hist, outputdir='./plots_chargino_mStop2500_mLSP1400/', outputfile='RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1400_'+hist+'.'+format_c)
        #main(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp1600/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1600_TuneCUETP8M1.root', hist=hist, outputdir='./plots_chargino_mStop2500_mLSP1600/', outputfile='RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1600_'+hist+'.'+format_c)
        #main(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp1800/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1800_TuneCUETP8M1.root', hist=hist, outputdir='./plots_chargino_mStop2500_mLSP1800/', outputfile='RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1800_'+hist+'.'+format_c)
        #main(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp2000/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-2000_TuneCUETP8M1.root', hist=hist, outputdir='./plots_chargino_mStop2500_mLSP2000/', outputfile='RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-2000_'+hist+'.'+format_c)
        
        #main(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp1200/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1200to2000.root', hist=hist, outputdir='./plots_chargino_mStop2500_mLSP1200_fastsim/', outputfile=hist+'.'+format_c)
        #main(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp1400/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1200to2000.root', hist=hist, outputdir='./plots_chargino_mStop2500_mLSP1400_fastsim/', outputfile=hist+'.'+format_c)
        #main(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp1600/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1200to2000.root', hist=hist, outputdir='./plots_chargino_mStop2500_mLSP1600_fastsim/', outputfile=hist+'.'+format_c)
        #main(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp1800/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1200to2000.root', hist=hist, outputdir='./plots_chargino_mStop2500_mLSP1800_fastsim/', outputfile=hist+'.'+format_c)
        #main(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp2000/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1200to2000.root', hist=hist, outputdir='./plots_chargino_mStop2500_mLSP2000_fastsim/', outputfile=hist+'.'+format_c)
