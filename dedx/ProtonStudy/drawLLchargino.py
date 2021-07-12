import os as os_
import sys
from ROOT import *
from shared_utils import *
gROOT.SetBatch(1)
gStyle.SetOptStat(0)
TH1.SetDefaultSumw2()

plotDir = 'plotsLLchargino'
if not os_.path.exists(plotDir) :
    os_.system('mkdir -p '+plotDir)

fsim = TFile('./LLchargino/SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root')
ffastsim = TFile('./LLchargino/SUS-RunIISummer15GS-00734_T2btLLFastSim.root')
fsim.ls()

#rebin = 1
rebin = 5
logscale = True

plots = [
	    ['P_chargino','(P | chargino) [GeV]'],
	    ['pt_chargino','(pt | chargino) [GeV]'],
	    ['eta_chargino','(eta | chargino)'],
	    ['phi_chargino','(phi | chargino)'],
	    
	    ['P_chargino_trackmatch','(P | chargino) [GeV]'],
	    ['pt_chargino_trackmatch','(pt | chargino) [GeV]'],
	    ['eta_chargino_trackmatch','(eta | chargino)'],
	    ['phi_chargino_trackmatch','(phi | chargino)'],
	    
	    ['P_chargino_trackmatch_pt1200','(P | chargino) [GeV]'],
	    ['pt_chargino_trackmatch_pt1200','(pt | chargino) [GeV]'],
	    ['eta_chargino_trackmatch_pt1200','(eta | chargino)'],
	    ['phi_chargino_trackmatch_pt1200','(phi | chargino)'],
	    
	    
	    ['P_track','(P | track) [GeV]'],
	    ['pt_track','(pt | track) [GeV]'],
	    ['eta_track','(eta | track)'],
	    ['phi_track','(phi | track)'],
	    ['pixeldedx_track','(pixeldedx | track)'],
	    ['stripsdedx_track','(stripsdedx | track)'],
	]

for plot in plots:
    print 'Drawing ', plot
    histname, xtitle = plot
    c1 = mkcanvas('c_'+histname)
    histo_sim = fsim.Get(histname)
    histo_fastsim = ffastsim.Get(histname)
    
    histo_sim.Sumw2()
    histo_fastsim.Sumw2()

    leg = TLegend(0.6,0.8,0.85,0.9)

    histoStyler(histo_sim, kRed)
    histoStyler(histo_fastsim, kBlue)
    histo_sim.Scale(1.0/histo_sim.Integral())
    histo_fastsim.Scale(1.0/histo_fastsim.Integral())

    histo_sim.Rebin(rebin)
    histo_fastsim.Rebin(rebin)

    histo_sim.SetLineWidth(3)
    histo_fastsim.SetLineWidth(3)

    leg.AddEntry(histo_sim,'T2bt FullSim')
    leg.AddEntry(histo_fastsim,'T2bt FastSim')

    rp = TRatioPlot(histo_fastsim,histo_sim)
    rp.SetH1DrawOpt("hist E0")
    rp.SetH2DrawOpt("E0")
    rp.Draw()
    leg.Draw()
    c1.Update()

    c1.Print(plotDir+'/'+histname+'.png')
    
    if logscale == True : 
	rp.GetUpperPad().SetLogy()
	c1.Update()
	c1.Print(plotDir+'/'+histname+'_log.png')


exit()

