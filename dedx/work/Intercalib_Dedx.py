import os,sys
from ROOT import *
from glob import glob
from natsort import natsorted,ns

gROOT.SetBatch(1)
gStyle.SetOptStat(0)
gStyle.SetOptFit(1111)

#format_c = 'pdf'
format_c = 'png'


dict_Run2016_SingleMuon = {
		    'Run2016B_SingleMuon':'./output_mediumchunks/Run2016B_SingleMuon.root',
		    'Run2016C_SingleMuon':'./output_mediumchunks/Run2016C_SingleMuon.root',
	       	    'Run2016D_SingleMuon':'./output_mediumchunks/Run2016D_SingleMuon.root',
               	    'Run2016E_SingleMuon':'./output_mediumchunks/Run2016E_SingleMuon.root',
               	    'Run2016F_SingleMuon':'./output_mediumchunks/Run2016F_SingleMuon.root',
               	    'Run2016G_SingleMuon':'./output_mediumchunks/Run2016G_SingleMuon.root',
               	    'Run2016H_SingleMuon':'./output_mediumchunks/Run2016H_SingleMuon.root',
		    }

dict_Run2016_SingleElectron = {
		    'Run2016B_SingleElectron':'./output_mediumchunks/Run2016B_SingleElectron.root',
		    'Run2016C_SingleElectron':'./output_mediumchunks/Run2016C_SingleElectron.root',
	       	    'Run2016D_SingleElectron':'./output_mediumchunks/Run2016D_SingleElectron.root',
               	    'Run2016E_SingleElectron':'./output_mediumchunks/Run2016E_SingleElectron.root',
               	    'Run2016F_SingleElectron':'./output_mediumchunks/Run2016F_SingleElectron.root',
               	    'Run2016G_SingleElectron':'./output_mediumchunks/Run2016G_SingleElectron.root',
               	    'Run2016H_SingleElectron':'./output_mediumchunks/Run2016H_SingleElectron.root',
		    }

dict_Run2017_SingleMuon = {
		    'Run2017B_SingleMuon':'./output_mediumchunks/Run2017B_SingleMuon.root',
		    'Run2017C_SingleMuon':'./output_mediumchunks/Run2017C_SingleMuon.root',
	       	    'Run2017D_SingleMuon':'./output_mediumchunks/Run2017D_SingleMuon.root',
               	    'Run2017E_SingleMuon':'./output_mediumchunks/Run2017E_SingleMuon.root',
               	    'Run2017F_SingleMuon':'./output_mediumchunks/Run2017F_SingleMuon.root',
               	    #'Run2017G_SingleMuon':'./output_mediumchunks/Run2017G_SingleMuon.root',
               	    #'Run2017H_SingleMuon':'./output_mediumchunks/Run2017H_SingleMuon.root',
		    }

dict_Run2017_SingleElectron = {
		    'Run2017B_SingleElectron':'./output_mediumchunks/Run2017B_SingleElectron.root',
		    'Run2017C_SingleElectron':'./output_mediumchunks/Run2017C_SingleElectron.root',
	       	    'Run2017D_SingleElectron':'./output_mediumchunks/Run2017D_SingleElectron.root',
               	    'Run2017E_SingleElectron':'./output_mediumchunks/Run2017E_SingleElectron.root',
               	    'Run2017F_SingleElectron':'./output_mediumchunks/Run2017F_SingleElectron.root',
               	    #'Run2017G_SingleElectron':'./output_mediumchunks/Run2017G_SingleElectron.root',
               	    #'Run2017H_SingleElectron':'./output_mediumchunks/Run2017H_SingleElectron.root',
		    }

