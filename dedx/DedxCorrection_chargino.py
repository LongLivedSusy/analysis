import os,sys
from ROOT import *
from glob import glob
#from natsort import natsorted,ns

gROOT.SetBatch(1)
gStyle.SetOptStat(False)
#gStyle.SetOptFit(1111)

#format_c = 'pdf'
format_c = 'png'

rebin = 10

dict_Summer16_FullSimSignal = {
	'Summer16FullSim.SMS-T2bt-LLChipm_ctau-200_mLSP-900':'./output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1.root',
        }

dict_Summer16_FastSimSignal = {
	'Summer16FastSim.SMS-T2bt-LLChipm_ctau-200_mLSP-900':'./output_chargino/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1.root',
	}


def main(SelectedFastSim,SelectedFullSim,hist,outputdir):

    ctitle = 'Dedx'
    c = TCanvas(ctitle,ctitle,800,600)
    tl = TLegend(0.6,0.6,0.85,0.9)
    
    fin={}
    hDedx={}
     
    c.cd()

     
    # MCs to be corrected
    i=0
    for name,f in sorted(SelectedFastSim.items()):
        fin[name] = TFile(f)
        hDedx[name] = fin[name].Get(hist)
	if i==0 :
	    print 'Cloning ',name
	    hDedx_totalMC = hDedx[name].Clone('hDedx_totalMC')
	else : 
	    print 'Adding ',name
	    hDedx_totalMC.Add(hDedx[name])
	i+=1
    
    hDedx_totalMC.GetXaxis().SetTitle('MeV/cm')
    hDedx_totalMC.GetYaxis().SetTitle('Normalized')
    hDedx_totalMC.Scale(1.0/hDedx_totalMC.Integral())


    # standard candle MC
    i = 0
    for name,f in sorted(SelectedFullSim.items()):
        fin[name] = TFile(f)
	hDedx[name] = fin[name].Get(hist) #MC : FullSim gen-matched muon dEdx at barrel region as standard candle
	if i==0:
	    print 'Cloning ',name
	    hDedx_standard = hDedx[name].Clone('hDedx_standard')
	else : 
	    print 'Adding ',name
	    hDedx_standard.Add(hDedx[name])
	i+=1

    hDedx_standard.GetXaxis().SetTitle('MeV/cm')
    hDedx_standard.GetYaxis().SetTitle('Normalized')
    hDedx_standard.Scale(1.0/hDedx_standard.Integral())

    c.cd()
    hDedx_standard.Rebin(rebin)
    hDedx_totalMC.Rebin(rebin)
    rp = TRatioPlot(hDedx_standard,hDedx_totalMC)
    rp.Draw()
    if 'Pixel' in hist : 
        hDedx_totalMC.SetTitle('harmonic-2 pixel dEdx')
        hDedx_standard.SetTitle('harmonic-2 pixel dEdx')
    elif 'Strips' in hist : 
        hDedx_totalMC.SetTitle('harmonic-2 strips dEdx')
        hDedx_standard.SetTitle('harmonic-2 strips dEdx')
    else : print 'no pixel/strips?'


    hDedx_totalMC.SetLineColor(kRed)
    hDedx_standard.SetFillStyle(3002)
    hDedx_standard.SetFillColor(kBlue)
    rp.GetUpperRefYaxis().SetTitle("Normalized");
    rp.GetUpperRefYaxis().SetRangeUser(0,0.1);
    rp.GetLowerRefYaxis().SetTitle("ratio");
    rp.GetLowerRefYaxis().SetRangeUser(0,2);
    tl.AddEntry(hDedx_standard, 'Summer16 T2bt Fullsim')
    tl.AddEntry(hDedx_totalMC,'Summer16 T2bt FastSim','l')
    tl.Draw()
    c.SaveAs(outputdir+'/RatioPlot_'+hist+'.'+format_c)
   
    
if __name__ == '__main__' :


    outputdir = './plots/Charginotrack'
    if not os.path.exists(outputdir) : os.system('mkdir -p '+outputdir)
       
    SelectedFullSim = dict_Summer16_FullSimSignal
    SelectedFastSim = dict_Summer16_FastSimSignal
    
    hists=[
    	 # before calibration
    	'hTrkPixelDedx_charginomatch_barrel',
    	'hTrkPixelDedx_charginomatch_endcap',
    	'hTrkStripsDedx_charginomatch_barrel',
    	'hTrkStripsDedx_charginomatch_endcap',
    	]
    
    # Run
    for hist in hists:
        main(SelectedFastSim,SelectedFullSim,hist,outputdir)

