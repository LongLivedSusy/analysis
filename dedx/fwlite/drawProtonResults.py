import os as os_
import sys
from ROOT import *
from shared_utils import *
gROOT.SetBatch(1)
#gStyle.SetOptStat(0)
TH1.SetDefaultSumw2()

plotDir = 'plots'
#plotDir = 'plots_noPU'
#plotDir = 'plots_standardmixPU'
if not os_.path.exists(plotDir) :
    os_.system('mkdir -p '+plotDir)

fdata = TFile('./SV_rootfiles/vertex_Run2016G.root')
fsim = TFile('./SV_rootfiles/vertex_RunIISummer16DR80Premix_T2bt.root')
#ffastsim = TFile('./SV_rootfiles/vertex_SUS-RunIISummer15GS-00734_T2btLLFastSim_StandardMixing_SVstuff.root')
fdata.ls()


#rebin = 1
rebin = 5
#rebin = 50

fnew = TFile('rootfiles/ProtonResults.root', 'recreate')

plots = [
	    #['mass_highPurity','mass_highPurity| SV'],
	    ##['P_Lambda','P_Lambda'],
	    #['P_good_Lambda','P_Lambda'],
	    #['P_good_Lambda_dedxexist','P_Lambda | dedx exist'],
	    ##['pt_Lambda','pt_Lambda'],
	    #['pt_good_Lambda','pt_Lambda'],
	    #['pt_good_Lambda_dedxexist','pt_Lambda | dedx exist'],
	    ##['eta_good_Lambda_dedxexist','eta_Lambda | dedx exist'],
	    ##['mass_Lambda','reconstructed #Lambda^{0} invariant mass [GeV]'],
	    #['mass_good_Lambda','reconstructed #Lambda^{0} invariant mass [GeV]'],
	    #['mass_good_Lambda_dedxexist','reconstructed #Lambda^{0} invariant mass [GeV] | dedx exist'],
	    ##['radialDistance_Lambda','rad.dist | Lambda [cm]'],
	    #['radialDistance_good_Lambda','rad.dist | Lambda [cm]'],
	    #['radialDistance_good_Lambda_dedxexist','rad.dist | Lambda [cm] | dedx exist'],
	    ##['bestCosAngle','bestCosAngle | PV,SV'],
	    #['bestCosAngle_good_Lambda','bestCosAngle | PV,SV'],
	    #['bestCosAngle_good_Lambda_dedxexist','bestCosAngle | PV,SV | dedx exist'],
	    
	    ['P_good_proton','(P | proton) [GeV]'],
	    ['P_good_proton_dedxexist','(P | proton) [GeV]'],
	    ['P_good_proton_dedxexist_barrel','(P | proton) [GeV]'],
	    ['P_good_proton_dedxexist_endcap','(P | proton) [GeV]'],
	    ['pt_good_proton','(pT | proton) [GeV]'],
	    ['pt_good_proton_dedxexist','(pT | proton) [GeV] '],
	    ['pt_good_proton_dedxexist_barrel','(pT | proton) [GeV] '],
	    ['pt_good_proton_dedxexist_endcap','(pT | proton) [GeV] '],
	    ['eta_good_proton_dedxexist','(eta | proton) [GeV] '],
	    ['dedxpixel_good_proton','pixel de/dx | proton [MeV/cm]'],
	    ['dedxpixel_good_proton_dedxexist','pixel de/dx | proton [MeV/cm] '],
	    #['dedxpixel_good_proton_dedxexist_P0to0p5','pixel de/dx | proton P[0-0.5] [MeV/cm] '],
	    #['dedxpixel_good_proton_dedxexist_P0p5to1','pixel de/dx | proton P[0.5-1] [MeV/cm] '],
	    ['dedxpixel_good_proton_dedxexist_P1to1p5','pixel de/dx | proton P[1-1.5] [MeV/cm] '],
	    ['dedxpixel_good_proton_dedxexist_P1p5to2','pixel de/dx | proton P[1.5-2] [MeV/cm] '],
	    ['dedxpixel_good_proton_dedxexist_P2to3','pixel de/dx | proton P[2-3] [MeV/cm] '],
	    ['dedxpixel_good_proton_dedxexist_P3toInf','pixel de/dx | proton P[3-Inf] [MeV/cm] '],
	    ['dedxpixel_good_proton_dedxexist_barrel','pixel de/dx | proton [MeV/cm] '],
	    ['dedxpixel_good_proton_dedxexist_endcap','pixel de/dx | proton [MeV/cm] '],
	    ['dedxpixelCalib_good_proton_dedxexist','calib.pixel de/dx | proton [MeV/cm]'],
	    #['dedxpixelCalib_good_proton_dedxexist_P0to0p5','pixel de/dx | proton P[0-0.5] [MeV/cm] '],
	    #['dedxpixelCalib_good_proton_dedxexist_P0p5to1','pixel de/dx | proton P[0.5-1] [MeV/cm] '],
	    ['dedxpixelCalib_good_proton_dedxexist_P1to1p5','pixel de/dx | proton P[1-1.5] [MeV/cm] '],
	    ['dedxpixelCalib_good_proton_dedxexist_P1p5to2','pixel de/dx | proton P[1.5-2] [MeV/cm] '],
	    ['dedxpixelCalib_good_proton_dedxexist_P2to3','pixel de/dx | proton P[2-3] [MeV/cm] '],
	    ['dedxpixelCalib_good_proton_dedxexist_P3toInf','pixel de/dx | proton P[3-Inf] [MeV/cm] '],
	    ['dedxstrips_good_proton','strip de/dx | proton [MeV/cm]'],
	    ['dedxstrips_good_proton_dedxexist','strip de/dx | proton [MeV/cm] '],
	    ['dedxstrips_good_proton_dedxexist_barrel','strip de/dx | proton [MeV/cm] '],
	    ['dedxstrips_good_proton_dedxexist_endcap','strip de/dx | proton [MeV/cm] '],
	    #['massdedxpixel_good_proton','mass(p,pixel de/dx | proton) [GeV]'],
	    #['massdedxpixel_good_proton_dedxexist','mass(p,pixel de/dx | proton) [GeV] '],
	    #['massdedxpixelCalib_proton','mass(p,calib.pixel de/dx | proton) [GeV]'],
	    #['massdedxpixelCalib_good_proton_dedxexist','mass(p,calib.pixel de/dx | proton) [GeV]'],
	    ['massdedxstrips_good_proton','mass(p,strip de/dx | proton) [GeV]'],
	    ['massdedxstrips_good_proton_dedxexist','mass(p,strip de/dx | proton) [GeV] '],
	]

