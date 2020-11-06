import os,sys
from ROOT import *
from glob import glob
#from natsort import natsorted,ns

gROOT.SetBatch(1)
gStyle.SetOptStat(False)
#gStyle.SetOptFit(1111)

#format_c = 'pdf'
format_c = 'png'

#rebin = 5
rebin = 10
#rebin = 20

dict_Summer16_FullSimSignal = {
	#'Summer16FullSim.SMS-T2bt-LLChipm_ctau-200_mLSP-900':'./output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1.root',
	#'Summer16FullSim.SMS-T2bt-LLChipm_ctau-200_mLSP-1100':'./output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1100_TuneCUETP8M1.root',
	'Summer16FullSim.SMS-T2bt-LLChipm_ctau-200_mLSP-1100':'./output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1_TuneCUETP8M1.root',
        }

dict_Summer16_FastSimSignal = {
	#'Summer16FastSim.SMS-T2bt-LLChipm_ctau-200_mLSP-900':'./output_chargino/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1.root',
	#'Summer16FastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-1100':'./output_chargino/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-1100and300.root',
	'Summer16FastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-1100':'./output_chargino/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-1.root',
	}



def main(SelectedFastSim,SelectedFullSim,hist,outputdir):

    ctitle = 'FullSim/FastSim comparison'
    c = TCanvas(ctitle,ctitle,800,600)
    tl = TLegend(0.6,0.7,0.85,0.9)

    #c.SetLogy()
    
    fin={}
    histos={}
     
    # Fastsim MC
    i=0
    for name,f in sorted(SelectedFastSim.items()):
        fin[name] = TFile(f)
        histos[name] = fin[name].Get(hist)
	if i==0 :
	    print 'Cloning ',name
	    hFastsim = histos[name].Clone('hFastsim')
	else : 
	    print 'Adding ',name
	    hFastsim.Add(histos[name])
	i+=1
    
    hFastsim.GetXaxis().SetTitle('GeV')
    hFastsim.GetYaxis().SetTitle('Normalized')
    hFastsim.Scale(1.0/hFastsim.Integral())


    # Fullsim MC
    i = 0
    for name,f in sorted(SelectedFullSim.items()):
        fin[name] = TFile(f)
	histos[name] = fin[name].Get(hist) 
	if i==0:
	    print 'Cloning ',name
	    hFullsim = histos[name].Clone('hFullsim')
	else : 
	    print 'Adding ',name
	    hFullsim.Add(histos[name])
	i+=1

    hFullsim.Rebin(rebin)
    hFastsim.Rebin(rebin)
    
    hFullsim.GetXaxis().SetTitle('GeV')
    hFullsim.GetYaxis().SetTitle('Normalized')
    hFullsim.Scale(1.0/hFullsim.Integral())

    hFastsim.SetLineColor(kRed)
    hFullsim.SetLineColor(kBlue)
    #hFullsim.SetFillStyle(3002)
    #hFullsim.SetFillColor(kBlue)
    
    rp = TRatioPlot(hFullsim,hFastsim)
    rp.SetH1DrawOpt('E')
    rp.SetH2DrawOpt('E')
    rp.Draw()
    rp.GetUpperPad().SetLogy()
    rp.GetUpperRefYaxis().SetTitle("Normalized");
    #rp.GetUpperRefYaxis().SetRangeUser(0,0.1);
    rp.GetLowerRefYaxis().SetTitle("Fullsim/Fastsim");
    #rp.GetLowerRefYaxis().SetRangeUser(0,2);
    rp.GetLowerRefGraph().SetMinimum(0);
    rp.GetLowerRefGraph().SetMaximum(2);
   
    tl.AddEntry(hFullsim,'T2bt Fullsim','lE')
    tl.AddEntry(hFastsim,'T2bt FastSim','lE')
    tl.Draw()

    c.Update()
    c.Print(outputdir+'/RatioPlot_'+hist+'.'+format_c)
   
    
if __name__ == '__main__' :


    outputdir = './plots/Charginotrack_mStop1300_mLSP1'
    #outputdir = './plots/Charginotrack_mStop1300_mLSP1100'
    if not os.path.exists(outputdir) : os.system('mkdir -p '+outputdir)
       
    SelectedFullSim = dict_Summer16_FullSimSignal
    SelectedFastSim = dict_Summer16_FastSimSignal
    
    hists=[
        'hGenStopMass',
        'hGenLSPMass',
        'hGenCharginoP',
        'hGenCharginoPt',
        'hGenCharginoEta',
        'hGenCharginoPhi',
    	
        'hTrkP_charginomatch',
        'hTrkPt_charginomatch',
        'hTrkEta_charginomatch',
        'hTrkPhi_charginomatch',

        'hTrkPixelDedx_charginomatch_barrel',
    	'hTrkPixelDedxCalib_charginomatch_barrel',
    	'hTrkStripsDedx_charginomatch_barrel',
    	'hTrkPixelDedx_charginomatch_endcap',
    	'hTrkPixelDedxCalib_charginomatch_endcap',
    	'hTrkStripsDedx_charginomatch_endcap',

        ]
    
    # Run
    for hist in hists:
        main(SelectedFastSim,SelectedFullSim,hist,outputdir)

