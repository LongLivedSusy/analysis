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

    outputdir = './dedxfit_intercalib_proton/'
    
    # Summer16 MC
    draw(inputfile='./SV_rootfiles/vertex_Summer16_T2bt.root',
        hist='dedxpixel_good_proton',
        fitfunc='gaus',
        fitrangemin=2.4,
        fitrangemax=3.2,
        outputdir=outputdir,
	outputfile='Summer16_T2bt_dedxpixel_proton.'+format_c)
    
    # Fall17 MC
    draw(inputfile='./SV_rootfiles/vertex_DYJetsToLL_M-50_Fall17.root',
        hist='dedxpixel_good_proton',
        fitfunc='gaus',
        fitrangemin=2.6,
        fitrangemax=3.1,
        outputdir=outputdir,
	outputfile='Fall17_DYJetsToLL_M-50_dedxpixel_proton.'+format_c)
    
    # Run2016B
    draw(inputfile='./SV_rootfiles/vertex_Run2016B_SingleElectron.root',
        hist='dedxpixel_good_proton',
        fitfunc='gaus',
        fitrangemin=2.0,
        fitrangemax=2.6,
        outputdir=outputdir,
	outputfile='Run2016B_dedxpixel_proton.'+format_c)
    
    # Run2016G
    draw(inputfile='./SV_rootfiles/vertex_Run2016G_SingleElectron.root',
        hist='dedxpixel_good_proton',
        fitfunc='gaus',
        fitrangemin=1.7,
        fitrangemax=2.4,
        outputdir=outputdir,
	outputfile='Run2016G_dedxpixel_proton.'+format_c)
    
    # Run2017F
    draw(inputfile='./SV_rootfiles/vertex_Run2017F_SingleElectron.root',
        hist='dedxpixel_good_proton',
        fitfunc='gaus',
        fitrangemin=1.8,
        fitrangemax=2.7,
        outputdir=outputdir,
	outputfile='Run2017F_dedxpixel_proton.'+format_c)
    
    # Run2018C
    draw(inputfile='./SV_rootfiles/vertex_Run2018C_EGamma.root',
        hist='dedxpixel_good_proton',
        fitfunc='gaus',
        fitrangemin=1.9,
        fitrangemax=2.6,
        outputdir=outputdir,
	outputfile='Run2018C_dedxpixel_proton.'+format_c)
    
