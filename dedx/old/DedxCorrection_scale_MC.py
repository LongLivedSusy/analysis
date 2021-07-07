import os,sys
from ROOT import *
from glob import glob
from natsort import natsorted,ns

gROOT.SetBatch(1)
gStyle.SetOptStat(False)
gStyle.SetOptFit(1111)

#format_c = 'pdf'
format_c = 'png'

def main(SelectedData,SelectedMC,hist,outputdir,isFastSim):

    c = TCanvas('c','',800,600)
    c2 = TCanvas('c2','',800,600)
    tl = TLegend(0.6,0.6,0.9,0.9)
    
    fin={}
    hDedx={}
     
    c.cd()

    # standard candle MC : Summer16
    i = 0
    for name,f in sorted(SelectedMC.items()):
        fin[name] = TFile(f)
	hDedx[name] = fin[name].Get('hTrkPixelDedx_fromZ_barrel') #MC : FullSim muon-matched track dEdx at barrel region as standard candle
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
    
    fitres_standard = hDedx_standard.Fit('gaus','S','',2.3,3.5)
    fitres_standard.Print()
    mean_standard = hDedx_standard.GetFunction('gaus').GetParameter(1)
    tl.AddEntry(hDedx_standard, 'Summer16 MC barrel, mu=%s'%(round(mean_standard,3)))
    hDedx_standard.Draw('HIST E SAME')
    c.SaveAs(outputdir+'/Intercalib_Summer16_'+hist+'.'+format_c)
    
     
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
    
    if isFastSim and not 'Calib' in hist : 
        fitres_totalMC = hDedx_totalMC.Fit('gaus','S','',4.0,5.5)
    elif isFastSim and 'Calib' in hist: 
        fitres_totalMC = hDedx_totalMC.Fit('gaus','S','',2.5,3.5)
    else :
        fitres_totalMC = hDedx_totalMC.Fit('gaus','S','',2.3,3.5)
    
    fitres_totalMC.Print()
    mean_totalMC = hDedx_totalMC.GetFunction('gaus').GetParameter(1)
    
    hDedx_totalMC.Draw('HIST E SAME')
    c.SaveAs(outputdir+'/Intercalib_totalMC_'+hist+'.'+format_c)
    
    #c2.cd()
    #rp = TRatioPlot(hDedx_standard,hDedx_totalMC)
    #rp.Draw()
    #hDedx_totalMC.SetTitle('harmonic-2 pixel dEdx')
    #hDedx_standard.SetTitle('harmonic-2 pixel dEdx')
    #hDedx_totalMC.SetLineColor(kRed)
    #hDedx_standard.SetFillStyle(3002)
    #hDedx_standard.SetFillColor(kBlue)
    #rp.GetUpperRefYaxis().SetTitle("Normalized");
    #rp.GetUpperRefYaxis().SetRangeUser(0,0.15);
    #rp.GetLowerRefYaxis().SetTitle("ratio");
    #rp.GetLowerRefYaxis().SetRangeUser(0,2);
    ##tl.AddEntry(hDedx_totalMC,'FastSim MC, mu=%s'%(round(mean_totalMC,3)),'l')
    ##tl.AddEntry(hDedx_totalMC,'Fall17 MC, mu=%s'%(round(mean_totalMC,3)),'l')
    #tl.Draw()
    #c2.SaveAs(outputdir+'/RatioPlot_'+hist+'.'+format_c)
   
    # Extract Scale Factor 
    with open(outputdir+"/ScaleFactor"+hist+".txt",'w') as txt:
	SF = round(mean_standard / mean_totalMC, 3)
        print "'This MC' : %s,"%(SF)
	txt.write("'This MC' : %s,\n"%(SF))


     
    
if __name__ == '__main__' :

    from Dict_datasets import *
    #from Dict_datasets_MIH import *
    
    #DataSets = ["Summer16"]
    DataSets = ["Summer16PrivateFastSim"]
    #DataSets = ["Fall17"]
    #DataSets = ["Summer16","Fall17"]

    for	data in DataSets:
        outputdir = './DedxScale_'+data
        #outputdir = './DedxScale_'+data+'_MIH'
	if not os.path.exists(outputdir) : os.system('mkdir -p '+outputdir)
    	   
	if data == "Summer16":
	    SelectedMC = dict_Summer16
	    SelectedData = dict_Summer16
            isFastSim=False
	elif data == "Summer16PrivateFastSim":
	    SelectedMC = dict_Summer16
	    SelectedData = dict_Summer16_PrivateFastSimSignal
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
		'hTrkPixelDedx_fromZ_barrel',
		'hTrkPixelDedx_fromZ_endcap',
		]
	
	# Run
	for hist in hists:
	    main(SelectedData,SelectedMC,hist,outputdir,isFastSim)

