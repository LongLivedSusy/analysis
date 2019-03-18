#!/usr/bin/env python
import os, sys
from ROOT import *
from array import array
from glob import glob

gROOT.SetBatch(1)

#----------------------------------------------------------------------------------
# Configurable parameters

pathToInputFiles = '/pnfs/knu.ac.kr/data/cms/store/user/spak/DisappTrks/outputs/TREE/'
inputFileSubdirectory = 'TreeMaker2/PreSelection'
outputFileSuffix = 'bTaggingEfficiencyMap'

datasets = [
  # Background
  #[
  #  '/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/jpilot-TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola-Summer12_DR53X-PU_S10-fe5dcf8cf2a24180bf030f68a7d97dda/USER', # dataset name
  #  {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],  # jet Pt and |eta| bins for b jets
  #   'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],  # jet Pt and |eta| bins for c jets
  #   'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},  # jet Pt and |eta| bins for udsg jets
  #  'AK4PF_DeepCSVM'
  #],
  # Signal
  [
    '/g1800_chi1400_27_200970_step4_100',
    {'b':    [[30,50,70,100,140,200,300,1000],[-2.4,-2.0,-1.6,-1.2,-0.8,-0.4,0.0,0.4,0.8,1.2,1.6,2.0,2.4]],
     'c':    [[30,50,70,100,140,200,300,1000],[-2.4,-2.0,-1.6,-1.2,-0.8,-0.4,0.0,0.4,0.8,1.2,1.6,2.0,2.4]],
     'udsg': [[30,50,70,100,140,200,300,600,1000],[-2.4,-2.0,-1.6,-1.2,-0.8,-0.4,0.0,0.4,0.8,1.2,1.6,2.0,2.4]]},
     'DeepCSVM'
  ]
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

def produceEfficiencyMaps(dataset, inputPath, subdirectory, suffix):
    
    inputFilename = os.path.join(inputPath, dataset[0].lstrip('/').replace('/','__') + '.root')
    
    outputFilename = dataset[0].split('/')[1] + '_' + dataset[2] + '_' + suffix + '.root'
    outputFile = TFile(outputFilename, 'RECREATE')
    
    t = TChain(subdirectory)
    filenamelist = glob(inputFilename)
    print 'adding', filenamelist
    [t.Add(fname) for fname in filenamelist]
    
    nentries = min(1000000,t.GetEntries())
    print "nentries:",nentries
    
    verbosity = 1000
    
    # for 2016 data and 80X MC
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80XReReco
    if	    'DeepCSVL' in dataset[2]:   CSV = 0.2219
    elif    'DeepCSVM' in dataset[2]:   CSV = 0.6324
    elif    'DeepCSVT' in dataset[2]:   CSV = 0.8958
    else:   print 'No CSV specified'
    
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
        if ientry %verbosity==0: print ientry, 'events passing'
        t.GetEntry(ientry)
    
        if not t.MHT  > 200: continue
        if not t.HT   > 100: continue
    
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


def main():

  for dataset in datasets:
    produceEfficiencyMaps(dataset, pathToInputFiles, inputFileSubdirectory, outputFileSuffix)

if __name__ == "__main__":
  main()
