import os,sys
from ROOT import *
from glob import glob
#from natsort import natsorted,ns

gROOT.SetBatch(1)
gStyle.SetOptStat(False)
#gStyle.SetOptFit(1111)

#format_c = 'pdf'
format_c = 'png'


dict_Summer16 = {
	'WJetsToLNu_TuneCUETP8M1':'./output_mediumchunks/Summer16.WJetsToLNu_TuneCUETP8M1.root',
	'WJetsToLNu_HT-100To200':'./output_mediumchunks/Summer16.WJetsToLNu_HT-100To200.root',
	'WJetsToLNu_HT-200To400':'./output_mediumchunks/Summer16.WJetsToLNu_HT-200To400.root',
	'WJetsToLNu_HT-400To600':'./output_mediumchunks/Summer16.WJetsToLNu_HT-400To600.root',
	'WJetsToLNu_HT-600To800':'./output_mediumchunks/Summer16.WJetsToLNu_HT-600To800.root',
	'WJetsToLNu_HT-800To1200':'./output_mediumchunks/Summer16.WJetsToLNu_HT-800To1200.root',
	'WJetsToLNu_HT-1200To2500':'./output_mediumchunks/Summer16.WJetsToLNu_HT-1200To2500.root',
	'WJetsToLNu_HT-2500ToInf':'./output_mediumchunks/Summer16.WJetsToLNu_HT-2500ToInf.root',
	'DYJetsToLL_M-50_TuneCUETP8M1':'./output_mediumchunks/Summer16.DYJetsToLL_M-50_TuneCUETP8M1.root',
	'DYJetsToLL_M-50_HT-100to200':'./output_mediumchunks/Summer16.DYJetsToLL_M-50_HT-100to200.root',
	'DYJetsToLL_M-50_HT-200to400':'./output_mediumchunks/Summer16.DYJetsToLL_M-50_HT-200to400.root',
	'DYJetsToLL_M-50_HT-400to600':'./output_mediumchunks/Summer16.DYJetsToLL_M-50_HT-400to600.root',
	'DYJetsToLL_M-50_HT-600to800':'./output_mediumchunks/Summer16.DYJetsToLL_M-50_HT-600to800.root',
	'DYJetsToLL_M-50_HT-800to1200':'./output_mediumchunks/Summer16.DYJetsToLL_M-50_HT-800to1200.root',
	'DYJetsToLL_M-50_HT-1200to2500':'./output_mediumchunks/Summer16.DYJetsToLL_M-50_HT-1200to2500.root',
	'DYJetsToLL_M-50_HT-2500toInf':'./output_mediumchunks/Summer16.DYJetsToLL_M-50_HT-2500toInf.root',
	'QCD_HT200to300':'./output_mediumchunks/Summer16.QCD_HT200to300.root',
	'QCD_HT300to500':'./output_mediumchunks/Summer16.QCD_HT300to500.root',
	'QCD_HT500to700':'./output_mediumchunks/Summer16.QCD_HT500to700.root',
	'QCD_HT700to1000':'./output_mediumchunks/Summer16.QCD_HT700to1000.root',
	'QCD_HT1000to1500':'./output_mediumchunks/Summer16.QCD_HT1000to1500.root',
	'QCD_HT1500to2000':'./output_mediumchunks/Summer16.QCD_HT1500to2000.root',
	'QCD_HT2000toInf':'./output_mediumchunks/Summer16.QCD_HT2000toInf.root',
	'TTJets':'./output_mediumchunks/Summer16.TTJets.root',
	'WW':'./output_mediumchunks/Summer16.WW.root',
	'WZ':'./output_mediumchunks/Summer16.WZ.root',
	'ZZ':'./output_mediumchunks/Summer16.ZZ.root',
	'ZJetsToNuNu_HT-100To200':'./output_mediumchunks/Summer16.ZJetsToNuNu_HT-100To200.root',
	'ZJetsToNuNu_HT-200To400':'./output_mediumchunks/Summer16.ZJetsToNuNu_HT-200To400.root',
	'ZJetsToNuNu_HT-400To600':'./output_mediumchunks/Summer16.ZJetsToNuNu_HT-400To600.root',
	'ZJetsToNuNu_HT-600To800':'./output_mediumchunks/Summer16.ZJetsToNuNu_HT-600To800.root',
	'ZJetsToNuNu_HT-800To1200':'./output_mediumchunks/Summer16.ZJetsToNuNu_HT-800To1200.root',
	'ZJetsToNuNu_HT-1200To2500':'./output_mediumchunks/Summer16.ZJetsToNuNu_HT-1200To2500.root',
	'ZJetsToNuNu_HT-2500ToInf':'./output_mediumchunks/Summer16.ZJetsToNuNu_HT-2500ToInf.root',
	}

