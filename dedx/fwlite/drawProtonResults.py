import os as os_
import sys
from ROOT import *
from shared_utils import *
gROOT.SetBatch(1)
TH1.SetDefaultSumw2()

#plotDir = 'plots'
#plotDir = 'plots_noPU'
plotDir = 'plots_standardmixPU'
if not os_.path.exists(plotDir) :
    os_.system('mkdir -p '+plotDir)

fdata = TFile('./SV_rootfiles/vertex_Run2016G8691FBA4-2697-E711-B324-F02FA768CFFE_SVstuff.root')
fsim = TFile('./SV_rootfiles/vertex_RunIISummer16DR80PremixD6188037-8CA5-E911-9A4F-34E6D7E05F1B_SVstuff.root')
#ffastsim = TFile('./SV_rootfiles/vertex_higgsino94x_susyall_mChipm250GeV_dm1p01GeV_pu35_part19of25_SVstuff.root')
#ffastsim = TFile('./SV_rootfiles/vertex_SUS-RunIISummer15GS-00734_T2btLLFastSim_103of200_SVstuff.root')
#ffastsim = TFile('./SV_rootfiles/vertex_SUS-RunIISummer15GS-00734_T2btLLFastSim_NoPU_SVstuff.root')
ffastsim = TFile('./SV_rootfiles/vertex_SUS-RunIISummer15GS-00734_T2btLLFastSim_StandardMixing_SVstuff.root')
fdata.ls()


#rebin = 1
rebin = 5
#rebin = 50

fnew = TFile('rootfiles/ProtonResults.root', 'recreate')

plots = [
	    #['mass_highPurity','mass_highPurity| SV'],
	    ##['P_Lambda','P_Lambda'],
	    #['P_good_Lambda','P_Lambda'],
	    #['P_good_Lambda_yesdedx','P_Lambda | dedx exist'],
	    ##['pt_Lambda','pt_Lambda'],
	    #['pt_good_Lambda','pt_Lambda'],
	    #['pt_good_Lambda_yesdedx','pt_Lambda | dedx exist'],
	    ##['eta_good_Lambda_yesdedx','eta_Lambda | dedx exist'],
	    ##['mass_Lambda','reconstructed #Lambda^{0} invariant mass [GeV]'],
	    #['mass_good_Lambda','reconstructed #Lambda^{0} invariant mass [GeV]'],
	    #['mass_good_Lambda_yesdedx','reconstructed #Lambda^{0} invariant mass [GeV] | dedx exist'],
	    ##['radialDistance_Lambda','rad.dist | Lambda [cm]'],
	    #['radialDistance_good_Lambda','rad.dist | Lambda [cm]'],
	    #['radialDistance_good_Lambda_yesdedx','rad.dist | Lambda [cm] | dedx exist'],
	    ##['bestCosAngle','bestCosAngle | PV,SV'],
	    #['bestCosAngle_good_Lambda','bestCosAngle | PV,SV'],
	    #['bestCosAngle_good_Lambda_yesdedx','bestCosAngle | PV,SV | dedx exist'],
	    
	    #['P_proton','(P | proton) [GeV]'],
	    ['P_good_proton','(P | proton) [GeV]'],
	    ['P_good_proton_yesdedx','(P | proton) [GeV] | dedx exist'],
	    ['P_good_proton_yesdedx_barrel','(P | proton) [GeV] | dedx exist'],
	    ['P_good_proton_yesdedx_endcap','(P | proton) [GeV] | dedx exist'],
	    #['pt_proton','(pT | proton) [GeV]'],
	    ['pt_good_proton','(pT | proton) [GeV]'],
	    ['pt_good_proton_yesdedx','(pT | proton) [GeV] | dedx exist'],
	    ['pt_good_proton_yesdedx_barrel','(pT | proton) [GeV] | dedx exist'],
	    ['pt_good_proton_yesdedx_endcap','(pT | proton) [GeV] | dedx exist'],
	    ['eta_good_proton_yesdedx','(eta | proton) [GeV] | dedx exist'],
	    #['dedxpixel_proton','pixel de/dx | proton [MeV/cm]'],
	    ['dedxpixel_good_proton','pixel de/dx | proton [MeV/cm]'],
	    ['dedxpixel_good_proton_yesdedx','pixel de/dx | proton [MeV/cm] | dedx exist'],
	    ['dedxpixel_good_proton_yesdedx_barrel','pixel de/dx | proton [MeV/cm] | dedx exist'],
	    ['dedxpixel_good_proton_yesdedx_endcap','pixel de/dx | proton [MeV/cm] | dedx exist'],
	    #['dedxpixelCalib_good_proton','calib.pixel de/dx | proton [MeV/cm]'],
	    #['dedxstrips_proton','strip de/dx | proton [MeV/cm]'],
	    ['dedxstrips_good_proton','strip de/dx | proton [MeV/cm]'],
	    ['dedxstrips_good_proton_yesdedx','strip de/dx | proton [MeV/cm] | dedx exist'],
	    ['dedxstrips_good_proton_yesdedx_barrel','strip de/dx | proton [MeV/cm] | dedx exist'],
	    ['dedxstrips_good_proton_yesdedx_endcap','strip de/dx | proton [MeV/cm] | dedx exist'],
	    #['massdedxpixel_proton','mass(p,pixel de/dx | proton) [GeV]'],
	    ['massdedxpixel_good_proton','mass(p,pixel de/dx | proton) [GeV]'],
	    ['massdedxpixel_good_proton_yesdedx','mass(p,pixel de/dx | proton) [GeV] | dedx exist'],
	    #['massdedxpixelCalib_proton','mass(p,calib.pixel de/dx | proton) [GeV]'],
	    #['massdedxpixelCalib_good_proton','mass(p,calib.pixel de/dx | proton) [GeV]'],
	    #['massdedxstrips_proton','mass(p,strip de/dx | proton) [GeV]'],
	    #['massdedxstrips_good_proton','mass(p,strip de/dx | proton) [GeV]'],
	    #['massdedxstrips_good_proton_yesdedx','mass(p,strip de/dx | proton) [GeV] | dedx exist'],
	]

