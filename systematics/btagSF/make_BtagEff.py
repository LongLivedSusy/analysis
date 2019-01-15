import os, sys
from ROOT import *
from glob import glob
import numpy as np

infilename = '/pnfs/knu.ac.kr/data/cms/store/user/ssekmen/distrack/BGMC/Production2016v2/Summer16.TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_*_RA2AnalysisTree.root'

t = TChain("TreeMaker2/PreSelection")
filenamelist = glob(infilename)
print 'adding', filenamelist
filelist = []
for filename in filenamelist :
    fname = filename.strip()
    t.Add(fname)

nentries = t.GetEntries()
print "nentries :",nentries


verbosity = 1000

# for data 2016 and 80X MC
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80XReReco
DeepCSVL = 0.2219
DeepCSVM = 0.6324
DeepCSVT = 0.8958

xbins = np.array([20,30,50,70,140,200,300,600,1000],dtype='f')
nbinsx = len(xbins)-1
ybins = np.array([-2.4,-2.0,-1.6,-1.2,-0.8,-0.4,0.0,0.4,0.8,1.2,1.6,2.0,2.4],dtype='f')
nbinsy = len(ybins)-1

h2_nb = TH2F("nb","nb",nbinsx,xbins,nbinsy,ybins)
h2_nb_btag = TH2F("nb_btag","nb_btag",nbinsx,xbins,nbinsy,ybins)
h2_nc = TH2F("nc","nc",nbinsx,xbins,nbinsy,ybins)
h2_nc_btag = TH2F("nc_btag","nc_btag",nbinsx,xbins,nbinsy,ybins)
h2_nudsg = TH2F("nudsg","nudsg",nbinsx,xbins,nbinsy,ybins)
h2_nudsg_btag = TH2F("nudsg_btag","nudsg_btag",nbinsx,xbins,nbinsy,ybins)

#define variable which will store number of particles in each pT,eta region, initialize 0
nb=np.zeros((nbinsx,nbinsy))
nc=np.zeros((nbinsx,nbinsy))
nudsg=np.zeros((nbinsx,nbinsy))
nb_btag=np.zeros((nbinsx,nbinsy))
nc_btag=np.zeros((nbinsx,nbinsy))
nudsg_btag=np.zeros((nbinsx,nbinsy))

for ientry in range(nentries) :
#for ientry in range(1000) :
    if ientry % verbosity ==0: print ientry, 'events passing'
    t.GetEntry(ientry)

    for ijet, jet in enumerate(t.Jets) :
	#print ientry,'th event', ijet, 'th jet', 'b_Disc :', t.Jets_bDiscriminatorCSV[ijet], '\thadron flavor:', t.Jets_hadronFlavor[ijet], '\tisTagged : ', True if t.Jets_bDiscriminatorCSV[ijet]>DeepCSVM else False
	if jet.Pt() < 20 : continue

	# Fill 2D : b,c,light quarks and b-tagged(medium WP) quark in each pT,eta region
	if t.Jets_hadronFlavor[ijet]==5: # truth b particle
	    h2_nb.Fill(jet.Pt(),jet.Eta())
	    if t.Jets_bDiscriminatorCSV[ijet]>DeepCSVM : # btagged particle
		h2_nb_btag.Fill(jet.Pt(),jet.Eta())
	elif t.Jets_hadronFlavor[ijet]==4: # truth c particle
	    h2_nc.Fill(jet.Pt(),jet.Eta())
	    if t.Jets_bDiscriminatorCSV[ijet]>DeepCSVM : # btagged particle
		h2_nc_btag.Fill(jet.Pt(),jet.Eta())
	elif t.Jets_hadronFlavor[ijet]==0: # truth udsg particle
	    h2_nudsg.Fill(jet.Pt(),jet.Eta())
	    if t.Jets_bDiscriminatorCSV[ijet]>DeepCSVM : # btagged particle
		h2_nudsg_btag.Fill(jet.Pt(),jet.Eta())
	else : print 'wired jet hadronFlavor'



