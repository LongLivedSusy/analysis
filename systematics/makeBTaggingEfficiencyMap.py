#!/usr/bin/env python
import os, sys
from ROOT import *
from array import array
from glob import glob

gROOT.SetBatch(1)
gStyle.SetOptStat(0)

#----------------------------------------------------------------------------------
# Configurable parameters

pathToInputFiles = '/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/'
inputFileSubdirectory = 'TreeMaker2/PreSelection'
outputFileSuffix = 'bTaggingEfficiencyMap'

binning = {
'b':	[[30,50,70,100,140,200,300,1000],   [-2.4,-2.0,-1.6,-1.2,-0.8,-0.4,0.0,0.4,0.8,1.2,1.6,2.0,2.4]],
'c':	[[30,50,70,100,140,200,300,1000],   [-2.4,-2.0,-1.6,-1.2,-0.8,-0.4,0.0,0.4,0.8,1.2,1.6,2.0,2.4]],
'udsg':	[[30,50,70,100,140,200,300,600,1000],[-2.4,-2.0,-1.6,-1.2,-0.8,-0.4,0.0,0.4,0.8,1.2,1.6,2.0,2.4]]
}

datasets = [
  # Background
  #[
  #  '/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/jpilot-TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola-Summer12_DR53X-PU_S10-fe5dcf8cf2a24180bf030f68a7d97dda/USER', # dataset name
  #  {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],  # jet Pt and |eta| bins for b jets
  #   'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],  # jet Pt and |eta| bins for c jets
  #   'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},  # jet Pt and |eta| bins for udsg jets
  #  'AK4PF_DeepCSVM'
  #],
  
  # Signal - T1qqqq
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-25_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-50_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-75_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-150_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-200_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-400_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-600_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-800_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-900_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-975_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1000_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1075_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1175_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1200_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1275_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1300_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1375_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1400_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1475_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1500_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1575_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1600_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1675_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1700_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1775_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1800_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1875_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1900_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1975_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2000_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2075_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2100_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2175_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2200_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2275_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2300_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2375_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2400_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2475_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2500_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2575_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2600_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2675_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2700_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2775_', binning, 'DeepCSVM'], 

  # Signal - T2bt
  ['RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-50_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-100_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-150_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-200_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-400_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-600_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-800_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-900_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1000_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1100_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1200_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1300_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1400_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1500_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1600_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1700_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1800_', binning, 'DeepCSVM'], 
  ['RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-2000_', binning, 'DeepCSVM'], 
]
#----------------------------------------------------------------------------------

def FillHisto(hist, valx, valy): 
    nbinsx=hist.GetNbinsX();
    minvalx=hist.GetXaxis().GetBinCenter(1);
    maxvalx=hist.GetXaxis().GetBinCenter(nbinsx);
    
    nbinsy=hist.GetNbinsY();
    minvaly=hist.GetYaxis().GetBinCenter(1);
    maxvaly=hist.GetYaxis().GetBinCenter(nbinsy);
    
    newvalx=valx;
    newvaly=valy;
    
    if(valx< minvalx) : newvalx=minvalx;
    elif(valx>maxvalx): newvalx=maxvalx;
    
    if(valy< minvaly) : newvaly=minvaly;
    elif(valy>maxvaly): newvaly=maxvaly;
    
    hist.Fill(newvalx, newvaly);

