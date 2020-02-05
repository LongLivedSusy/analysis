import os,sys
from ROOT import *
from glob import glob
from natsort import natsorted,ns

gROOT.SetBatch(1)
gStyle.SetOptStat(0)

#format_c = 'pdf'
format_c = 'png'


dict_Run2016_MET = {'Run2016B_MET':'./output_mediumchunks/Run2016B_MET.root',
		    'Run2016C_MET':'./output_mediumchunks/Run2016C_MET.root',
	       	    'Run2016D_MET':'./output_mediumchunks/Run2016D_MET.root',
               	    'Run2016E_MET':'./output_mediumchunks/Run2016E_MET.root',
               	    'Run2016F_MET':'./output_mediumchunks/Run2016F_MET.root',
               	    'Run2016G_MET':'./output_mediumchunks/Run2016G_MET.root',
               	    'Run2016H_MET':'./output_mediumchunks/Run2016H_MET.root',
		    }

dict_Run2016_SingleMuon = {
		    #'Run2016B_SingleMuon':'./output_mediumchunks/Run2016B_SingleMuon.root',
		    #'Run2016C_SingleMuon':'./output_mediumchunks/Run2016C_SingleMuon.root',
	       	    #'Run2016D_SingleMuon':'./output_mediumchunks/Run2016D_SingleMuon.root',
               	    #'Run2016E_SingleMuon':'./output_mediumchunks/Run2016E_SingleMuon.root',
               	    #'Run2016F_SingleMuon':'./output_mediumchunks/Run2016F_SingleMuon.root',
               	    #'Run2016G_SingleMuon':'./output_mediumchunks/Run2016G_SingleMuon.root',
               	    'Run2016H_SingleMuon':'./output_mediumchunks/Run2016H_SingleMuon.root',
		    }

dict_Run2016_SingleElectron = {
		    #'Run2016B_SingleElectron':'./output_mediumchunks/Run2016B_SingleElectron.root',
		    #'Run2016C_SingleElectron':'./output_mediumchunks/Run2016C_SingleElectron.root',
	       	    #'Run2016D_SingleElectron':'./output_mediumchunks/Run2016D_SingleElectron.root',
               	    #'Run2016E_SingleElectron':'./output_mediumchunks/Run2016E_SingleElectron.root',
               	    #'Run2016F_SingleElectron':'./output_mediumchunks/Run2016F_SingleElectron.root',
               	    #'Run2016G_SingleElectron':'./output_mediumchunks/Run2016G_SingleElectron.root',
               	    'Run2016H_SingleElectron':'./output_mediumchunks/Run2016H_SingleElectron.root',
		    }

dict_SMS_T2bt_LLChipm_ctau_200 = {
    'SMS-T2bt-LLChipm_ctau-200_mLSP-1':'./output_mediumchunks/SMS-T2bt-LLChipm_ctau-200_mLSP-1_.root',
    #'SMS-T2bt-LLChipm_ctau-200_mLSP-50':'./output_mediumchunks/SMS-T2bt-LLChipm_ctau-200_mLSP-50_.root',
    'SMS-T2bt-LLChipm_ctau-200_mLSP-150':'./output_mediumchunks/SMS-T2bt-LLChipm_ctau-200_mLSP-150_.root',
    #'SMS-T2bt-LLChipm_ctau-200_mLSP-200':'./output_mediumchunks/SMS-T2bt-LLChipm_ctau-200_mLSP-200_.root',
    'SMS-T2bt-LLChipm_ctau-200_mLSP-400':'./output_mediumchunks/SMS-T2bt-LLChipm_ctau-200_mLSP-400_.root',
    #'SMS-T2bt-LLChipm_ctau-200_mLSP-600':'./output_mediumchunks/SMS-T2bt-LLChipm_ctau-200_mLSP-600_.root',
    #'SMS-T2bt-LLChipm_ctau-200_mLSP-800':'./output_mediumchunks/SMS-T2bt-LLChipm_ctau-200_mLSP-800_.root',
    #'SMS-T2bt-LLChipm_ctau-200_mLSP-900':'./output_mediumchunks/SMS-T2bt-LLChipm_ctau-200_mLSP-900_.root',
    'SMS-T2bt-LLChipm_ctau-200_mLSP-1000':'./output_mediumchunks/SMS-T2bt-LLChipm_ctau-200_mLSP-1000_.root',
    #'SMS-T2bt-LLChipm_ctau-200_mLSP-1100':'./output_mediumchunks/SMS-T2bt-LLChipm_ctau-200_mLSP-1100_.root',
    #'SMS-T2bt-LLChipm_ctau-200_mLSP-1200':'./output_mediumchunks/SMS-T2bt-LLChipm_ctau-200_mLSP-1200_.root',
    #'SMS-T2bt-LLChipm_ctau-200_mLSP-1300':'./output_mediumchunks/SMS-T2bt-LLChipm_ctau-200_mLSP-1300_.root',
    #'SMS-T2bt-LLChipm_ctau-200_mLSP-1400':'./output_mediumchunks/SMS-T2bt-LLChipm_ctau-200_mLSP-1400_.root',
    #'SMS-T2bt-LLChipm_ctau-200_mLSP-1500':'./output_mediumchunks/SMS-T2bt-LLChipm_ctau-200_mLSP-1500_.root',
    #'SMS-T2bt-LLChipm_ctau-200_mLSP-1600':'./output_mediumchunks/SMS-T2bt-LLChipm_ctau-200_mLSP-1600_.root',
    #'SMS-T2bt-LLChipm_ctau-200_mLSP-1700':'./output_mediumchunks/SMS-T2bt-LLChipm_ctau-200_mLSP-1700_.root',
    #'SMS-T2bt-LLChipm_ctau-200_mLSP-1800':'./output_mediumchunks/SMS-T2bt-LLChipm_ctau-200_mLSP-1800_.root',
    'SMS-T2bt-LLChipm_ctau-200_mLSP-2000':'./output_mediumchunks/SMS-T2bt-LLChipm_ctau-200_mLSP-2000_.root',
    }

