import os,sys
from ROOT import *
from glob import glob
from natsort import natsorted,ns

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
     
    c_mc.cd() 
    gStyle.SetOptFit(1111)
    # Standard candle MC : Summer16
    i = 0
    for name,f in natsorted(SelectedMC.items()):
        fin[name] = TFile(f)
        hDedx[name] = fin[name].Get("hTrkPixelDedx_fromZ_barrel") # pixel barrel is standard candle
	if 'Strips' in hist : hDedx[name] = fin[name].Get("hTrkStripsDedx_fromZ_barrel") # pixel barrel is standard candle
	if i==0:
	    print 'Cloning ',name
	    hDedx_standard = hDedx[name].Clone('hDedx_standard')
	else : 
	    print 'Adding ',name
	    hDedx_standard.Add(hDedx[name])
	i+=1

    hDedx_standard.SetLineWidth(2)
    hDedx_standard.Scale(1.0/hDedx_standard.Integral())
    hDedx_standard.GetXaxis().SetTitle('MeV/cm')
    hDedx_standard.GetYaxis().SetTitle('Normalized')
    #fitres = hDedx_standard.Fit('gaus','S0','',2.5,3.5)
    fitres = hDedx_standard.Fit('gaus','S','',2.5,3.5)
    fitres.Print()
    mean_mc = hDedx_standard.GetFunction('gaus').GetParameter(1)
    hDedx_standard.Draw('HIST E SAME')
    c_mc.SaveAs(outputdir+'/Intercalib_standardMC.'+format_c)
    
    c.cd()
    gStyle.SetOptFit(1111)
    #Data Intercalib
    for name,f in natsorted(SelectedData.items()):
	print 'name',name
        fin[name] = TFile(f)
        hDedx[name] = fin[name].Get(hist)
        hDedx[name].SetTitle(name+' '+hist)
        hDedx[name].SetLineWidth(2)
        hDedx[name].Scale(1.0/hDedx[name].Integral())
	
	fitrangemin = hDedx[name].GetXaxis().GetBinCenter(hDedx[name].GetMaximumBin())-0.4
	fitrangemax = hDedx[name].GetXaxis().GetBinCenter(hDedx[name].GetMaximumBin())+0.4
	hDedx[name].Fit('gaus','S','',fitrangemin,fitrangemax)
	
	fitres.Print()
        mean[name] = hDedx[name].GetFunction('gaus').GetParameter(1)
	hDedx[name].GetXaxis().SetTitle('MeV/cm')
	hDedx[name].GetYaxis().SetTitle('Normalized')
	hDedx[name].Draw('HIST E SAME')
    	c.SaveAs(outputdir+'/Intercalib_'+name+'_'+hist+'.'+format_c)
     
    # Data all period and MC
    gStyle.SetOptFit(0)
    c2.cd()
    hDedx_standard.SetFillStyle(3002)
    hDedx_standard.SetFillColor(kBlue)
    hDedx_standard.GetYaxis().SetRangeUser(0,0.15)
    hDedx_standard.Draw('HIST E SAME')
    tl.AddEntry(hDedx_standard, 'Summer16 MC, mu=%s'%(round(mean_mc,3)))
    
    i=0
    for name,f in natsorted(SelectedData.items()):
        fin[name] = TFile(f)
        hDedx[name] = fin[name].Get(hist)
        hDedx[name].SetTitle('data period')
        hDedx[name].GetXaxis().SetTitle('MeV/cm')
        hDedx[name].GetYaxis().SetTitle('Normalized')
        hDedx[name].SetLineWidth(2)
        hDedx[name].SetLineColor(i+1)
        hDedx[name].Scale(1.0/hDedx[name].Integral())
	if 'Pixel' in hist:
	    hDedx[name].GetYaxis().SetRangeUser(0,0.15)
    	elif 'Strips' in hist:
	    hDedx[name].GetYaxis().SetRangeUser(0,0.2)
    	hDedx[name].Draw('HIST E SAME')
        tl.AddEntry(hDedx[name],'%s, mu=%s'%(name,round(mean[name],3)),'l')
        i=i+1
    
    tl.Draw('SAME')
    c2.SaveAs(outputdir+'/Intercalib_AllPeriod_'+hist+'.'+format_c)
    
    
    # Extract Scale Factor 
    if not 'Scale' in hist : 
        with open(outputdir+"/CF_"+hist+".txt",'w') as txt:
	    for name,f in natsorted(SelectedData.items()):
		SF = round(mean_mc / mean[name],3)
                print "'%s' : %s,"%(name.split('_')[0], SF)
		txt.write("'%s' : %s,\n"%(name.split('_')[0], SF))
     
    
if __name__ == '__main__' :

    #from Dict_datasets import *
    from Dict_datasets_MIH import *

    #DataSets = ["Run2016"]
    #DataSets = ["Run2017"]
    #DataSets = ["Run2018"]
    DataSets = ["Run2016","Run2017","Run2018"]

    for	data in DataSets:
        #outputdir = './DedxScale_'+data
        outputdir = './DedxScale_'+data+'_MIH'
	if not os.path.exists(outputdir) : os.system('mkdir -p '+outputdir)
    	   
	if data == "Run2016":
	    SelectedMC = dict_Summer16
	    SelectedData = dict_Run2016_SingleMuon
	elif data == "Run2017":
	    SelectedMC = dict_Summer16
    	    SelectedData = dict_Run2017_SingleMuon
	elif data == "Run2018":
	    SelectedMC = dict_Summer16
    	    SelectedData = dict_Run2018_SingleMuon
	else : 
	    print 'wrong data'
	    quit()

	hists=[
		# before calibration
		#'hTrkPixelDedx_fromZ_barrel',
		#'hTrkPixelDedx_fromZ_endcap',
		#'hTrkStripsDedx_fromZ_barrel',
		#'hTrkStripsDedx_fromZ_endcap',

		'hTrkPixelDedxScale_fromZ_barrel',
		'hTrkPixelDedxScale_fromZ_endcap',
		]
	
	# Run
	for hist in hists:
	    main(SelectedData,SelectedMC,hist,outputdir)

