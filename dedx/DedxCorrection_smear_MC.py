import os,sys
import math
from ROOT import *
from glob import glob
from natsort import natsorted,ns

gROOT.SetBatch(1)
gStyle.SetOptStat(0)
gStyle.SetOptFit(1111)

#format_c = 'pdf'
format_c = 'png'

def main(SelectedData,SelectedMC,hist,outputdir,foutname):

    print 'Running for data:',natsorted(SelectedData)
    print 'hist:',hist
    print 'outputdir:',outputdir
    print 'foutname:',foutname

    c = TCanvas('c','',800,600)
    c_mc = TCanvas('c_mc','',800,600)
    tl = TLegend(0.5,0.6,0.9,0.9)
    
    fin={}
    hDedx_dict={}
    mean={}
    sigma={}
    
    c.cd()
    i=0
    for name,f in natsorted(SelectedData.items()):
        fin[name] = TFile(f)
        hDedx_dict[name] = fin[name].Get(hist)
	if i==0 :
	    print 'Cloning ',name
	    hDedx_data = hDedx_dict[name].Clone()
	else :
	    print 'Adding ', name
	    hDedx_data.Add(hDedx_dict[name])
	i=i+1
    
    i=0
    for name,f in natsorted(SelectedMC.items()):
        fin[name] = TFile(f)
        hDedx_dict[name] = fin[name].Get(hist)
	if i==0 :
	    print 'Cloning ',name
	    hDedx_mc = hDedx_dict[name].Clone()
	else :
	    print 'Adding ', name
	    hDedx_mc.Add(hDedx_dict[name])
	i=i+1
    
    hDedx_data.Scale(1.0/hDedx_data.Integral())
    hDedx_mc.Scale(1.0/hDedx_mc.Integral())
    
    if 'barrel' in hist : 
	   fitres_data = hDedx_data.Fit('gaus','S','',2.0,3.8)
	   fitres_mc = hDedx_mc.Fit('gaus','S','',2.0,3.8)
    elif 'endcap' in hist : 
	   fitres_data = hDedx_data.Fit('gaus','S','',2.0,3.8)
	   fitres_mc = hDedx_mc.Fit('gaus','S','',2.2,3.6)
    else : print 'something wrong'; quit()
    	   
    fitres_data.Print()
    fitres_mc.Print()
    
    mean_data = hDedx_data.GetFunction('gaus').GetParameter(1)
    sigma_data = hDedx_data.GetFunction('gaus').GetParameter(2)
    mean_mc = hDedx_mc.GetFunction('gaus').GetParameter(1)
    sigma_mc = hDedx_mc.GetFunction('gaus').GetParameter(2)

    sigma_smear = TMath.Sqrt(sigma_data**2-sigma_mc**2)
    if math.isnan(sigma_smear):
	print 'sigma_smear is nan'
	quit()
    

    fsmear = TF1("fsmear","gaus",-1,1)
    fsmear.SetParameters(1,0,sigma_smear)

    hsmear = TH1F('hsmear','',200,-1,1)
    hsmear.FillRandom('fsmear',10000)

    fout = TFile(outputdir+'/'+foutname,'recreate')
    hsmear.Write()
    fsmear.Write()
   
    pngname_data = foutname.replace('.root','_data.png')
    c.cd()
    hDedx_data.Draw()
    c.SaveAs(outputdir+'/'+pngname_data)
    
    c.Clear()
    
    pngname_mc = foutname.replace('.root','_mc.png')
    hDedx_mc.Draw()
    c.SaveAs(outputdir+'/'+pngname_mc)

if __name__ == '__main__' :
    
    #from Dict_datasets import *
    from Dict_datasets_MIH import *
    
    outputdir = './DedxSmear_MIH/'
    if not os.path.exists(outputdir) : os.system('mkdir -p '+outputdir)
    
    # Run
    main(dict_Run2016_SingleMuon,dict_Summer16,"hTrkPixelDedxScale_fromZ_barrel",outputdir,"phase0_dedxsmear_barrel.root")
    main(dict_Run2016_SingleMuon,dict_Summer16,"hTrkPixelDedxScale_fromZ_endcap",outputdir,"phase0_dedxsmear_endcap.root")
    main(dict_Run2017_SingleMuon,dict_Fall17,"hTrkPixelDedxScale_fromZ_barrel",outputdir,"phase1_dedxsmear_barrel.root")
    main(dict_Run2017_SingleMuon,dict_Fall17,"hTrkPixelDedxScale_fromZ_endcap",outputdir,"phase1_dedxsmear_endcap.root")