dict_Summer16_FastSimSignal = {
	'Summer16FastSim.SMS-T2bt-LLChipm_ctau-200_mLSP-900':'./output_mediumchunks/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1.root',
	}

dict_Fall17 = {
	'WJetsToLNu_HT-100To200':'./output_mediumchunks/RunIIFall17MiniAODv2.WJetsToLNu_HT-100To200.root',
	'WJetsToLNu_HT-200To400':'./output_mediumchunks/RunIIFall17MiniAODv2.WJetsToLNu_HT-200To400.root',
	'WJetsToLNu_HT-400To600':'./output_mediumchunks/RunIIFall17MiniAODv2.WJetsToLNu_HT-400To600.root',
	'WJetsToLNu_HT-600To800':'./output_mediumchunks/RunIIFall17MiniAODv2.WJetsToLNu_HT-600To800.root',
	'WJetsToLNu_HT-800To1200':'./output_mediumchunks/RunIIFall17MiniAODv2.WJetsToLNu_HT-800To1200.root',
	'WJetsToLNu_HT-1200To2500':'./output_mediumchunks/RunIIFall17MiniAODv2.WJetsToLNu_HT-1200To2500.root',
	'WJetsToLNu_HT-2500ToInf':'./output_mediumchunks/RunIIFall17MiniAODv2.WJetsToLNu_HT-2500ToInf.root',
	'DYJetsToLL_M-50_TuneCUETP8M1':'./output_mediumchunks/RunIIFall17MiniAODv2.DYJetsToLL_M-50_TuneCP5.root',
	'DYJetsToLL_M-50_HT-100to200':'./output_mediumchunks/RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-100to200.root',
	'DYJetsToLL_M-50_HT-200to400':'./output_mediumchunks/RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-200to400.root',
	'DYJetsToLL_M-50_HT-400to600':'./output_mediumchunks/RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-400to600.root',
	'DYJetsToLL_M-50_HT-600to800':'./output_mediumchunks/RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-600to800.root',
	'DYJetsToLL_M-50_HT-800to1200':'./output_mediumchunks/RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-800to1200.root',
	'DYJetsToLL_M-50_HT-1200to2500':'./output_mediumchunks/RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-1200to2500.root',
	'DYJetsToLL_M-50_HT-2500toInf':'./output_mediumchunks/RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-2500toInf.root',
	'QCD_HT200to300':'./output_mediumchunks/RunIIFall17MiniAODv2.QCD_HT200to300.root',
	'QCD_HT300to500':'./output_mediumchunks/RunIIFall17MiniAODv2.QCD_HT300to500.root',
	'QCD_HT500to700':'./output_mediumchunks/RunIIFall17MiniAODv2.QCD_HT500to700.root',
	'QCD_HT700to1000':'./output_mediumchunks/RunIIFall17MiniAODv2.QCD_HT700to1000.root',
	'QCD_HT1000to1500':'./output_mediumchunks/RunIIFall17MiniAODv2.QCD_HT1000to1500.root',
	'QCD_HT1500to2000':'./output_mediumchunks/RunIIFall17MiniAODv2.QCD_HT1500to2000.root',
	'QCD_HT2000toInf':'./output_mediumchunks/RunIIFall17MiniAODv2.QCD_HT2000toInf.root',
	'TTJets_TuneCP5':'./output_mediumchunks/RunIIFall17MiniAODv2.TTJets_TuneCP5.root',
	'TTJets_HT-600to800':'./output_mediumchunks/RunIIFall17MiniAODv2.TTJets_HT-600to800.root',
	'TTJets_HT-800to1200':'./output_mediumchunks/RunIIFall17MiniAODv2.TTJets_HT-800to1200.root',
	'TTJets_HT-1200to2500':'./output_mediumchunks/RunIIFall17MiniAODv2.TTJets_HT-1200to2500.root',
	'TTJets_HT-2500toInf':'./output_mediumchunks/RunIIFall17MiniAODv2.TTJets_HT-2500toInf.root',
	'WWTo1L1Nu2Q':'./output_mediumchunks/RunIIFall17MiniAODv2.WWTo1L1Nu2Q.root',
	'WZTo1L1Nu2Q':'./output_mediumchunks/RunIIFall17MiniAODv2.WZTo1L1Nu2Q.root',
	'ZZTo2L2Q':'./output_mediumchunks/RunIIFall17MiniAODv2.ZZTo2L2Q.root',
	'ZJetsToNuNu_HT-100To200':'./output_mediumchunks/RunIIFall17MiniAODv2.ZJetsToNuNu_HT-100To200.root',
	'ZJetsToNuNu_HT-200To400':'./output_mediumchunks/RunIIFall17MiniAODv2.ZJetsToNuNu_HT-200To400.root',
	'ZJetsToNuNu_HT-400To600':'./output_mediumchunks/RunIIFall17MiniAODv2.ZJetsToNuNu_HT-400To600.root',
	'ZJetsToNuNu_HT-600To800':'./output_mediumchunks/RunIIFall17MiniAODv2.ZJetsToNuNu_HT-600To800.root',
	'ZJetsToNuNu_HT-800To1200':'./output_mediumchunks/RunIIFall17MiniAODv2.ZJetsToNuNu_HT-800To1200.root',
	'ZJetsToNuNu_HT-1200To2500':'./output_mediumchunks/RunIIFall17MiniAODv2.ZJetsToNuNu_HT-1200To2500.root',
	'ZJetsToNuNu_HT-2500ToInf':'./output_mediumchunks/RunIIFall17MiniAODv2.ZJetsToNuNu_HT-2500ToInf.root',
	}


