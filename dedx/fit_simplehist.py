import os,sys
from ROOT import *
from glob import glob
from shared_utils import *
from natsort import natsorted,ns

gROOT.SetBatch(1)
gStyle.SetOptStat(True)
#gStyle.SetOptStat(False)
gStyle.SetOptFit(1111)

#format_c = 'pdf'
format_c = 'png'

#rebin = 1
rebin = 2

def draw(inputfile,hist,fitfunc,fitrangemin,fitrangemax,outputdir,outputfile):

    if not os.path.exists(outputdir) : os.system('mkdir -p '+outputdir)

    c = mkcanvas()
    stamp()
    tl = mklegend()
   
    f = TFile(inputfile)
    
    h = f.Get(hist)

    h.Rebin(rebin)
    
    fitres = h.Fit(fitfunc,'S','',fitrangemin,fitrangemax)
    h.Draw('HIST E SAME')
    #c.SaveAs(outputdir+'/'+hist+'.'+format_c)
    c.SaveAs(outputdir+'/'+outputfile)
    
if __name__ == '__main__' :

    outputdir = './FitDedx_chipm/'
    '''
    # Fullsim mStop1300_mLSP1
    draw(inputfile='./output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1_TuneCUETP8M1.root',
        hist='hTrkPixelDedx_charginomatch_barrel',
        fitfunc='landau',
        fitrangemin=2.5,
        fitrangemax=3.5,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop1300_mLSP1_barrel.'+format_c)

    draw(inputfile='./output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1_TuneCUETP8M1.root',
        hist='hTrkPixelDedx_charginomatch_endcap',
        fitfunc='landau',
        fitrangemin=2.5,
        fitrangemax=3.5,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop1300_mLSP1_endcap.'+format_c)

    # Fastsim mStop1300_mLSP1
    draw(inputfile='./output_chargino/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-1.root',
        hist='hTrkPixelDedx_charginomatch_barrel',
        fitfunc='landau',
        fitrangemin=4.0,
        fitrangemax=5.0,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop1300_mLSP1_barrel_fastsim.'+format_c)

    draw(inputfile='./output_chargino/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-1.root',
        hist='hTrkPixelDedx_charginomatch_endcap',
        fitfunc='landau',
        fitrangemin=4.0,
        fitrangemax=5.0,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop1300_mLSP1_endcap_fastsim.'+format_c)

    # Fullsim mStop1300_mLSP50
    draw(inputfile='./output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-50_TuneCUETP8M1.root',
        hist='hTrkPixelDedx_charginomatch_barrel',
        fitfunc='landau',
        fitrangemin=2.5,
        fitrangemax=3.5,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop1300_mLSP50_barrel.'+format_c)

    draw(inputfile='./output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-50_TuneCUETP8M1.root',
        hist='hTrkPixelDedx_charginomatch_endcap',
        fitfunc='landau',
        fitrangemin=2.5,
        fitrangemax=3.5,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop1300_mLSP50_endcap.'+format_c)

    # Fastsim mStop1300_mLSP50
    draw(inputfile='./output_chargino/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-50.root',
        hist='hTrkPixelDedx_charginomatch_barrel',
        fitfunc='landau',
        fitrangemin=2.8,
        fitrangemax=3.6,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop1300_mLSP50_barrel_fastsim.'+format_c)

    draw(inputfile='./output_chargino/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-50.root',
        hist='hTrkPixelDedx_charginomatch_endcap',
        fitfunc='landau',
        fitrangemin=3.0,
        fitrangemax=3.8,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop1300_mLSP50_endcap_fastsim.'+format_c)

    # Fullsim mStop1300_mLSP200
    draw(inputfile='./output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-200_TuneCUETP8M1.root',
        hist='hTrkPixelDedx_charginomatch_barrel',
        fitfunc='landau',
        fitrangemin=2.5,
        fitrangemax=3.5,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop1300_mLSP200_barrel.'+format_c)

    draw(inputfile='./output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-200_TuneCUETP8M1.root',
        hist='hTrkPixelDedx_charginomatch_endcap',
        fitfunc='landau',
        fitrangemin=2.5,
        fitrangemax=3.5,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop1300_mLSP200_endcap.'+format_c)

    # Fastsim mStop1300_mLSP200
    draw(inputfile='./output_chargino/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-200.root',
        hist='hTrkPixelDedx_charginomatch_barrel',
        fitfunc='landau',
        fitrangemin=2.8,
        fitrangemax=3.4,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop1300_mLSP200_barrel_fastsim.'+format_c)

    draw(inputfile='./output_chargino/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-200.root',
        hist='hTrkPixelDedx_charginomatch_endcap',
        fitfunc='landau',
        fitrangemin=2.8,
        fitrangemax=3.4,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop1300_mLSP200_endcap_fastsim.'+format_c)

    # Fullsim mStop1300_mLSP400
    draw(inputfile='./output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-400_TuneCUETP8M1.root',
        hist='hTrkPixelDedx_charginomatch_barrel',
        fitfunc='landau',
        fitrangemin=2.5,
        fitrangemax=4.0,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop1300_mLSP400_barrel.'+format_c)

    draw(inputfile='./output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-400_TuneCUETP8M1.root',
        hist='hTrkPixelDedx_charginomatch_endcap',
        fitfunc='landau',
        fitrangemin=2.5,
        fitrangemax=4.0,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop1300_mLSP400_endcap.'+format_c)

    # Fastsim mStop1300_mLSP400
    draw(inputfile='./output_chargino/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-400.root',
        hist='hTrkPixelDedx_charginomatch_barrel',
        fitfunc='landau',
        fitrangemin=2.6,
        fitrangemax=4.0,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop1300_mLSP400_barrel_fastsim.'+format_c)

    draw(inputfile='./output_chargino/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-400.root',
        hist='hTrkPixelDedx_charginomatch_endcap',
        fitfunc='landau',
        fitrangemin=2.6,
        fitrangemax=4.0,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop1300_mLSP400_endcap_fastsim.'+format_c)

    # Fullsim mStop1300_mLSP600
    draw(inputfile='./output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-600_TuneCUETP8M1.root',
        hist='hTrkPixelDedx_charginomatch_barrel',
        fitfunc='landau',
        fitrangemin=2.6,
        fitrangemax=5.0,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop1300_mLSP600_barrel.'+format_c)

    draw(inputfile='./output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-600_TuneCUETP8M1.root',
        hist='hTrkPixelDedx_charginomatch_endcap',
        fitfunc='landau',
        fitrangemin=2.4,
        fitrangemax=6.6,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop1300_mLSP600_endcap.'+format_c)

    # Fastsim mStop1300_mLSP600
    draw(inputfile='./output_chargino/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-600.root',
        hist='hTrkPixelDedx_charginomatch_barrel',
        fitfunc='landau',
        fitrangemin=2.6,
        fitrangemax=5.0,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop1300_mLSP600_barrel_fastsim.'+format_c)

    draw(inputfile='./output_chargino/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-600.root',
        hist='hTrkPixelDedx_charginomatch_endcap',
        fitfunc='landau',
        fitrangemin=2.8,
        fitrangemax=5.0,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop1300_mLSP600_endcap_fastsim.'+format_c)

    # Fullsim mStop1300_mLSP800
    draw(inputfile='./output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-800_TuneCUETP8M1.root',
        hist='hTrkPixelDedx_charginomatch_barrel',
        fitfunc='landau',
        fitrangemin=3.0,
        fitrangemax=6.0,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop1300_mLSP800_barrel.'+format_c)

    draw(inputfile='./output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-800_TuneCUETP8M1.root',
        hist='hTrkPixelDedx_charginomatch_endcap',
        fitfunc='landau',
        fitrangemin=2.6,
        fitrangemax=6.0,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop1300_mLSP800_endcap.'+format_c)

    # Fastsim mStop1300_mLSP800
    draw(inputfile='./output_chargino/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-800.root',
        hist='hTrkPixelDedx_charginomatch_barrel',
        fitfunc='landau',
        fitrangemin=3.0,
        fitrangemax=6.0,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop1300_mLSP800_barrel_fastsim.'+format_c)

    draw(inputfile='./output_chargino/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-800.root',
        hist='hTrkPixelDedx_charginomatch_endcap',
        fitfunc='landau',
        fitrangemin=2.8,
        fitrangemax=6.0,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop1300_mLSP800_endcap_fastsim.'+format_c)

    # Fullsim mStop1300_mLSP1000
    draw(inputfile='./output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1.root',
        hist='hTrkPixelDedx_charginomatch_barrel',
        fitfunc='landau',
        fitrangemin=3.0,
        fitrangemax=6.0,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop1300_mLSP1000_barrel.'+format_c)

    draw(inputfile='./output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1.root',
        hist='hTrkPixelDedx_charginomatch_endcap',
        fitfunc='landau',
        fitrangemin=2.6,
        fitrangemax=6.6,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop1300_mLSP1000_endcap.'+format_c)

    # Fastsim mStop1300_mLSP1000
    draw(inputfile='./output_chargino/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-1000.root',
        hist='hTrkPixelDedx_charginomatch_barrel',
        fitfunc='landau',
        fitrangemin=3.0,
        fitrangemax=6.6,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop1300_mLSP1000_barrel_fastsim.'+format_c)

    draw(inputfile='./output_chargino/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-1000.root',
        hist='hTrkPixelDedx_charginomatch_endcap',
        fitfunc='landau',
        fitrangemin=3.0,
        fitrangemax=6.6,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop1300_mLSP1000_endcap_fastsim.'+format_c)
    '''
    # Fullsim mStop2500_mLSP1200
    draw(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp1200/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1200_TuneCUETP8M1.root',
        hist='hTrkPixelDedx_charginomatch_barrel',
        fitfunc='landau',
        fitrangemin=2.5,
        fitrangemax=6.0,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop2500_mLSP1200_barrel.'+format_c)

    draw(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp1200/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1200_TuneCUETP8M1.root',
        hist='hTrkPixelDedx_charginomatch_endcap',
        fitfunc='landau',
        fitrangemin=2.6,
        fitrangemax=6.6,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop2500_mLSP1200_endcap.'+format_c)

    # Fastsim mStop2500_mLSP1200
    draw(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp1200/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1200to2000.root',
        hist='hTrkPixelDedx_charginomatch_barrel',
        fitfunc='landau',
        fitrangemin=2.8,
        fitrangemax=6.6,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop2500_mLSP1200_barrel_fastsim.'+format_c)

    draw(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp1200/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1200to2000.root',
        hist='hTrkPixelDedx_charginomatch_endcap',
        fitfunc='landau',
        fitrangemin=3.0,
        fitrangemax=6.6,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop2500_mLSP1200_endcap_fastsim.'+format_c)

    # Fullsim mStop2500_mLSP1400
    draw(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp1400/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1400_TuneCUETP8M1.root',
        hist='hTrkPixelDedx_charginomatch_barrel',
        fitfunc='landau',
        fitrangemin=3.0,
        fitrangemax=6.0,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop2500_mLSP1400_barrel.'+format_c)

    draw(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp1400/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1400_TuneCUETP8M1.root',
        hist='hTrkPixelDedx_charginomatch_endcap',
        fitfunc='landau',
        fitrangemin=2.6,
        fitrangemax=6.6,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop2500_mLSP1400_endcap.'+format_c)

    # Fastsim mStop2500_mLSP1400
    draw(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp1400/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1200to2000.root',
        hist='hTrkPixelDedx_charginomatch_barrel',
        fitfunc='landau',
        fitrangemin=3.0,
        fitrangemax=6.6,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop2500_mLSP1400_barrel_fastsim.'+format_c)

    draw(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp1400/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1200to2000.root',
        hist='hTrkPixelDedx_charginomatch_endcap',
        fitfunc='landau',
        fitrangemin=3.0,
        fitrangemax=6.6,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop2500_mLSP1400_endcap_fastsim.'+format_c)

    # Fullsim mStop2500_mLSP1600
    draw(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp1600/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1600_TuneCUETP8M1.root',
        hist='hTrkPixelDedx_charginomatch_barrel',
        fitfunc='landau',
        fitrangemin=3.0,
        fitrangemax=8.0,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop2500_mLSP1600_barrel.'+format_c)

    draw(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp1600/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1600_TuneCUETP8M1.root',
        hist='hTrkPixelDedx_charginomatch_endcap',
        fitfunc='landau',
        fitrangemin=3.0,
        fitrangemax=6.6,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop2500_mLSP1600_endcap.'+format_c)

    # Fastsim mStop2500_mLSP1600
    draw(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp1600/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1200to2000.root',
        hist='hTrkPixelDedx_charginomatch_barrel',
        fitfunc='landau',
        fitrangemin=3.0,
        fitrangemax=8.0,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop2500_mLSP1600_barrel_fastsim.'+format_c)

    draw(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp1600/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1200to2000.root',
        hist='hTrkPixelDedx_charginomatch_endcap',
        fitfunc='landau',
        fitrangemin=3.0,
        fitrangemax=6.6,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop2500_mLSP1600_endcap_fastsim.'+format_c)

    # Fullsim mStop2500_mLSP1800
    draw(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp1800/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1800_TuneCUETP8M1.root',
        hist='hTrkPixelDedx_charginomatch_barrel',
        fitfunc='landau',
        fitrangemin=3.0,
        fitrangemax=10.0,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop2500_mLSP1800_barrel.'+format_c)

    draw(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp1800/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1800_TuneCUETP8M1.root',
        hist='hTrkPixelDedx_charginomatch_endcap',
        fitfunc='landau',
        fitrangemin=2.6,
        fitrangemax=10.0,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop2500_mLSP1800_endcap.'+format_c)

    # Fastsim mStop2500_mLSP1800
    draw(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp1800/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1200to2000.root',
        hist='hTrkPixelDedx_charginomatch_barrel',
        fitfunc='landau',
        fitrangemin=3.0,
        fitrangemax=10.0,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop2500_mLSP1800_barrel_fastsim.'+format_c)

    draw(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp1800/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1200to2000.root',
        hist='hTrkPixelDedx_charginomatch_endcap',
        fitfunc='landau',
        fitrangemin=3.0,
        fitrangemax=10.0,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop2500_mLSP1800_endcap_fastsim.'+format_c)

    # Fullsim mStop2500_mLSP2000
    draw(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp2000/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-2000_TuneCUETP8M1.root',
        hist='hTrkPixelDedx_charginomatch_barrel',
        fitfunc='landau',
        fitrangemin=3.0,
        fitrangemax=100,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop2500_mLSP2000_barrel.'+format_c)

    draw(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp2000/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-2000_TuneCUETP8M1.root',
        hist='hTrkPixelDedx_charginomatch_endcap',
        fitfunc='landau',
        fitrangemin=2.6,
        fitrangemax=10.0,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop2500_mLSP2000_endcap.'+format_c)

    # Fastsim mStop2500_mLSP2000
    draw(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp2000/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1200to2000.root',
        hist='hTrkPixelDedx_charginomatch_barrel',
        fitfunc='landau',
        fitrangemin=3.0,
        fitrangemax=10.0,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop2500_mLSP2000_barrel_fastsim.'+format_c)

    draw(inputfile='./output_smallchunks_T2btLL_mstop2500_mlsp2000/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1200to2000.root',
        hist='hTrkPixelDedx_charginomatch_endcap',
        fitfunc='landau',
        fitrangemin=3.0,
        fitrangemax=10.0,
        outputdir=outputdir,
	outputfile='TrkPixelDedx_chipm_mStop2500_mLSP2000_endcap_fastsim.'+format_c)

