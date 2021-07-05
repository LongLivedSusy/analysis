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

    outputdir = './dedxfit_intercalib_barrel/'
    
    # Summer16 MC
    draw(inputfile='./output_bigchunks/Summer16_TotalMC.root',
        hist='hTrkPixelDedx_fromZ_barrel',
        fitfunc='gaus',
        fitrangemin=2.5,
        fitrangemax=3.3,
        outputdir=outputdir,
	outputfile='Summer16_TrkPixelDedx_fromZ_barrel.'+format_c)
    
    # Run2016B
    draw(inputfile='./output_mediumchunks/Run2016B-SingleMuon.root',
        hist='hTrkPixelDedx_fromZ_barrel',
        fitfunc='gaus',
        fitrangemin=2.0,
        fitrangemax=2.8,
        outputdir=outputdir,
	outputfile='Run2016B_TrkPixelDedx_fromZ_barrel.'+format_c)
    
    # Run2016C
    draw(inputfile='./output_mediumchunks/Run2016C-SingleMuon.root',
        hist='hTrkPixelDedx_fromZ_barrel',
        fitfunc='gaus',
        fitrangemin=2.0,
        fitrangemax=2.8,
        outputdir=outputdir,
	outputfile='Run2016C_TrkPixelDedx_fromZ_barrel.'+format_c)
    
    # Run2016D
    draw(inputfile='./output_mediumchunks/Run2016D-SingleMuon.root',
        hist='hTrkPixelDedx_fromZ_barrel',
        fitfunc='gaus',
        fitrangemin=1.9,
        fitrangemax=2.7,
        outputdir=outputdir,
	outputfile='Run2016D_TrkPixelDedx_fromZ_barrel.'+format_c)
    
    # Run2016E
    draw(inputfile='./output_mediumchunks/Run2016E-SingleMuon.root',
        hist='hTrkPixelDedx_fromZ_barrel',
        fitfunc='gaus',
        fitrangemin=1.8,
        fitrangemax=2.6,
        outputdir=outputdir,
	outputfile='Run2016E_TrkPixelDedx_fromZ_barrel.'+format_c)
    
    # Run2016F
    draw(inputfile='./output_mediumchunks/Run2016F-SingleMuon.root',
        hist='hTrkPixelDedx_fromZ_barrel',
        fitfunc='gaus',
        fitrangemin=1.8,
        fitrangemax=2.6,
        outputdir=outputdir,
	outputfile='Run2016F_TrkPixelDedx_fromZ_barrel.'+format_c)
    
    # Run2016G
    draw(inputfile='./output_mediumchunks/Run2016G-SingleMuon.root',
        hist='hTrkPixelDedx_fromZ_barrel',
        fitfunc='gaus',
        fitrangemin=1.7,
        fitrangemax=2.5,
        outputdir=outputdir,
	outputfile='Run2016G_TrkPixelDedx_fromZ_barrel.'+format_c)
    
    # Run2016H
    draw(inputfile='./output_mediumchunks/Run2016H-SingleMuon.root',
        hist='hTrkPixelDedx_fromZ_barrel',
        fitfunc='gaus',
        fitrangemin=1.7,
        fitrangemax=2.5,
        outputdir=outputdir,
	outputfile='Run2016H_TrkPixelDedx_fromZ_barrel.'+format_c)
    
    # Run2017B
    draw(inputfile='./output_mediumchunks/Run2017B-SingleMuon.root',
        hist='hTrkPixelDedx_fromZ_barrel',
        fitfunc='gaus',
        fitrangemin=2.6,
        fitrangemax=3.4,
        outputdir=outputdir,
	outputfile='Run2017B_TrkPixelDedx_fromZ_barrel.'+format_c)
    
    # Run2017C
    draw(inputfile='./output_mediumchunks/Run2017C-SingleMuon.root',
        hist='hTrkPixelDedx_fromZ_barrel',
        fitfunc='gaus',
        fitrangemin=2.0,
        fitrangemax=2.8,
        outputdir=outputdir,
	outputfile='Run2017C_TrkPixelDedx_fromZ_barrel.'+format_c)
    
    # Run2017D
    draw(inputfile='./output_mediumchunks/Run2017D-SingleMuon.root',
        hist='hTrkPixelDedx_fromZ_barrel',
        fitfunc='gaus',
        fitrangemin=2.0,
        fitrangemax=2.8,
        outputdir=outputdir,
	outputfile='Run2017D_TrkPixelDedx_fromZ_barrel.'+format_c)
    
    # Run2017E
    draw(inputfile='./output_mediumchunks/Run2017E-SingleMuon.root',
        hist='hTrkPixelDedx_fromZ_barrel',
        fitfunc='gaus',
        fitrangemin=2.3,
        fitrangemax=3.2,
        outputdir=outputdir,
	outputfile='Run2017E_TrkPixelDedx_fromZ_barrel.'+format_c)
    
    # Run2017F
    draw(inputfile='./output_mediumchunks/Run2017F-SingleMuon.root',
        hist='hTrkPixelDedx_fromZ_barrel',
        fitfunc='gaus',
        fitrangemin=2.1,
        fitrangemax=2.9,
        outputdir=outputdir,
	outputfile='Run2017F_TrkPixelDedx_fromZ_barrel.'+format_c)
    
    # Run2018A
    draw(inputfile='./output_mediumchunks/Run2018A-SingleMuon.root',
        hist='hTrkPixelDedx_fromZ_barrel',
        fitfunc='gaus',
        fitrangemin=2.1,
        fitrangemax=2.9,
        outputdir=outputdir,
	outputfile='Run2018A_TrkPixelDedx_fromZ_barrel.'+format_c)
    
    # Run2018B
    draw(inputfile='./output_mediumchunks/Run2018B-SingleMuon.root',
        hist='hTrkPixelDedx_fromZ_barrel',
        fitfunc='gaus',
        fitrangemin=2.0,
        fitrangemax=2.8,
        outputdir=outputdir,
	outputfile='Run2018B_TrkPixelDedx_fromZ_barrel.'+format_c)
    
    # Run2018C
    draw(inputfile='./output_mediumchunks/Run2018C-SingleMuon.root',
        hist='hTrkPixelDedx_fromZ_barrel',
        fitfunc='gaus',
        fitrangemin=2.0,
        fitrangemax=2.8,
        outputdir=outputdir,
	outputfile='Run2018C_TrkPixelDedx_fromZ_barrel.'+format_c)
    
    # Run2018D
    draw(inputfile='./output_mediumchunks/Run2018D-SingleMuon.root',
        hist='hTrkPixelDedx_fromZ_barrel',
        fitfunc='gaus',
        fitrangemin=1.9,
        fitrangemax=2.7,
        outputdir=outputdir,
	outputfile='Run2018D_TrkPixelDedx_fromZ_barrel.'+format_c)
    