#SelectedData = dict_Run2016_SingleMuon
#hist = 'hTrkDedx_tightmumatch'
#outputdir = 'plots_mu'

SelectedData = dict_Run2016_SingleElectron
hist = 'hTrkDedx_tightelematch'
outputdir = 'plots_ele'

c = TCanvas('Dedx','Dedx',800,600)
tl = TLegend(0.5,0.6,0.9,0.9)

fin={}
hDedx={}
mean={}

i=0
for name,f in natsorted(SelectedData.items()):
#for name,f in natsorted(dict_Run2016_SingleElectron.items()):
    fin[name] = TFile(f)
    hDedx[name] = fin[name].Get(hist)
    hDedx[name].SetLineColor(i+1)
    hDedx[name].SetLineWidth(2)
    hDedx[name].Scale(1.0/hDedx[name].Integral())
    fitres = hDedx[name].Fit('gaus','S0','',1.5,3.0)
    fitres.Print()
    mean[name] = hDedx[name].GetFunction('gaus').GetParameter(1)
    tl.AddEntry(hDedx[name],'%s, mu=%s'%(name,round(mean[name],3)),'l')
    if i == 0:
	hDedx[name].SetMinimum(1e-6)
	hDedx[name].SetMaximum(1e1)
	hDedx[name].Draw('HIST E SAME')
	hDedx_total = hDedx[name].Clone('hDedx_total')
    else : 
	hDedx[name].Draw('HIST E SAME')
	hDedx_total.Add(hDedx[name])
    i=i+1

i = 0
for name,f in natsorted(dict_SMS_T2bt_LLChipm_ctau_200.items()):
    fin[name] = TFile(f)
    hDedx[name] = fin[name].Get(hist)
    hDedx[name].SetLineColor(i+2)
    hDedx[name].SetLineWidth(2)
    fitres = hDedx[name].Fit('gaus','S0','',2.0,3.5)
    fitres.Print()
    mean[name] = hDedx[name].GetFunction('gaus').GetParameter(1)
    tl.AddEntry(hDedx[name],'%s, mu=%s'%(name,round(mean[name],3)),'l')
    hDedx[name].DrawNormalized('HIST E SAME')
    if i == 0:
	hDedx_total_sig = hDedx[name].Clone('hDedx_total_sig')
    else : 
	hDedx_total_sig.Add(hDedx[name])
    i=i+1


tl.Draw('SAME')
c.SaveAs(outputdir+'/Normalized_'+hist+'.'+format_c)
c.SetLogy()
c.SaveAs(outputdir+'/Normalized_'+hist+'_Logy.'+format_c)

#c.Clear()
#c.SetLogy(0)
#hDedx_total.DrawNormalized('HIST')
#hDedx_total_sig.DrawNormalized('HIST SAMES')
#fitres_total = hDedx_total.Fit('gaus','S','',1.5,3.5)
#fitres_total.Print()
#fitres_total_sig = hDedx_total_sig.Fit('gaus','S','',2.5,3.3)
#fitres_total_sig.Print()
#c.SaveAs(outputdir+'/Normalized_'+hist+'_total.pdf')
#c.SetLogy(1)
#c.SaveAs(outputdir+'/Normalized_'+hist+'_total_Logy.pdf')

