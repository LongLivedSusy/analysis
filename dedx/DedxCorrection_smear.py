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

def main(SelectedData,hist,outputdir,foutname):

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
	    hDedx = hDedx_dict[name].Clone()
	else :
	    print 'Adding ', name
	    hDedx.Add(hDedx_dict[name])
	i=i+1
    
    hDedx.Scale(1.0/hDedx.Integral())
    if 'data' in foutname:
        if 'barrel' in hist : 
	   fitres = hDedx.Fit('gaus','S','',2.0,3.8)
        elif 'endcap' in hist : 
	   fitres = hDedx.Fit('gaus','S','',2.0,3.8)
    elif 'mc' in foutname:
        if 'barrel' in hist : 
	   fitres = hDedx.Fit('gaus','S','',2.2,3.6)
        elif 'endcap' in hist : 
	   fitres = hDedx.Fit('gaus','S','',2.2,3.8)
    else : print 'something wrong'; quit()
    	   
    
    fitres.Print()
    mean = hDedx.GetFunction('gaus').GetParameter(1)
    sigma = hDedx.GetFunction('gaus').GetParameter(2)

    fout = TFile(outputdir+'/'+foutname,'recreate')
    fitres.Write()
   
    pngname = foutname.replace('root','png')
    c.cd()
    hDedx.Draw()
    c.SaveAs(outputdir+'/'+pngname)

if __name__ == '__main__' :
    
    outputdir = './DedxSmear/'
    if not os.path.exists(outputdir) : os.system('mkdir -p '+outputdir)
    
    # Run
    main(dict_Run2016_SingleMuon,"hTrkPixelDedxScale_fromZ_barrel",outputdir,"phase0_data_dedxsmear_barrel.root")
    main(dict_Run2016_SingleMuon,"hTrkPixelDedxScale_fromZ_endcap",outputdir,"phase0_data_dedxsmear_endcap.root")
    main(dict_Summer16_DYJetsToLL,"hTrkPixelDedxScale_fromZ_barrel",outputdir,"phase0_mc_dedxsmear_barrel.root")
    main(dict_Summer16_DYJetsToLL,"hTrkPixelDedxScale_fromZ_endcap",outputdir,"phase0_mc_dedxsmear_endcap.root")