def main(SelectedData,SelectedMC,hist,outputdir,isFastSim):

    print 'SelectedData : %s, SelectedMC : %s, hist : %s, outputdir : %s, isFastSim: %s'%(SelectedData,SelectedMC,hist,outputdir,isFastSim)

    if 'Pixel' in hist and 'ele' in hist:
	ctitle = 'Electron track Pixel dEdx'
    elif 'Pixel' in hist and 'mu' in hist:
	ctitle = 'Muon track Pixel dEdx'
    elif 'Strips' in hist and 'ele' in hist:
	ctitle = 'Electron track Strips dEdx'
    elif 'Strips' in hist and 'mu' in hist:
	ctitle = 'Muon track Strips dEdx'
    else :
	print 'Something wrong : hist does not contain proper strings'
	quit()

    c = TCanvas(ctitle,ctitle,800,600)
    c2 = TCanvas(ctitle+' all',ctitle+' all',800,600)
    tl = TLegend(0.6,0.6,0.9,0.9)
    
    fin={}
    hDedx={}
     
    c.cd()
     
    # MCs to be corrected
    i=0
    for name,f in sorted(SelectedData.items()):
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
    for name,f in sorted(SelectedMC.items()):
        fin[name] = TFile(f)
	hDedx[name] = fin[name].Get('hTrkPixelDedx_tightgenmumatch_barrel') #MC : FullSim gen-matched muon dEdx at barrel region as standard candle
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
    if isFastSim and not 'Calib' in hist : 
        fitres_totalMC = hDedx_totalMC.Fit('gaus','S','',4.0,5.5)
    elif isFastSim and 'Calib' in hist: 
        fitres_totalMC = hDedx_totalMC.Fit('gaus','S','',2.5,3.5)
    else :
        fitres_totalMC = hDedx_totalMC.Fit('gaus','S','',2.5,3.5)
    
    fitres_totalMC.Print()
    mean_totalMC = hDedx_totalMC.GetFunction('gaus').GetParameter(1)
    
    hDedx_totalMC.Draw('HIST E SAME')
    c.SaveAs(outputdir+'/Intercalib_totalMC_'+hist+'.'+format_c)
    
    fitres_standard = hDedx_standard.Fit('gaus','S','',2.3,3.5)
    fitres_standard.Print()
    mean_standard = hDedx_standard.GetFunction('gaus').GetParameter(1)
    tl.AddEntry(hDedx_standard, 'Summer16 MC barrel, mu=%s'%(round(mean_standard,3)))
    
    hDedx_standard.Draw('HIST E SAME')
    c.SaveAs(outputdir+'/Intercalib_Summer16_'+hist+'.'+format_c)

    c2.cd()
    rp = TRatioPlot(hDedx_standard,hDedx_totalMC)
    rp.Draw()
    hDedx_totalMC.SetTitle('harmonic-2 pixel dEdx')
    hDedx_standard.SetTitle('harmonic-2 pixel dEdx')
    hDedx_totalMC.SetLineColor(kRed)
    hDedx_standard.SetFillStyle(3002)
    hDedx_standard.SetFillColor(kBlue)
    rp.GetUpperRefYaxis().SetTitle("Normalized");
    rp.GetUpperRefYaxis().SetRangeUser(0,0.15);
    rp.GetLowerRefYaxis().SetTitle("ratio");
    rp.GetLowerRefYaxis().SetRangeUser(0,2);
    tl.AddEntry(hDedx_totalMC,'FastSim MC, mu=%s'%(round(mean_totalMC,3)),'l')
    #tl.AddEntry(hDedx_totalMC,'Fall17 MC, mu=%s'%(round(mean_totalMC,3)),'l')
    tl.Draw()
    c2.SaveAs(outputdir+'/RatioPlot_'+hist+'.'+format_c)
   
    # Extract Scale Factor 
    with open(outputdir+"/datacalib_dict"+hist+".txt",'w') as txt:
	SF = mean_standard / mean_totalMC
        print "'This MC' : %s,"%(SF)
	txt.write("'This MC' : %s,\n"%(SF))


     
    
