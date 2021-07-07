import os,sys
#from ROOT import *
from glob import glob
import ROOT as rt
import CMS_lumi, tdrstyle
import array

#set the tdr style
tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12

H_ref = 600; 
W_ref = 800; 
W = W_ref
H = H_ref

# 
# Simple example of macro: plot with CMS name and lumi text
#  (this script does not pretend to work in all configurations)
# iPeriod = 1*(0/1 7 TeV) + 2*(0/1 8 TeV)  + 4*(0/1 13 TeV) 
# For instance: 
#               iPeriod = 3 means: 7 TeV + 8 TeV
#               iPeriod = 7 means: 7 TeV + 8 TeV + 13 TeV 
#               iPeriod = 0 means: free form (uses lumi_sqrtS)
# Initiated by: Gautier Hamel de Monchenault (Saclay)
# Translated in Python by: Joshua Hardenbrook (Princeton)
# Updated by:   Dinko Ferencek (Rutgers)
#

iPeriod = 3

# references for T, B, L, R
T = 0.08*H_ref
B = 0.12*H_ref
L = 0.12*W_ref
R = 0.04*W_ref

rt.gROOT.SetBatch(1)
rt.gStyle.SetOptStat(False)
#rt.gStyle.SetOptFit(1111)

#format_c = 'pdf'
format_c = 'png'

#outputdir = './plots/T2bt_mStop1300_mLSP1'
#outputdir = './plots/T2bt_mStop1300_mLSP50'
#outputdir = './plots/T2bt_mStop1300_mLSP200'
#outputdir = './plots/T2bt_mStop1300_mLSP1100'
outputdir = './plots/T2bt_mStop1300_mLSP1100_dEdx'
#outputdir = './plots/T1qqqq_mGluino2200_mLSP2000_dEdx'
#outputdir = './plots/T1qqqq_mGluino1300_mLSP1100_dEdx'

#rebin = 1
rebin = 5
#rebin = 10
#rebin = 20
    
if not os.path.exists(outputdir) : os.system('mkdir -p '+outputdir)
    
#f1 = rt.TFile('./output_test/RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq-LLChipm_ctau-200_TuneCP2_13TeV-madgraphMLM-pythia8_mGluino2200_mLSP2000.root')
#f1 = rt.TFile('./output_test/RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq-LLChipm_ctau-200_TuneCP2_13TeV-madgraphMLM-pythia8_mGluino1300_mLSP1100.root')

f1 = rt.TFile('./output_smallchunks_localrun/T2bt_mStop1300_mLSP1100/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1100_TuneCUETP8M1.root')
f2 = rt.TFile('./output_smallchunks_localrun/T2bt_mStop1300_mLSP1100/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-1100and300.root')

