import os,sys
from ROOT import *
from glob import glob
from natsort import natsorted,ns
from Dict_datasets import *

gROOT.SetBatch(1)
gStyle.SetOptStat(0)
gStyle.SetOptFit(1111)

#format_c = 'pdf'
format_c = 'png'

def main(SelectedData,SelectedMC,hist,outputdir):

    print 'Drawing for ',hist
    c = TCanvas('c','',800,600)
    c_mc = TCanvas('c_mc','',800,600)
    c2 = TCanvas('c2','',800,600)
    tl = TLegend(0.5,0.6,0.9,0.9)
    
    fin={}
    hDedx={}
    mean={}
    sigma={}
    smearfunction={}
    
    c.cd()
    #Data
    i=0
    for name,f in natsorted(SelectedData.items()):
        fin[name] = TFile(f)
        hDedx[name] = fin[name].Get(hist)
	if i==0 :
	    print 'Cloning ',name
	    hDedx_data = hDedx[name].Clone('hDedx_data')
	else :
	    print 'Adding ', name
	    hDedx_data.Add(hDedx[name])
	i+=1
    
    #MC
    j=0
    for name,f in natsorted(SelectedMC.items()):
        fin[name] = TFile(f)
        hDedx[name] = fin[name].Get(hist)
	if j==0 :
	    print 'Cloning ',name
	    hDedx_MC = hDedx[name].Clone('hDedx_MC')
	else :
	    print 'Adding ', name
	    hDedx_MC.Add(hDedx[name])
	j+=1

    hDedx_data.Scale(1.0/hDedx_data.Integral())
    hDedx_MC.Scale(1.0/hDedx_MC.Integral())
    fitres_data = hDedx_data.Fit('gaus','S','',1.8,3.2)
    fitres_MC = hDedx_MC.Fit('gaus','S','',2.5,3.5)
    fitres_data.Print()
    fitres_MC.Print()
    mean_data = hDedx_data.GetFunction('gaus').GetParameter(1)
    sigma_data = hDedx_data.GetFunction('gaus').GetParameter(2)
    mean_MC = hDedx_MC.GetFunction('gaus').GetParameter(1)
    sigma_MC = hDedx_MC.GetFunction('gaus').GetParameter(2)

    sigma_smear = TMath.Sqrt((sigma_data*sigma_data) - (sigma_MC*sigma_MC))
    fsmear = TF1('fsmear','gaus',0,2)
    fsmear.SetParameter(0,10000)
    fsmear.SetParameter(1,1)
    fsmear.SetParameter(2,sigma_smear)
    hsmear = TH1F('hsmear','',200,0,2)
    hsmear.FillRandom('fsmear',10000)

    fsmear.Draw()
    hsmear.Draw('hist same')

    if 'barrel' in hist : 
	foutname = 'dedx_for_smear_barrel.root'
	pngname = 'dedx_for_smear_barrel.png'
    elif 'endcap' in hist : 
	foutname = 'dedx_for_smear_endcap.root'
	pngname = 'dedx_for_smear_endcap.png'
    else : print 'something wrong'; quit()

    fout = TFile(outputdir+'/'+foutname,'recreate')
    fsmear.Write()
    hsmear.Write()

    c.SaveAs(outputdir+'/'+pngname)


if __name__ == '__main__' :

    DataSets = ["Run2016"]

    outputdir = './DedxSmear/'
    if not os.path.exists(outputdir) : os.system('mkdir -p '+outputdir)
    
    for	data in DataSets:
    	   
	if "Run2016" in data:
	    SelectedData = dict_Run2016_SingleMuon
	    SelectedMC = dict_Summer16
	else : 
	    print 'wrong data'
	    quit()

	hists=[
		'hTrkPixelDedx_fromZ_barrel',
		'hTrkPixelDedx_fromZ_endcap',
		]
	
	# Run
	for hist in hists:
	    main(SelectedData,SelectedMC,hist,outputdir)