'''
	# CHEKCS :counting number of b,c,light quarks and b-tagged(medium WP) quark in each pT,eta region
	for i in range(nbinsx): # loop for pt bin
	    for j in range(nbinsy): # loop for eta bin
		if t.Jets_hadronFlavor[ijet]==5: # truth b particle
		    if xbins[i]<jet.Pt()<=xbins[i+1] and ybins[j]<jet.Eta()<=ybins[j+1] : #pt,eta region
			nb[i][j]+=1 # number of truth b
			if t.Jets_bDiscriminatorCSV[ijet]>DeepCSVM : # btagged particle
			#print '%s event ijet %s, truth b , region:pt[%s,%s],eta[%s,%s]\tjetpt:%s,\tjeteta:%s'%(ientry,ijet,xbins[i],xbins[i+1],ybins[j],ybins[j+1],jet.Pt(),jet.Eta())
			    nb_btag[i][j]+=1 # number of truth b & b_Discriminator passed
		elif t.Jets_hadronFlavor[ijet]==4: # truth c particle
		    if xbins[i]<jet.Pt()<=xbins[i+1] and ybins[j]<jet.Eta()<=ybins[j+1] : #pt,eta region
			nc[i][j]+=1 # number of truth c
			#print '%s event ijet %s, truth c, region:pt[%s,%s],eta[%s,%s]\tjetpt:%s,\tjeteta:%s'%(ientry,ijet,xbins[i],xbins[i+1],ybins[j],ybins[j+1],jet.Pt(),jet.Eta())
			if t.Jets_bDiscriminatorCSV[ijet]>DeepCSVM : # btagged particle
			    nc_btag[i][j]+=1 # number of truth b & b_Discriminator passed
		elif t.Jets_hadronFlavor[ijet]==0: # truth udsg particle
		    if xbins[i]<jet.Pt()<=xbins[i+1] and ybins[j]<jet.Eta()<=ybins[j+1] : #pt,eta region
			nudsg[i][j]+=1 # number of truth udsg
			#print '%s event ijet %s, truth udsg, region:pt[%s,%s],eta[%s,%s]\tjetpt:%s,\tjeteta:%s'%(ientry,ijet,xbins[i],xbins[i+1],ybins[j],ybins[j+1],jet.Pt(),jet.Eta())
			if t.Jets_bDiscriminatorCSV[ijet]>DeepCSVM : # btagged particle
			    nudsg_btag[i][j]+=1 # number of truth udsg & b_Discriminator passed
		else : print 'hahaha'
	
	#print '===================nb======================'
	#print nb
	#print '===================nc======================'
	#print nc
	#print '===================nudsg======================'
	#print nudsg
	#print '========================================='
	#print '========================================='
'''

h2_eff_b = TH2F()
h2_eff_c = TH2F()
h2_eff_udsg = TH2F()

#Calculate efficiency : n/n_btagged
h2_eff_b = h2_nb_btag.Clone()
h2_eff_b.Divide(h2_nb)
h2_eff_b.SetNameTitle("eff_b","eff_b")
h2_eff_b.SetOption("COLZ")
h2_eff_b.SetStats(False)

h2_eff_c = h2_nc_btag.Clone()
h2_eff_c.Divide(h2_nc)
h2_eff_c.SetNameTitle("eff_c","eff_c")
h2_eff_c.SetOption("COLZ")
h2_eff_c.SetStats(False)

h2_eff_udsg = h2_nudsg_btag.Clone()
h2_eff_udsg.Divide(h2_nudsg)
h2_eff_udsg.SetNameTitle("eff_udsg","eff_udsg")
h2_eff_udsg.SetOption("COLZ")
h2_eff_udsg.SetStats(False)

# Save in root file
newfilename = 'BTagEfficiency_Summer16_TTJets.root'
fout = TFile(newfilename,"RECREATE")
h2_nb.Write()
h2_nb_btag.Write()
h2_nc.Write()
h2_nc_btag.Write()
h2_nudsg.Write()
h2_nudsg_btag.Write()
h2_eff_b.Write()
h2_eff_c.Write()
h2_eff_udsg.Write()
fout.Close()

print "enter any key to quit"
raw_input()