if __name__ == '__main__' :

    DataSets = ["Summer16PrivateFastSim"]
    #DataSets = ["Fall17"]

    for	data in DataSets:
        outputdir = './plots/InterCalib_'+data
	if not os.path.exists(outputdir) : os.system('mkdir -p '+outputdir)
    	   
	if data == "Summer16PrivateFastSim":
	    SelectedMC = dict_Summer16
	    SelectedData = dict_Summer16_FastSimSignal
            isFastSim=True
	elif data == "Fall17":
	    SelectedMC = dict_Summer16
	    SelectedData = dict_Fall17
            isFastSim=False
	else : 
	    print 'wrong data'
	    quit()

	hists=[
		 # before calibration
		'hTrkPixelDedx_tightgenmumatch_barrel',
		'hTrkPixelDedx_tightgenmumatch_endcap',
		#'hTrkStripsDedx_tightgenmumatch_barrel',
		#'hTrkStripsDedx_tightgenmumatch_endcap',

		# after calibration
		#'hTrkPixelDedxCalib_tightgenmumatch',
		'hTrkPixelDedxCalib_tightgenmumatch_barrel',
		'hTrkPixelDedxCalib_tightgenmumatch_endcap',
		#'hTrkStripsDedxCalib_tightgenmumatch',
		#'hTrkStripsDedxCalib_tightgenmumatch_barrel',
		#'hTrkStripsDedxCalib_tightgenmumatch_endcap',
		]
	
	# Run
	for hist in hists:
	    main(SelectedData,SelectedMC,hist,outputdir,isFastSim)