hists=[
    #'hGenGluino',
    #'hGenStopMass',
    #'hGenLSPMass',
    #'hGenCharginoP',
    #'hGenCharginoPt',
    #'hGenCharginoEta',
    #'hGenCharginoPhi',
    #    
    #'hTrkP_charginomatch',
    #'hTrkPt_charginomatch',
    #'hTrkEta_charginomatch',
    #'hTrkPhi_charginomatch',

    'hTrkPixelDedx_charginomatch_barrel',
    'hTrkPixelDedxCalib_charginomatch_barrel',
    'hTrkStripsDedx_charginomatch_barrel',
	
    'hTrkPixelDedx_charginomatch_endcap',
    'hTrkPixelDedxCalib_charginomatch_endcap',
    'hTrkStripsDedx_charginomatch_endcap',

    # Muon
    #'hMuP',
    #'hMuPt',
    #'hMuEta',
    #'hMuPhi',
    #
    #'hMuP_genmatch',
    #'hMuPt_genmatch',
    #'hMuEta_genmatch',
    #'hMuPhi_genmatch',
    #
    #'hTrkP_tightmumatch',
    #'hTrkP_tightmumatch_barrel',
    #'hTrkP_tightmumatch_endcap',

    #'hTrkP_tightgenmumatch',
    #'hTrkP_tightgenmumatch_barrel',
    #'hTrkP_tightgenmumatch_endcap',

    #'hTrkPt_tightmumatch',
    #'hTrkPt_tightmumatch_barrel',
    #'hTrkPt_tightmumatch_endcap',
    #
    ##'hTrkEta_tightmumatch',
    ##'hTrkEta_tightmumatch_barrel',
    ##'hTrkEta_tightmumatch_endcap',

    #'hTrkPt_tightgenmumatch',
    #'hTrkPt_tightgenmumatch_barrel',
    #'hTrkPt_tightgenmumatch_endcap',
    #
    ##'hTrkEta_tightgenmumatch',
    ##'hTrkEta_tightgenmumatch_barrel',
    ##'hTrkEta_tightgenmumatch_endcap',

    #'hTrkPixelDedx_tightmumatch',
    #'hTrkPixelDedx_tightmumatch_barrel',
    #'hTrkPixelDedx_tightmumatch_endcap',
    #'hTrkPixelDedxCalib_tightmumatch',
    #'hTrkPixelDedxCalib_tightmumatch_barrel',
    #'hTrkPixelDedxCalib_tightmumatch_endcap',

    'hTrkPixelDedx_tightgenmumatch',
    'hTrkPixelDedx_tightgenmumatch_barrel',
    'hTrkPixelDedx_tightgenmumatch_endcap',
    'hTrkPixelDedxCalib_tightgenmumatch',
    'hTrkPixelDedxCalib_tightgenmumatch_barrel',
    'hTrkPixelDedxCalib_tightgenmumatch_endcap',

    #'hTrkStripsDedx_tightmumatch',
    #'hTrkStripsDedx_tightmumatch_barrel',
    #'hTrkStripsDedx_tightmumatch_endcap',

    'hTrkStripsDedx_tightgenmumatch',
    'hTrkStripsDedx_tightgenmumatch_barrel',
    'hTrkStripsDedx_tightgenmumatch_endcap',
    ]

# Run
for hist in hists:
    
    print 'Drawing hist : ',hist

    canvas = rt.TCanvas("c","c",50,50,W,H)
    canvas.SetFillColor(0)
    canvas.SetBorderMode(0)
    canvas.SetFrameFillStyle(0)
    canvas.SetFrameBorderMode(0)
    canvas.SetLeftMargin( L/W )
    canvas.SetRightMargin( R/W )
    canvas.SetTopMargin( T/H )
    canvas.SetBottomMargin( B/H )
    canvas.SetTickx(0)
    canvas.SetTicky(0)
    
    tl = rt.TLegend(0.6,0.7,0.85,0.9)

    #c.SetLogy()
    h1 = f1.Get(hist) 
    h1.Scale(1.0/h1.Integral())

    h2 = f2.Get(hist) 
    h2.Scale(1.0/h2.Integral())

    h1.Rebin(rebin)
    h2.Rebin(rebin)
    
    h1.SetLineColor(rt.kBlue)
    h2.SetLineColor(rt.kRed)
    #h1.SetFillStyle(3002)
    #h1.SetFillColor(kBlue)
    
    rp = rt.TRatioPlot(h1,h2)
    rp.SetH1DrawOpt('E')
    rp.SetH2DrawOpt('E')
    rp.Draw()
    rp.GetUpperPad().SetLogy()
    rp.GetUpperRefYaxis().SetTitle("Normalized");
    #rp.GetUpperRefYaxis().SetRangeUser(0,0.1);
    #rp.GetLowerRefXaxis().SetTitle("MeV");
    rp.GetLowerRefYaxis().SetTitle("Fullsim/Fastsim");
    #rp.GetLowerRefYaxis().SetRangeUser(0,2);
    rp.GetLowerRefGraph().SetMinimum(0);
    rp.GetLowerRefGraph().SetMaximum(2);
   
    tl.AddEntry(h1,'SMS-T2btLL Fullsim','lE')
    tl.AddEntry(h2,'SMS-T2btLL FastSim','lE')
    tl.Draw()

    canvas.Update()
    canvas.Print(outputdir+'/RatioPlot_'+hist+'.'+format_c)
    canvas.Close()