for plot in plots:
    print 'Drawing ', plot
    histname, xtitle = plot
    c1 = mkcanvas('c_'+histname)
    histo_data = fdata.Get(histname)
    histo_sim = fsim.Get(histname)
    #histo_fastsim = ffastsim.Get(histname)
    
    histo_data.Sumw2()
    histo_sim.Sumw2()
    #histo_fastsim.Sumw2()

    leg = mklegend_(x1=.42, y1=.55, x2=.79, y2=.76, color=kWhite)

    histoStyler(histo_data, kBlack)
    histoStyler(histo_sim, kRed)
    #histoStyler(histo_fastsim, kBlue)
    histo_data.Scale(1.0/histo_data.Integral())
    histo_sim.Scale(1.0/histo_sim.Integral())
    #histo_fastsim.Scale(1.0/histo_fastsim.Integral())

    histo_data.SetLineWidth(3)
    histo_sim.SetLineWidth(3)
    #histo_fastsim.SetLineWidth(3)

    histo_data.Rebin(rebin)
    histo_sim.Rebin(rebin)
    #histo_fastsim.Rebin(rebin)

    histo_data.GetXaxis().SetTitle(xtitle)

    histo_data.SetTitle('Run 2016G')
    histo_sim.SetTitle('Summer16 T2bt MC')
    #histo_fastsim.SetTitle('T2bt FastSim')


    hratio, [pad1, pad2] = FabDraw(c1,leg,histo_data,[histo_sim],datamc='data',lumi=epsi, title = '', LinearScale=True, fractionthing='data / sim')

    pad1.cd()
    #histo_fastsim.Draw('SAMES')
    #leg.AddEntry(histo_fastsim, 'T2bt Fastsim')
    leg.Draw()
    c1.Update()
    
    fnew.cd()
    c1.Write()
    c1.Print(plotDir+'/'+histname+'.png')
    c1.Clear()
    c1.Close()
print 'just created', fnew.GetName()
fnew.Close()
exit()

