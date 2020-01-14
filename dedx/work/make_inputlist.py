import os, sys
from glob import glob

def make_inputlist(samples):
    userlist = []
    hub_folders = glob("/pnfs/desy.de/cms/tier2/store/user/*/NtupleHub/")
    for hub_folder in hub_folders:
        userlist.append(hub_folder.split("/")[-3])
    
    folders=[]
    for user in userlist:
        print "Adding NtupleHub contents from %s..." % user
        if user == "sbein":
            folders.append("/pnfs/desy.de/cms/tier2/store/user/%s/NtupleHub/ProductionRun2v4" % user)
	elif user == "vkutzner":
            folders.append("/pnfs/desy.de/cms/tier2/store/user/%s/NtupleHub/ProductionRun2v3" % user)
            folders.append("/pnfs/desy.de/cms/tier2/store/user/%s/NtupleHub/ProductionRun2v3_aksingh" % user)
        else:
            folders.append("/pnfs/desy.de/cms/tier2/store/user/%s/NtupleHub/ProductionRun2v3" % user)
   
    print "Making input lists.."
    if not os.path.exists("./inputs"):
	os.system("mkdir -p inputs")
    
    samplelist=[]
    for sample in samples:
	outputname = sample
	if "*" in sample : 
	    outputname = sample.replace("*","_")
        print outputname
	with open("./inputs/%s.txt"%outputname,'w') as f:
	    for folder in folders:
		for inputfile in sorted(glob(folder + "/" + sample +"*.root")):
		    f.write(inputfile+'\n')
   
def split_inputlist(nfpj=100):
    inputfiles = glob("./inputs/*.txt")
    
    print "Making splitted input lists.."
    if not os.path.exists("./inputs/split"):
	os.system("mkdir -p ./inputs/split")
    
    for inputfile in inputfiles:
	outfile = inputfile.split('/')[-1].replace(".txt","_")
	os.system("split -l %s -d -a 3 %s ./inputs/split/%s"%(nfpj,inputfile,outfile))




if __name__ == "__main__" : 
   
    # Sample name for globbing
    mc_summer16 = [
    "Summer16.DYJetsToLL",
    "Summer16.QCD",
    "Summer16.WJetsToLNu_HT",
    "Summer16.ZJetsToNuNu",
    "Summer16.WW_TuneCUETP8M1",
    "Summer16.WZ_TuneCUETP8M1",
    "Summer16.ZZ_TuneCUETP8M1",
    "Summer16.TTJets_TuneCUETP8M1_13TeV",
    ]

    Run2016_MET = [
    "Run2016B*MET",
    "Run2016C*MET",
    "Run2016D*MET",
    "Run2016E*MET",
    "Run2016F*MET",
    "Run2016G*MET",
    "Run2016H*MET",
    ]
    
    Run2016_SingleMuon = [
    "Run2016B*SingleMuon",
    "Run2016C*SingleMuon",
    "Run2016D*SingleMuon",
    "Run2016E*SingleMuon",
    "Run2016F*SingleMuon",
    "Run2016G*SingleMuon",
    "Run2016H*SingleMuon",
    ]
    
    Run2016_SingleElectron = [
    "Run2016B*SingleElectron",
    "Run2016C*SingleElectron",
    "Run2016D*SingleElectron",
    "Run2016E*SingleElectron",
    "Run2016F*SingleElectron",
    "Run2016G*SingleElectron",
    "Run2016H*SingleElectron",
    ]
    
    mc_signal = [
    "RunIISummer16MiniAODv3.SMS-T1qqqq",
    "RunIISummer16MiniAODv3.SMS-T2bt",
    ]

    samples=[]
    samples.extend(mc_summer16)
    samples.extend(Run2016_MET)
    samples.extend(Run2016_SingleMuon)
    samples.extend(Run2016_SingleElectron)
    #samples.extend(mc_signal)

    #Input list for each process
    make_inputlist(samples)

    #Split list for number of files per job
    nfpj = 100
    split_inputlist(nfpj)

