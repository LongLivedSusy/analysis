import os,sys
from ROOT import *
from glob import glob
from natsort import natsorted,ns

gROOT.SetBatch(1)
gStyle.SetOptStat(0)
gStyle.SetOptFit(1111)

#format_c = 'pdf'
format_c = 'png'

dict_samples = {
        'Run2016H_SingleMuon':'./output_mediumchunks/Run2016H_SingleMuon.root',
	'WJetsToLNu_TuneCUETP8M1':'./output_mediumchunks/WJetsToLNu_TuneCUETP8M1.root',
	'SMS-T2bt-LLChipm_ctau-200_mLSP-1':'./output_mediumchunks/SMS-T2bt-LLChipm_ctau-200_mLSP-1_.root',
	'SMS-T2bt-LLChipm_ctau-200_mLSP-150':'./output_mediumchunks/SMS-T2bt-LLChipm_ctau-200_mLSP-150_.root',
	#'SMS-T2bt-LLChipm_ctau-200_mLSP-400':'./output_mediumchunks/SMS-T2bt-LLChipm_ctau-200_mLSP-400_.root',
	#'SMS-T2bt-LLChipm_ctau-200_mLSP-1000':'./output_mediumchunks/SMS-T2bt-LLChipm_ctau-200_mLSP-1000_.root',
	#'WJetsToLNu_HT-100To200':'./output_mediumchunks/WJetsToLNu_HT-100To200.root',
	#'WJetsToLNu_HT-200To400':'./output_mediumchunks/WJetsToLNu_HT-200To400.root',
	#'WJetsToLNu_HT-400To600':'./output_mediumchunks/WJetsToLNu_HT-400To600.root',
	#'WJetsToLNu_HT-600To800':'./output_mediumchunks/WJetsToLNu_HT-600To800.root',
	#'WJetsToLNu_HT-800To1200':'./output_mediumchunks/WJetsToLNu_HT-800To1200.root',
	#'WJetsToLNu_HT-1200To2500':'./output_mediumchunks/WJetsToLNu_HT-1200To2500.root',
	#'WJetsToLNu_HT-2500ToInf':'./output_mediumchunks/WJetsToLNu_HT-2500ToInf.root',
	#'DYJetsToLL_M-50_TuneCUETP8M1':'./output_mediumchunks/DYJetsToLL_M-50_TuneCUETP8M1.root',
	#'DYJetsToLL_M-50_HT-100to200':'./output_mediumchunks/DYJetsToLL_M-50_HT-100to200.root',
	#'DYJetsToLL_M-50_HT-200to400':'./output_mediumchunks/DYJetsToLL_M-50_HT-200to400.root',
	#'DYJetsToLL_M-50_HT-400to600':'./output_mediumchunks/DYJetsToLL_M-50_HT-400to600.root',
	#'DYJetsToLL_M-50_HT-600to800':'./output_mediumchunks/DYJetsToLL_M-50_HT-600to800.root',
	#'DYJetsToLL_M-50_HT-800to1200':'./output_mediumchunks/DYJetsToLL_M-50_HT-800to1200.root',
	#'DYJetsToLL_M-50_HT-1200to2500':'./output_mediumchunks/DYJetsToLL_M-50_HT-1200to2500.root',
	#'DYJetsToLL_M-50_HT-2500toInf':'./output_mediumchunks/DYJetsToLL_M-50_HT-2500toInf.root',
	#'QCD_HT200to300':'./output_mediumchunks/QCD_HT200to300.root',
	#'QCD_HT300to500':'./output_mediumchunks/QCD_HT300to500.root',
	#'QCD_HT500to700':'./output_mediumchunks/QCD_HT500to700.root',
	#'QCD_HT700to1000':'./output_mediumchunks/QCD_HT700to1000.root',
	#'QCD_HT1000to1500':'./output_mediumchunks/QCD_HT1000to1500.root',
	#'QCD_HT1500to2000':'./output_mediumchunks/QCD_HT1500to2000.root',
	#'QCD_HT2000toInf':'./output_mediumchunks/QCD_HT2000toInf.root',
	#'TTJets':'./output_mediumchunks/TTJets.root',
	#'WW':'./output_mediumchunks/WW.root',
	#'WZ':'./output_mediumchunks/WZ.root',
	#'ZZ':'./output_mediumchunks/ZZ.root',
	#'ZJetsToNuNu_HT-100To200':'./output_mediumchunks/ZJetsToNuNu_HT-100To200.root',
	#'ZJetsToNuNu_HT-200To400':'./output_mediumchunks/ZJetsToNuNu_HT-200To400.root',
	#'ZJetsToNuNu_HT-400To600':'./output_mediumchunks/ZJetsToNuNu_HT-400To600.root',
	#'ZJetsToNuNu_HT-600To800':'./output_mediumchunks/ZJetsToNuNu_HT-600To800.root',
	#'ZJetsToNuNu_HT-800To1200':'./output_mediumchunks/ZJetsToNuNu_HT-800To1200.root',
	#'ZJetsToNuNu_HT-1200To2500':'./output_mediumchunks/ZJetsToNuNu_HT-1200To2500.root',
	##'ZJetsToNuNu_HT-2500ToInf':'./output_mediumchunks/ZJetsToNuNu_HT-2500ToInf.root',
	}

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

def draw2D(SelectedData,hist,outputdir):

    c = TCanvas('Dedx','Dedx vs P',800,600)
    
    fin={}
    h={}
    
    c.cd()
    for name,f in natsorted(SelectedData.items()):
        fin[name] = TFile(f)
        h[name] = fin[name].Get(hist)
        h[name].SetTitle(name)
        h[name].SetLineWidth(2)
	h[name].Draw('COLZ')
	h[name].GetXaxis().SetTitle('P');
	h[name].GetYaxis().SetTitle('dEdx');
	h[name].GetXaxis().SetRangeUser(0.,1000);
    	c.SaveAs(outputdir+'/2D_'+name+'_'+hist+'.'+format_c)
    
def draw3D(SelectedData,hist,outputdir):

    c = TCanvas('3D','P vs Eta vs Dedx',800,600)
    
    fin={}
    h={}
    
    c.cd()
    for name,f in natsorted(SelectedData.items()):
        fin[name] = TFile(f)
        h[name] = fin[name].Get(hist)
        h[name].SetTitle(name)
        h[name].SetLineWidth(2)
	#h[name].Draw('')
	h[name].Draw('BOX')
	h[name].GetXaxis().SetTitle('P');
	h[name].GetYaxis().SetTitle('Eta');
	h[name].GetZaxis().SetTitle('dEdx');
	h[name].GetXaxis().SetRangeUser(0.,1000);
    	c.SaveAs(outputdir+'/3D_'+name+'_'+hist+'.'+format_c)
    
if __name__ == '__main__' :

    hists = ['h2_TrkMu_P_Dedx','h2_TrkEle_P_Dedx','h2_TrkChi_P_Dedx']
    for hist in hists:
	SelectedData = dict_samples
    	outputdir = './2Dplots'
	
	draw2D(SelectedData,hist,outputdir)
    
    hists = ['h3_TrkMu_P_Eta_Dedx','h3_TrkEle_P_Eta_Dedx','h3_TrkChi_P_Eta_Dedx']
    for hist in hists:
	SelectedData = dict_samples
    	outputdir = './2Dplots'
	
	draw3D(SelectedData,hist,outputdir)
    
