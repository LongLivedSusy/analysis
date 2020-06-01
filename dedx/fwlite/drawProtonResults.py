import os, sys
from ROOT import *
from shared_utils import *
gROOT.SetBatch(1)

fdata = TFile('./EDM_output/vertex_Run2016GC8DC13E5-2297-E711-B519-0090FAA597B4SVstuff.root')
#fsim = TFile('vertex_RunIISummer16DR80PremixB64B10BA-6BA5-E911-B5B2-AC1F6B0DE348SVstuff.root')
fsim = TFile('./EDM_output/vertex_higgsino94x_susyall_mChipm100GeV_dm0p16GeV_pu35_SVstuff.root')
fdata.ls()


rebin = 5

plotDir = 'plots'
if not os.path.exists(plotDir) :
    os.system('mkdir -p '+plotDir)

fnew = TFile('rootfiles/ProtonResults.root', 'recreate')

plots = [
	['massdedx_to1p5_Proton','mass(p,de/dx | proton) [GeV]'],
	['dedx_to1p5_Proton','de/dx | proton [GeV]'],
	['massdedxCalib_to1p5_Proton','mass(p,de/dx | proton) [GeV]'],
	['dedxCalib_to1p5_Proton','de/dx | proton [GeV]']
	]

for plot in plots:
    histname, xtitle = plot
    c1 = mkcanvas('c_'+histname)
    hMassFromDeDx_data = fdata.Get(histname)
    hMassFromDeDx_sim = fsim.Get(histname)

    leg = mklegend(x1=.42, y1=.55, x2=.79, y2=.76, color=kWhite)

    histoStyler(hMassFromDeDx_data, kBlack)
    histoStyler(hMassFromDeDx_sim, kRed)
    hMassFromDeDx_data.Scale(1.0/hMassFromDeDx_data.Integral())
    hMassFromDeDx_sim.Scale(1.0/hMassFromDeDx_sim.Integral())

    hMassFromDeDx_data.SetLineWidth(3)
    hMassFromDeDx_sim.SetLineWidth(3)

    hMassFromDeDx_data.Rebin(rebin)
    hMassFromDeDx_sim.Rebin(rebin)

    hMassFromDeDx_data.GetXaxis().SetTitle(xtitle)

    hMassFromDeDx_data.SetTitle('Run 2016G')
    if 'higgsino' in fsim.GetName() : 
	hMassFromDeDx_sim.SetTitle('higgsino FastSim')
    else : hMassFromDeDx_sim.SetTitle('Summer16 MC')


    hratio, [pad1, pad2] = FabDraw(c1,leg,hMassFromDeDx_data,[hMassFromDeDx_sim],datamc='data',lumi=epsi, title = '', LinearScale=True, fractionthing='data / sim')

    c1.Update()
    fnew.cd()
    c1.Write()
    c1.Print(plotDir+'/'histname+'.png')
print 'just created', fnew.GetName()
fnew.Close()
exit()

