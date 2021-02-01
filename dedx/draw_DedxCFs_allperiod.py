from ROOT import *
from shared_utils import * 

gROOT.SetBatch(True)
gStyle.SetOptStat(0)
canvas = mkcanvas()
legend = mklegend_(x1=0.55, y1=0.7, x2=0.9, y2=0.9)

hMuonDedxCFs_barrel = TH1F('hMuonDedxCFs_barrel','',16,0,16)
hMuonDedxCFs_endcap = TH1F('hMuonDedxCFs_endcap','',16,0,16)
hProtonDedxCFs_barrel = TH1F('hProtonDedxCFs_barrel','',16,0,16)
hProtonDedxCFs_endcap = TH1F('hProtonDedxCFs_endcap','',16,0,16)
for index, key in enumerate(sorted(DedxCorr_Pixel_barrel)):
    if not 'Run' in key: continue
    hMuonDedxCFs_barrel.SetBinContent(index,DedxCorr_Pixel_barrel[key])
    hMuonDedxCFs_barrel.SetBinError(index,0)
    hMuonDedxCFs_barrel.GetXaxis().SetBinLabel(index,key)

for index, key in enumerate(sorted(DedxCorr_Pixel_endcap)):
    if not 'Run' in key: continue
    hMuonDedxCFs_endcap.SetBinContent(index,DedxCorr_Pixel_endcap[key])
    hMuonDedxCFs_endcap.SetBinError(index,0)
    hMuonDedxCFs_endcap.GetXaxis().SetBinLabel(index,key)

hProtonDedxCFs_barrel.SetBinContent(1,1.212) #Run2016B
hProtonDedxCFs_barrel.SetBinError(1,0) #Run2016B
hProtonDedxCFs_endcap.SetBinContent(1,1.273) #Run2016B
hProtonDedxCFs_endcap.SetBinError(1,0) #Run2016B
hProtonDedxCFs_barrel.SetBinContent(6,1.457) #Run2016G
hProtonDedxCFs_barrel.SetBinError(6,0) #Run2016G
hProtonDedxCFs_endcap.SetBinContent(6,1.438) #Run2016G
hProtonDedxCFs_endcap.SetBinError(6,0) #Run2016G
hProtonDedxCFs_barrel.SetBinContent(12,1.143) # Run2017F
hProtonDedxCFs_barrel.SetBinError(12,0) # Run2017F
hProtonDedxCFs_endcap.SetBinContent(12,1.380) # Run2017F
hProtonDedxCFs_endcap.SetBinError(12,0) # Run2017F
hProtonDedxCFs_barrel.SetBinContent(15,1.223) # Run2018C
hProtonDedxCFs_barrel.SetBinError(15,0) # Run2018C
hProtonDedxCFs_endcap.SetBinContent(15,1.391) # Run2018C
hProtonDedxCFs_endcap.SetBinError(15,0) # Run2018C

histoStyler(hMuonDedxCFs_barrel,kBlue)
histoStyler(hMuonDedxCFs_endcap,kGreen)
histoStyler(hProtonDedxCFs_barrel,kRed)
histoStyler(hProtonDedxCFs_endcap,46)

legend.AddEntry(hMuonDedxCFs_barrel,'muon barrel')
legend.AddEntry(hMuonDedxCFs_endcap,'muon endcap')
legend.AddEntry(hProtonDedxCFs_barrel,'proton(P>6) barrel')
legend.AddEntry(hProtonDedxCFs_barrel,'proton(P>6) endcap')


hMuonDedxCFs_barrel.SetTitle('pixel dE/dx correction factors')
hMuonDedxCFs_barrel.GetXaxis().SetLabelSize(0.039)


hMuonDedxCFs_barrel.GetYaxis().SetRangeUser(0.9,2.0)
hMuonDedxCFs_barrel.Draw()
hMuonDedxCFs_endcap.Draw('hsame')
hProtonDedxCFs_barrel.Draw('hsame')
hProtonDedxCFs_endcap.Draw('hsame')
legend.Draw()
stamp()
canvas.SaveAs("dEdxCF.png")
#canvas.SaveAs("dEdxCF.pdf")

