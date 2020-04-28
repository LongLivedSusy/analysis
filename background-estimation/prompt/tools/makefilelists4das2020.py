from glob import glob


flistwjets = glob('/pnfs/desy.de/cms/tier2/store/user/*/NtupleHub/ProductionRun2v3/*WJets*.root')
flistzjets = glob('/pnfs/desy.de/cms/tier2/store/user/*/NtupleHub/ProductionRun2v3/*ZJets*.root')
flistttjets = glob('/pnfs/desy.de/cms/tier2/store/user/*/NtupleHub/ProductionRun2v3/*TTJets*.root')
flistdy = glob('/pnfs/desy.de/cms/tier2/store/user/*/NtupleHub/ProductionRun2v3/*DYJets*.root')
flistsmu = glob('/pnfs/desy.de/cms/tier2/store/user/*/NtupleHub/ProductionRun2v3/*un2016*SingleMu*.root')
flistsel = glob('/pnfs/desy.de/cms/tier2/store/user/*/NtupleHub/ProductionRun2v3/*un2016*SingleEl*.root')
flistmet = glob('/pnfs/desy.de/cms/tier2/store/user/*/NtupleHub/ProductionRun2v3/*un2016*MET*.root')

print len(flistwjets), len(flistzjets), len(flistttjets), len(flistdy)

f = open('flist-wjets.txt','w')
for filename in flistwjets:
	f.write(filename+'\n')
f.close()
f = open('flist-zjets.txt','w')
for filename in flistzjets:
	f.write(filename+'\n')
f.close()
f = open('flist-ttjets.txt','w')
for filename in flistttjets:
	f.write(filename+'\n')
f.close()
f = open('flist-dyjets.txt','w')
for filename in flistdy:
	f.write(filename+'\n')
f.close()
f = open('flist-met.txt','w')
for filename in flistmet:
	f.write(filename+'\n')
f.close()
f = open('flist-sel.txt','w')
for filename in flistsel:
	f.write(filename+'\n')
f.close()
f = open('flist-smu.txt','w')
for filename in flistsmu:
	f.write(filename+'\n')
f.close()