def produceEfficiencyMaps(dataset, inputPath, subdirectory, outputDir, suffix):
    
    inputFilename = os.path.join(inputPath, dataset[0] + '*.root')
    
    outputFilename = dataset[0] + dataset[2] + '_' + suffix + '.root'
    outputFile = TFile(outputDir+'/'+outputFilename, 'RECREATE')
    
    t = TChain(subdirectory)
    filenamelist = glob(inputFilename)
    for fname in filenamelist : 
	print 'adding', fname
	t.Add(fname)
    
    nentries = min(100000,t.GetEntries())
    print "nentries:",nentries
    
    verbosity = 1000
    
    # for 2016 data and 80X MC
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80XReReco
    if	    'DeepCSVL' in dataset[2]:   CSV = 0.2219
    elif    'DeepCSVM' in dataset[2]:   CSV = 0.6324
    elif    'DeepCSVT' in dataset[2]:   CSV = 0.8958
    else:   print 'No CSV specified'

    print 'Using CSV : ',dataset[2]
    
    # Histogram for each flavor
    # Pt, Eta 2D histo
    dict_partonFlavor = {0:'b', 1:'c', 2:'udsg'} 
    denominatorHisto=[]
    numeratorHisto=[]
    efficiencyHisto=[]
    for key, value in dict_partonFlavor.iteritems():
        binsX = array('d', dataset[1][value][0])
        binsY = array('d', dataset[1][value][1])
        
        denominatorHisto.append(TH2D('denominator_' + value, '', (len(binsX)-1), binsX, (len(binsY)-1), binsY))
        numeratorHisto.append(TH2D('numerator_' + value, '', (len(binsX)-1), binsX, (len(binsY)-1), binsY))
        efficiencyHisto.append(TH2D())
    
    # Loop events
    for ientry in range(nentries):
    #for ientry in range(10):
        if ientry %verbosity==0: print ientry, 'events passing'
        t.GetEntry(ientry)

	if not (bool(t.JetID) and  t.NVtx>0): continue
	
	if 'T1qqqq' in inputFilename :  
	    if not t.MHT  > 150: continue
	
	for ijet, jet in enumerate(t.Jets):
	    if jet.Pt()	< 30: continue
	    if t.Jets_hadronFlavor[ijet]==5:
	        FillHisto(denominatorHisto[0], jet.Pt(), jet.Eta())
	        if t.Jets_bDiscriminatorCSV[ijet]>CSV :
		   FillHisto(numeratorHisto[0], jet.Pt(), jet.Eta())
	    elif t.Jets_hadronFlavor[ijet]==4:
	        FillHisto(denominatorHisto[1], jet.Pt(), jet.Eta())
	        if t.Jets_bDiscriminatorCSV[ijet]>CSV :
		   FillHisto(numeratorHisto[1], jet.Pt(), jet.Eta())
	    elif t.Jets_hadronFlavor[ijet]==0:
	        FillHisto(denominatorHisto[2], jet.Pt(), jet.Eta())
	        if t.Jets_bDiscriminatorCSV[ijet]>CSV :
		   FillHisto(numeratorHisto[2], jet.Pt(), jet.Eta())
   
    # Efficiency histogram
    for key, value in dict_partonFlavor.iteritems():
	efficiencyHisto[key] = numeratorHisto[key].Clone()
	efficiencyHisto[key].Divide(denominatorHisto[key])
	efficiencyHisto[key].SetNameTitle('efficiency_'+value,'')
	efficiencyHisto[key].SetOption("COLZ")

    # check if there are any bins with 0 or 100% efficiency
    for i in range(1,denominatorHisto[key].GetXaxis().GetNbins()+1):
	for j in range(1,denominatorHisto[key].GetYaxis().GetNbins()+1):
	    efficiency = efficiencyHisto[key].GetBinContent(i,j)
	    if(efficiency==0. or efficiency==1.):
		print 'Warning! Bin(%i,%i) for %s jets has a b-tagging efficiency of %.3f'%(i,j,value,efficiency)
	
    
    outputFile.cd()
    
    for key in range(len(dict_partonFlavor)):
	denominatorHisto[key].Write()
	numeratorHisto[key].Write()
	efficiencyHisto[key].Write()

    outputFile.Close()
    print '-------------------------------------------------------------------------------------------'
    print 'b-tagging efficiency map for'
    print dataset[0]
    print 'successfully created and stored in %s'%outputFilename
    print ''


if __name__ == "__main__":
    
    outputDir = './BtagEffMaps/'
    
    if not os.path.exists(outputDir):
	print 'Making outputDir : ', outputDir
	os.system('mkdir -p '+ outputDir)
    else : print 'outputDir {} exists'.format(outputDir)

    for dataset in datasets:
	produceEfficiencyMaps(dataset, pathToInputFiles, inputFileSubdirectory, outputDir, outputFileSuffix)