for plot in plots:
    print 'Drawing ', plot
    histname, xtitle = plot
    c1 = mkcanvas('c_'+histname)
    histo_data = fdata.Get(histname)
    histo_sim = fsim.Get(histname)
    histo_fastsim = ffastsim.Get(histname)
    
    histo_data.Sumw2()
    histo_sim.Sumw2()
    histo_fastsim.Sumw2()

    leg = mklegend(x1=.42, y1=.55, x2=.79, y2=.76, color=kWhite)

    histoStyler(histo_data, kBlack)
    histoStyler(histo_sim, kRed)
    histoStyler(histo_fastsim, kBlue)
    histo_data.Scale(1.0/histo_data.Integral())
    histo_sim.Scale(1.0/histo_sim.Integral())
    histo_fastsim.Scale(1.0/histo_fastsim.Integral())

    histo_data.SetLineWidth(3)
    histo_sim.SetLineWidth(3)
    histo_fastsim.SetLineWidth(3)

    histo_data.Rebin(rebin)
    histo_sim.Rebin(rebin)
    histo_fastsim.Rebin(rebin)

    histo_data.GetXaxis().SetTitle(xtitle)

    histo_data.SetTitle('Run 2016G')
    histo_sim.SetTitle('T2bt FullSim')
    histo_fastsim.SetTitle('T2bt FastSim')


    hratio, [pad1, pad2] = FabDraw(c1,leg,histo_data,[histo_sim],datamc='data',lumi=epsi, title = '', LinearScale=True, fractionthing='data / sim')
    #hratio, [pad1, pad2] = FabDraw(c1,leg,histo_data,[histo_fastsim],datamc='data',lumi=epsi, title = '', LinearScale=True, fractionthing='data / sim')

    pad1.cd()
    histo_fastsim.Draw('SAMES')
    leg.AddEntry(histo_fastsim, 'T2bt Fastsim')
    leg.Draw()
    c1.Update()
    
    fnew.cd()
    c1.Write()
    c1.Print(plotDir+'/'+histname+'.png')
    c1.Clear()
print 'just created', fnew.GetName()
fnew.Close()
exit()

