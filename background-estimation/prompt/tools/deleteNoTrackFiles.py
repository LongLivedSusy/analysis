from ROOT import *
from glob import glob
import os

istest = False
flist = glob('/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/ProductionRun2v1/*.root')
for fname in flist:
   needsdeleting = False
   f = TFile(fname)
   
   try:
      t = f.Get('TreeMaker2/PreSelection')
      if t.GetEntries()==0: a = a
      t.GetEntry(0)
      tlen = len(t.tracks)
      print 'got track length', tlen
      f.Close()
      print 'SUCCESS!', fname
   except:
      print 'failed to find tracks, removing', fname
      command = 'lcg-del -b -l -T  srmv2 "srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN='+fname+'"' 
      print 'command', command     
      if not istest: os.system(command)
      f.Close()




