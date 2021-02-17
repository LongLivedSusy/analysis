import os as os_
import sys
from ROOT import *
from shared_utils import *
gROOT.SetBatch(1)
#gStyle.SetOptStat(0)
TH1.SetDefaultSumw2()

plotDir = 'plots_Proton_Run2017C_UL'
#plotDir = 'plots_noPU'
#plotDir = 'plots_standardmixPU'
if not os_.path.exists(plotDir) :
    os_.system('mkdir -p '+plotDir)

fdata = TFile('./SV_rootfiles/vertex_Run2017C_SingleMuon_UL.root')
fsim = TFile('./SV_rootfiles/vertex_DYJetsToLL_M-50_UL17.root')
#ffastsim = TFile('./SV_rootfiles/vertex_SUS-RunIISummer15GS-00734_T2btLLFastSim_StandardMixing_SVstuff.root')
fdata.ls()


rebin = 1
rebin = 4
#rebin = 50

plots = [
	    ['mass_highPurity','mass_highPurity| SV'],
	    ['P_Lambda','P_Lambda'],
	    ['P_good_Lambda','P_Lambda'],
	    ['P_good_Lambda','P_Lambda | dedx exist'],
	    ['P_good_Lambda_NoMassWindow','P_Lambda | dedx exist'],
	    ['pt_Lambda','pt_Lambda'],
	    ['pt_good_Lambda','pt_Lambda'],
	    ['pt_good_Lambda','pt_Lambda | dedx exist'],
	    ['pt_good_Lambda_NoMassWindow','pt_Lambda | dedx exist'],
	    #['eta_good_Lambda','eta_Lambda | dedx exist'],
	    ['mass_Lambda','reconstructed #Lambda^{0} invariant mass [GeV]'],
	    ['mass_good_Lambda','reconstructed #Lambda^{0} invariant mass [GeV]'],
	    ['mass_good_Lambda_NoMassWindow','reconstructed #Lambda^{0} invariant mass [GeV] | dedx exist'],
	    ['radialDistance_Lambda','rad.dist | Lambda [cm]'],
	    ['radialDistance_good_Lambda','rad.dist | Lambda [cm]'],
	    ['radialDistance_good_Lambda_NoMassWindow','rad.dist | Lambda [cm] | dedx exist'],
	    ['bestCosAngle','bestCosAngle | PV,SV'],
	    ['bestCosAngle_good_Lambda','bestCosAngle | PV,SV'],
	    ['bestCosAngle_good_Lambda_NoMassWindow','bestCosAngle | PV,SV | dedx exist'],
	    ['P_good_proton','(P | proton) [GeV]'],
	    ['P_good_proton_barrel','(P | proton) [GeV]'],
	    ['P_good_proton_endcap','(P | proton) [GeV]'],
	    ['pt_good_proton','(pT | proton) [GeV] '],
	    ['pt_good_proton_barrel','(pT | proton) [GeV] '],
	    ['pt_good_proton_endcap','(pT | proton) [GeV] '],
	    ['eta_good_proton','(eta | proton) [GeV] '],
	    ['dedxpixel_good_proton','pixel de/dx | proton [MeV/cm] '],
	    ['dedxpixel_good_proton_barrel','pixel de/dx | proton [MeV/cm] '],
	    ['dedxpixel_good_proton_endcap','pixel de/dx | proton [MeV/cm] '],
	    ['dedxpixel_good_proton_P1to2','pixel de/dx | proton P[1-2] [MeV/cm] '],
	    ['dedxpixel_good_proton_P1to2_barrel','pixel de/dx | proton P[1-2] [MeV/cm] '],
	    #['dedxpixel_good_proton_P1to2_endcap','pixel de/dx | proton P[1-2] [MeV/cm] '],
	    ['dedxpixel_good_proton_P2to3','pixel de/dx | proton P[2-3] [MeV/cm] '],
	    ['dedxpixel_good_proton_P2to3_barrel','pixel de/dx | proton P[2-3] [MeV/cm] '],
	    ['dedxpixel_good_proton_P2to3_endcap','pixel de/dx | proton P[2-3] [MeV/cm] '],
	    ['dedxpixel_good_proton_P3to4','pixel de/dx | proton P[3-4] [MeV/cm] '],
	    ['dedxpixel_good_proton_P3to4_barrel','pixel de/dx | proton P[3-4] [MeV/cm] '],
	    ['dedxpixel_good_proton_P3to4_endcap','pixel de/dx | proton P[3-4] [MeV/cm] '],
	    ['dedxpixel_good_proton_P4to5','pixel de/dx | proton P[4-5] [MeV/cm] '],
	    ['dedxpixel_good_proton_P4to5_barrel','pixel de/dx | proton P[4-5] [MeV/cm] '],
	    ['dedxpixel_good_proton_P4to5_endcap','pixel de/dx | proton P[4-5] [MeV/cm] '],
	    ['dedxpixel_good_proton_P5to6','pixel de/dx | proton P[5-6] [MeV/cm] '],
	    ['dedxpixel_good_proton_P5to6_barrel','pixel de/dx | proton P[5-6] [MeV/cm] '],
	    ['dedxpixel_good_proton_P5to6_endcap','pixel de/dx | proton P[5-6] [MeV/cm] '],
	    ['dedxpixel_good_proton_P6toInf','pixel de/dx | proton P[6-Inf] [MeV/cm] '],
	    ['dedxpixel_good_proton_P6toInf_barrel','pixel de/dx | proton P[6-Inf] [MeV/cm] '],
	    ['dedxpixel_good_proton_P6toInf_endcap','pixel de/dx | proton P[6-Inf] [MeV/cm] '],
	    ['dedxpixelCalib_good_proton','pixel de/dx | proton [MeV/cm] '],
	    #['dedxpixelCalib_good_proton_barrel','pixel de/dx | proton [MeV/cm] '],
	    #['dedxpixelCalib_good_proton_endcap','pixel de/dx | proton [MeV/cm] '],
	    ['dedxpixelCalib_good_proton_P1to2','pixel de/dx | proton P[1-2] [MeV/cm] '],
	    ['dedxpixelCalib_good_proton_P1to2_barrel','pixel de/dx | proton P[1-2] [MeV/cm] '],
	    #['dedxpixelCalib_good_proton_P1to2_endcap','pixel de/dx | proton P[1-2] [MeV/cm] '],
	    ['dedxpixelCalib_good_proton_P2to3','pixel de/dx | proton P[2-3] [MeV/cm] '],
	    ['dedxpixelCalib_good_proton_P2to3_barrel','pixel de/dx | proton P[2-3] [MeV/cm] '],
	    ['dedxpixelCalib_good_proton_P2to3_endcap','pixel de/dx | proton P[2-3] [MeV/cm] '],
	    ['dedxpixelCalib_good_proton_P3to4','pixel de/dx | proton P[3-4] [MeV/cm] '],
	    ['dedxpixelCalib_good_proton_P3to4_barrel','pixel de/dx | proton P[3-4] [MeV/cm] '],
	    ['dedxpixelCalib_good_proton_P3to4_endcap','pixel de/dx | proton P[3-4] [MeV/cm] '],
	    ['dedxpixelCalib_good_proton_P4to5','pixel de/dx | proton P[4-5] [MeV/cm] '],
	    ['dedxpixelCalib_good_proton_P4to5_barrel','pixel de/dx | proton P[4-5] [MeV/cm] '],
	    ['dedxpixelCalib_good_proton_P4to5_endcap','pixel de/dx | proton P[4-5] [MeV/cm] '],
	    ['dedxpixelCalib_good_proton_P5to6','pixel de/dx | proton P[5-6] [MeV/cm] '],
	    ['dedxpixelCalib_good_proton_P5to6_barrel','pixel de/dx | proton P[5-6] [MeV/cm] '],
	    ['dedxpixelCalib_good_proton_P5to6_endcap','pixel de/dx | proton P[5-6] [MeV/cm] '],
	    ['dedxpixelCalib_good_proton_P6toInf','pixel de/dx | proton P[6-Inf] [MeV/cm] '],
	    ['dedxpixelCalib_good_proton_P6toInf_barrel','pixel de/dx | proton P[6-Inf] [MeV/cm] '],
	    ['dedxpixelCalib_good_proton_P6toInf_endcap','pixel de/dx | proton P[6-Inf] [MeV/cm] '],
	    ['dedxstrips_good_proton','strip de/dx | proton [MeV/cm]'],
	    ['dedxstrips_good_proton_barrel','strip de/dx | proton [MeV/cm] '],
	    ['dedxstrips_good_proton_endcap','strip de/dx | proton [MeV/cm] '],
	    ##['massdedxpixel_good_proton','mass(p,pixel de/dx | proton) [GeV]'],
	    #['massdedxpixel_good_proton','mass(p,pixel de/dx | proton) [GeV] '],
	    ##['massdedxpixelCalib_proton','mass(p,calib.pixel de/dx | proton) [GeV]'],
	    #['massdedxpixelCalib_good_proton','mass(p,calib.pixel de/dx | proton) [GeV]'],
	    ##['massdedxstrips_good_proton','mass(p,strip de/dx | proton) [GeV]'],
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
    
    if 'Run2016B' in fdata : histo_data.SetTitle('Run 2016B')
    elif 'Run2016G' in fdata : histo_data.SetTitle('Run 2016G')
    elif 'Run2017F' in fdata : histo_data.SetTitle('Run 2017F')
    elif 'Run2018C' in fdata : histo_data.SetTitle('Run 2018C')
    
    #histo_sim.SetTitle('Summer16 T2bt MC')
    histo_sim.SetTitle('Summer19UL17 DYJetsToLL')
    #histo_fastsim.SetTitle('T2bt FastSim')


    hratio, [pad1, pad2] = FabDraw(c1,leg,histo_data,[histo_sim],datamc='data',lumi=epsi, title = '', LinearScale=True, fractionthing='data / sim')
    
    latex = TLatex()
    
    pad1.cd()
    #histo_fastsim.Draw('SAMES')
    #leg.AddEntry(histo_fastsim, 'T2bt Fastsim')
    leg.Draw()
    #if ('dedxpixelCalib_good_proton' in histname or 'dedxstrips_good_proton' in histname) and 'mass' not in histname:
    #    latex.DrawLatex(5,0.08,"#epsilon_data(2.0<de/dx<4.0 MeV/cm) = "+str(round(histo_data.Integral(histo_data.FindBin(2),histo_data.FindBin(4)),2)))
    #	latex.DrawLatex(5,0.06,"#epsilon_data(4.0<de/dx MeV/cm) = "+str(round(histo_data.Integral(histo_data.FindBin(4),99999),2)))
    #    latex.DrawLatex(5,0.04,"#epsilon_mc(2.0<de/dx<4.0 MeV/cm) = "+str(round(histo_sim.Integral(histo_sim.FindBin(2),histo_sim.FindBin(4)),2)))
    #	latex.DrawLatex(5,0.02,"#epsilon_mc(4.0<de/dx MeV/cm) = "+str(round(histo_sim.Integral(histo_sim.FindBin(4),99999),2)))

    c1.Update()
    
    c1.Print(plotDir+'/'+histname+'.png')
    c1.Clear()
    c1.Close()
exit()