dict_Summer16 = {
	'WJetsToLNu_TuneCUETP8M1':'./output_mediumchunks/WJetsToLNu_TuneCUETP8M1.root',
	'WJetsToLNu_HT-100To200':'./output_mediumchunks/WJetsToLNu_HT-100To200.root',
	'WJetsToLNu_HT-200To400':'./output_mediumchunks/WJetsToLNu_HT-200To400.root',
	'WJetsToLNu_HT-400To600':'./output_mediumchunks/WJetsToLNu_HT-400To600.root',
	'WJetsToLNu_HT-600To800':'./output_mediumchunks/WJetsToLNu_HT-600To800.root',
	'WJetsToLNu_HT-800To1200':'./output_mediumchunks/WJetsToLNu_HT-800To1200.root',
	'WJetsToLNu_HT-1200To2500':'./output_mediumchunks/WJetsToLNu_HT-1200To2500.root',
	'WJetsToLNu_HT-2500ToInf':'./output_mediumchunks/WJetsToLNu_HT-2500ToInf.root',
	'DYJetsToLL_M-50_TuneCUETP8M1':'./output_mediumchunks/DYJetsToLL_M-50_TuneCUETP8M1.root',
	'DYJetsToLL_M-50_HT-100to200':'./output_mediumchunks/DYJetsToLL_M-50_HT-100to200.root',
	'DYJetsToLL_M-50_HT-200to400':'./output_mediumchunks/DYJetsToLL_M-50_HT-200to400.root',
	'DYJetsToLL_M-50_HT-400to600':'./output_mediumchunks/DYJetsToLL_M-50_HT-400to600.root',
	'DYJetsToLL_M-50_HT-600to800':'./output_mediumchunks/DYJetsToLL_M-50_HT-600to800.root',
	'DYJetsToLL_M-50_HT-800to1200':'./output_mediumchunks/DYJetsToLL_M-50_HT-800to1200.root',
	'DYJetsToLL_M-50_HT-1200to2500':'./output_mediumchunks/DYJetsToLL_M-50_HT-1200to2500.root',
	'DYJetsToLL_M-50_HT-2500toInf':'./output_mediumchunks/DYJetsToLL_M-50_HT-2500toInf.root',
	'QCD_HT200to300':'./output_mediumchunks/QCD_HT200to300.root',
	'QCD_HT300to500':'./output_mediumchunks/QCD_HT300to500.root',
	'QCD_HT500to700':'./output_mediumchunks/QCD_HT500to700.root',
	'QCD_HT700to1000':'./output_mediumchunks/QCD_HT700to1000.root',
	'QCD_HT1000to1500':'./output_mediumchunks/QCD_HT1000to1500.root',
	'QCD_HT1500to2000':'./output_mediumchunks/QCD_HT1500to2000.root',
	'QCD_HT2000toInf':'./output_mediumchunks/QCD_HT2000toInf.root',
	'TTJets':'./output_mediumchunks/TTJets.root',
	'WW':'./output_mediumchunks/WW.root',
	'WZ':'./output_mediumchunks/WZ.root',
	'ZZ':'./output_mediumchunks/ZZ.root',
	'ZJetsToNuNu_HT-100To200':'./output_mediumchunks/ZJetsToNuNu_HT-100To200.root',
	'ZJetsToNuNu_HT-200To400':'./output_mediumchunks/ZJetsToNuNu_HT-200To400.root',
	'ZJetsToNuNu_HT-400To600':'./output_mediumchunks/ZJetsToNuNu_HT-400To600.root',
	'ZJetsToNuNu_HT-600To800':'./output_mediumchunks/ZJetsToNuNu_HT-600To800.root',
	'ZJetsToNuNu_HT-800To1200':'./output_mediumchunks/ZJetsToNuNu_HT-800To1200.root',
	'ZJetsToNuNu_HT-1200To2500':'./output_mediumchunks/ZJetsToNuNu_HT-1200To2500.root',
	'ZJetsToNuNu_HT-2500ToInf':'./output_mediumchunks/ZJetsToNuNu_HT-2500ToInf.root',
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


def main(SelectedData,SelectedMC,hist,outputdir):

    print 'SelectedData : %s, SelectedMC : %s, hist : %s, outputdir : %s'%(SelectedData,SelectedMC,hist,outputdir)

    if 'Pixel' in hist and 'ele' in hist:
	ctitle = 'Electron track Pixel dEdx'
    elif 'Pixel' in hist and 'mu' in hist:
	ctitle = 'Muon track Pixel dEdx'
    elif 'Strips' in hist and 'ele' in hist:
	ctitle = 'Electron track Strips dEdx'
    elif 'Strips' in hist and 'mu' in hist:
	ctitle = 'Muon track Strips dEdx'
    else :
	print 'Something wrong : hist does not include proper strings'
	quit()

    c = TCanvas(ctitle,ctitle,800,600)
    c2 = TCanvas(ctitle+' all period',ctitle+' all period',800,600)
    tl = TLegend(0.5,0.6,0.9,0.9)
    
    fin={}
    hDedx={}
    mean={}
   
    #Data Intercalib
    c.cd()
    for name,f in natsorted(SelectedData.items()):
	print 'name',name
        fin[name] = TFile(f)
        hDedx[name] = fin[name].Get(hist)
        hDedx[name].SetTitle(name+' '+hist)
        hDedx[name].SetLineWidth(2)
        hDedx[name].Scale(1.0/hDedx[name].Integral())
	if 'Pixel' in hist:
	    fitres = hDedx[name].Fit('gaus','S','',1.5,3.0)
    	elif 'Strips' in hist:
	    fitres = hDedx[name].Fit('gaus','S','',1.5,4.0)
        fitres.Print()
        mean[name] = hDedx[name].GetFunction('gaus').GetParameter(1)
	hDedx[name].Draw('HIST E SAME')
    	c.SaveAs(outputdir+'/Intercalib_'+name+'_'+hist+'.'+format_c)
   
    # Data all period
    c2.cd()
    i=0
    for name,f in natsorted(SelectedData.items()):
        fin[name] = TFile(f)
        hDedx[name] = fin[name].Get(hist)
        hDedx[name].SetTitle(ctitle+' all period')
        hDedx[name].GetXaxis().SetTitle('MeV/cm')
        hDedx[name].GetYaxis().SetTitle('Normalized')
        hDedx[name].SetLineWidth(2)
        hDedx[name].SetLineColor(i+1)
        hDedx[name].Scale(1.0/hDedx[name].Integral())
	if 'Pixel' in hist:
	    hDedx[name].GetYaxis().SetRangeUser(0,0.1)
    	elif 'Strips' in hist:
	    hDedx[name].GetYaxis().SetRangeUser(0,0.2)
    	hDedx[name].Draw('HIST E SAME')
        tl.AddEntry(hDedx[name],'%s, mu=%s'%(name,round(mean[name],3)),'l')
        i=i+1
   
    # MC
    i = 0
    for name,f in natsorted(SelectedMC.items()):
        fin[name] = TFile(f)
        hDedx[name] = fin[name].Get(hist)
	if i==0:
	    print 'Cloning ',name
	    hDedx_total = hDedx[name].Clone('hDedx_total')
	else : 
	    print 'Adding ',name
	    hDedx_total.Add(hDedx[name])
	i+=1

    hDedx_total.SetTitle('Total MC background '+hist)
    hDedx_total.SetFillStyle(3002)
    hDedx_total.SetFillColor(kBlue)
    hDedx_total.Scale(1.0/hDedx_total.Integral())
    fitres = hDedx_total.Fit('gaus','S0','',2.5,3.5)
    fitres.Print()
    mean_mc = hDedx_total.GetFunction('gaus').GetParameter(1)
    hDedx_total.Draw('HIST E SAME')
    tl.AddEntry(hDedx_total, 'Total MC bkg, mu=%s'%(round(mean_mc,3)))
    tl.Draw('SAME')
    
    c2.SaveAs(outputdir+'/Intercalib_AllPeriod_'+hist+'.'+format_c)
    
    # Extract Scale Factor 
    if SelectedData == dict_Run2016_SingleMuon :
	stdRun='Run2016H_SingleMuon'
    elif SelectedData == dict_Run2016_SingleElectron :
	stdRun='Run2016H_SingleElectron'
    else : 
	print '2017 not yet'
    
    #print 'Standard Run period : ',stdRun
    #for name,f in natsorted(SelectedData.items()):
    #    SF = mean[stdRun] / mean[name]
    #    print "'%s' : %s,"%(name.split('_')[0], SF)
    #SF = mean[stdRun] / mean_mc
    #print "'Summer16' : %s,"%(SF)
    
    
if __name__ == '__main__' :

    outputdir = './plots/InterCalib_2017/'
    if not os.path.exists(outputdir) :
	os.system('mkdir -p '+outputdir)
	
    #SelectedMC = dict_Summer16
    SelectedMC = dict_Fall17

    #Muon pixel Dedx
    #hists = ['hTrkPixelDedx_tightmumatch','hTrkPixelDedx_tightmumatch_barrel','hTrkPixelDedx_tightmumatch_endcap','hTrkPixelDedxCalib_tightmumatch','hTrkPixelDedxCalib_tightmumatch_barrel','hTrkPixelDedxCalib_tightmumatch_endcap']
    hists = ['hTrkPixelDedx_tightmumatch','hTrkPixelDedx_tightmumatch_barrel','hTrkPixelDedx_tightmumatch_endcap']
    for hist in hists:
	#SelectedData = dict_Run2016_SingleMuon
	SelectedData = dict_Run2017_SingleMuon
	main(SelectedData,SelectedMC,hist,outputdir)
    
    #Muon strips Dedx
    #hists = ['hTrkStripsDedx_tightmumatch','hTrkStripsDedx_tightmumatch_barrel','hTrkStripsDedx_tightmumatch_endcap','hTrkStripsDedxCalib_tightmumatch','hTrkStripsDedxCalib_tightmumatch_barrel','hTrkStripsDedxCalib_tightmumatch_endcap']
    hists = ['hTrkStripsDedx_tightmumatch','hTrkStripsDedx_tightmumatch_barrel','hTrkStripsDedx_tightmumatch_endcap']
    for hist in hists:
	#SelectedData = dict_Run2016_SingleMuon
	SelectedData = dict_Run2017_SingleMuon
	main(SelectedData,SelectedMC,hist,outputdir)
   
    #Electron pixel Dedx
    #hists = ['hTrkPixelDedx_tightelematch','hTrkPixelDedx_tightelematch_barrel','hTrkPixelDedx_tightelematch_endcap','hTrkPixelDedxCalib_tightelematch','hTrkPixelDedxCalib_tightelematch_barrel','hTrkPixelDedxCalib_tightelematch_endcap']
    hists = ['hTrkPixelDedx_tightelematch','hTrkPixelDedx_tightelematch_barrel','hTrkPixelDedx_tightelematch_endcap']
    for hist in hists:
	#SelectedData = dict_Run2016_SingleElectron
	SelectedData = dict_Run2017_SingleElectron
	main(SelectedData,SelectedMC,hist,outputdir)
   
    #Electron Strips Dedx
    #hists = ['hTrkStripsDedx_tightelematch','hTrkStripsDedx_tightelematch_barrel','hTrkStripsDedx_tightelematch_endcap','hTrkStripsDedxCalib_tightelematch','hTrkStripsDedxCalib_tightelematch_barrel','hTrkStripsDedxCalib_tightelematch_endcap']
    hists = ['hTrkStripsDedx_tightelematch','hTrkStripsDedx_tightelematch_barrel','hTrkStripsDedx_tightelematch_endcap']
    for hist in hists:
	#SelectedData = dict_Run2016_SingleElectron
	SelectedData = dict_Run2017_SingleElectron
	main(SelectedData,SelectedMC,hist,outputdir)
   
