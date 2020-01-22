import os,sys
from ROOT import *
from glob import glob

gROOT.SetBatch(1)
gStyle.SetOptStat(0)

dict_Run2016_MET = {'Run2016B_MET':'./output_mediumchunks_MET_drmu001/Run2016B_MET.root',
		    'Run2016C_MET':'./output_mediumchunks_MET_drmu001/Run2016C_MET.root',
	       	    'Run2016D_MET':'./output_mediumchunks_MET_drmu001/Run2016D_MET.root',
               	    'Run2016E_MET':'./output_mediumchunks_MET_drmu001/Run2016E_MET.root',
               	    'Run2016F_MET':'./output_mediumchunks_MET_drmu001/Run2016F_MET.root',
               	    'Run2016G_MET':'./output_mediumchunks_MET_drmu001/Run2016G_MET.root',
               	    'Run2016H_MET':'./output_mediumchunks_MET_drmu001/Run2016H_MET.root',
		    }

c = TCanvas('Dedx','Dedx',800,600)
tl = TLegend(0.5,0.6,0.9,0.9)

fin={}
hDedx={}
mean={}

i=0
for name,f in sorted(dict_Run2016_MET.items()):
    fin[name] = TFile(f)
    hDedx[name] = fin[name].Get('hTrkDedx_mumatch')
    hDedx[name].SetLineColor(i+1)
    hDedx[name].SetLineWidth(2)
    fitres = hDedx[name].Fit('gaus','S0','',1,4)
    fitres.Print()
    mean[name] = hDedx[name].GetFunction('gaus').GetParameter(1)
    tl.AddEntry(hDedx[name],'%s, mu=%s'%(name,round(mean[name],3)),'l')
    hDedx[name].DrawNormalized('HIST SAME')
    i=i+1

c.SetLogy()
tl.Draw('SAME')
c.SaveAs('./plots/DedxByEras.png')
