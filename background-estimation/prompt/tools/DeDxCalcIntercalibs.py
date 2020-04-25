from ROOT import *
from utils import *
import os, sys
gStyle.SetOptStat(0)
#gROOT.SetBatch(1)

#f = TFile('PromptBkgHist_Summer16.WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1AOD_70000-F85B7AB3-5BC6-E611-909F-02163E013D4E_-SmearLeps4ZedTrue-nfpj100.root')
#f = TFile('output/totalweightedbkgsDataDrivenMCSmearLeps4ZedFalse.root')
#f = TFile('output/totalweightedbkgsDataDrivenSingleEllectronData.root')
#f = TFile('output/totalweightedbkgsDataDrivenSingleMuDataNoSmear.root')
#headfile = TFile('output/totalweightedbkgsDataDrivenMETDataNoSmear.root')

datastream = 'SingleEl'
phase = 0

if phase == 0:
	filenames = ['output/totalweightedRun2016B'+datastream+'.root',\
				  'output/totalweightedRun2016C'+datastream+'.root',\
				  'output/totalweightedRun2016D'+datastream+'.root',\
				  'output/totalweightedRun2016E'+datastream+'.root',\
				  'output/totalweightedRun2016F'+datastream+'.root',\
				  'output/totalweightedRun2016G'+datastream+'.root',\
				  'output/totalweightedRun2016H'+datastream+'.root',\
				  'output/totalweightedbkgsDataDrivenMCSmearLeps4ZedFalse.root']
				  
if phase == 1:
	filenames = [ 'output/totalweightedRun2016H'+datastream+'.root',\
				  'output/totalweightedRun2017B'+datastream+'.root',\
				  'output/totalweightedRun2017C'+datastream+'.root',\
				  'output/totalweightedRun2017D'+datastream+'.root',\
				  'output/totalweightedRun2017E'+datastream+'.root',\
				  'output/totalweightedRun2017F'+datastream+'.root',\
				  'output/totalweightedRun2018A'+datastream+'.root',\
				  'output/totalweightedRun2018C'+datastream+'.root',\
				  'output/totalweightedRun2018D'+datastream+'.root']
				  			
#				  'output/totalweightedRun2018B'+datastream+'.root',\ doesn't exist?
				  			
files = []
for fname in filenames:
	files.append(TFile(fname))
files[0].ls()


print 'files', files

hists = []
#histnames = ['hElNoCutsZone0p0To2p1_DeDxAverageControl']

histnames = ['hElSElValidationZLLZone0p0To2p1_DeDxAverageControl']
histnames = ['hElNoCutsZone0p0To2p1_DeDxAverageControl']
fnew = TFile('calibratedDeDxPromptControlData.root', 'recreate')


colors = [1,2,4, kTeal-5, kYellow, kOrange+1, kGreen-2, kGreen-1, kGreen, kGreen+1, kGreen+2]
c1 = mkcanvas()
c1.SetLogy()
dictstring = ''
for name in histnames:
  leg = mklegend(x1=.52, y1=.6, x2=.95, y2=.82, color=kWhite)
  arg = ''
  precalibdict = {}
  calibdict = {}  
  if not 'Zone0p0To2p1' in name: continue
  shortname = name.split('Zone')[0]+'_'+(''.join(name.split('_')[-1:]))
  shortname = shortname.replace('NoCuts', 'TightLep')
  
  for ifile, file_ in enumerate(files):
  	print 'trying to get', name, 'from', file_.GetName()
	hist = file_.Get(name).Clone(name+str(ifile))
	hists.append(hist.Clone())
	hists[-1].SetDirectory(0)
	hists[-1].SetLineColor(colors[ifile])
	hists[-1].Add(file_.Get(name.replace('Zone0p0To2p1','Zone2p1To4')))
	hists[-1].Add(file_.Get(name.replace('Zone0p0To2p1','Zone4To99')))	
	if hists[-1].Integral()==0: 
		print 'empty hist, continuing'
		continue
	hists[-1].SetTitle('')
	hists[-1].Scale(1.0/hists[-1].Integral())
	fitres = hists[-1].Fit('gaus','S0','S',1.5,3.5)
	#print dir(fitres)
	mean = fitres.Parameters()[1]
	legname = file_.GetName().replace('output/','').replace('.root','').replace('totalweighted','').replace(datastream,'-'+datastream).replace('bigchunks/','').split('Smear')[0]+ ', mu='+str(round(mean,4))
	keyname = legname.split('-'+datastream)[0]
	print 'keyname', keyname
	precalibdict[keyname] = mean
	if phase == 1 and 'Run2016H' in keyname: continue
	leg.AddEntry(hists[-1], legname)
	fnew.cd()
	hists[-1].Write(shortname+'_'+(file_.GetName().split('/')[-1].replace('totalweighted','').replace('.root','')))
	hists[-1].Draw(arg)
	arg = 'same hist'
	print 'made it to the end'
	
  for key in precalibdict:
  	calibdict[key] = precalibdict['Run2016H']/precalibdict[key]
  	
  print calibdict
  stamp()	
  leg.Draw()			
  c1.Update()
  c1.Write('c_'+shortname)
  pause()
print 'just created', fnew.GetName()
fnew.Close()

	


	
