import os,sys
from ROOT import *
from glob import glob
from shared_utils import *
from natsort import natsorted,ns

gROOT.SetBatch(1)
gStyle.SetOptStat(True)
#gStyle.SetOptStat(False)
gStyle.SetOptFit(1111)

def draw(inputfile,hist,fitfunc,fitrangemin,fitrangemax,outputdir,outputfile):

    if not os.path.exists(outputdir) : os.system('mkdir -p '+outputdir)

    c = mkcanvas()
    stamp()
    tl = mklegend()
   
    f = TFile(inputfile)
    
    h = f.Get(hist)

    h.Rebin(rebin)
    h.Scale(1.0/h.Integral())
    
    fitres = h.Fit(fitfunc,'S','',fitrangemin,fitrangemax)
    h.Draw('HIST E SAME')
    c.SaveAs(outputdir+'/'+outputfile)
    
if __name__ == '__main__' :

    #format_c = 'pdf'
    format_c = 'png'
    
    rebin = 1
    #rebin = 2

    # Barrel
    outputdir = './dedxfit_smear/'
    
    # Summer16 MC
    draw(inputfile='./output_bigchunks/Summer16_TotalMC.root',
        hist='hTrkPixelDedxScale_fromZ_barrel', # barrel
        fitfunc='gaus',
        fitrangemin=2.1,
        fitrangemax=3.7,
        outputdir=outputdir,
	outputfile='Summer16_TrkPixelDedxScale_fromZ_barrel.'+format_c)
    
    draw(inputfile='./output_bigchunks/Summer16_TotalMC.root',
        hist='hTrkPixelDedxScale_fromZ_endcap', # endcap
        fitfunc='gaus',
        fitrangemin=2.0,
        fitrangemax=3.7,
        outputdir=outputdir,
	outputfile='Summer16_TrkPixelDedxScale_fromZ_endcap.'+format_c)
    
    # Phase0: Run2016
    draw(inputfile='./output_bigchunks/Run2016.root',
        hist='hTrkPixelDedxScale_fromZ_barrel', # barrel 
        fitfunc='gaus',
        fitrangemin=1.8,
        fitrangemax=4.0,
        outputdir=outputdir,
	outputfile='Phase0_TrkPixelDedxScale_fromZ_barrel.'+format_c)
    
    draw(inputfile='./output_bigchunks/Run2016.root',
        hist='hTrkPixelDedxScale_fromZ_endcap', # endcap
        fitfunc='gaus',
        fitrangemin=2.0,
        fitrangemax=3.8,
        outputdir=outputdir,
	outputfile='Phase0_TrkPixelDedxScale_fromZ_endcap.'+format_c)
    
    # Phase1: Run2017-2018
    draw(inputfile='./output_bigchunks/Run2017-2018.root',
        hist='hTrkPixelDedxScale_fromZ_barrel', # barrel
        fitfunc='gaus',
        fitrangemin=1.8,
        fitrangemax=4.0,
        outputdir=outputdir,
	outputfile='Phase1_TrkPixelDedxScale_fromZ_barrel.'+format_c)
    
    draw(inputfile='./output_bigchunks/Run2017-2018.root',
        hist='hTrkPixelDedxScale_fromZ_endcap', # endcap
        fitfunc='gaus',
        fitrangemin=2.0,
        fitrangemax=3.8,
        outputdir=outputdir,
	outputfile='Phase1_TrkPixelDedxScale_fromZ_endcap.'+format_c)
