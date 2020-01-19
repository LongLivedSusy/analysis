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

    ## Bkg samples
    Summer16_DYJetsToLL = [
    #"Summer16.DYJetsToLL_M-50_TuneCUETP8M1",
    "Summer16.DYJetsToLL_M-50_HT-100to200",
    "Summer16.DYJetsToLL_M-50_HT-200to400",
    "Summer16.DYJetsToLL_M-50_HT-400to600",
    "Summer16.DYJetsToLL_M-50_HT-600to800",
    "Summer16.DYJetsToLL_M-50_HT-800to1200",
    "Summer16.DYJetsToLL_M-50_HT-1200to2500",
    "Summer16.DYJetsToLL_M-50_HT-2500toInf",
    ]

    Summer16_QCD = [
    "Summer16.QCD_HT200to300",
    "Summer16.QCD_HT300to500",
    "Summer16.QCD_HT500to700",
    "Summer16.QCD_HT700to1000",
    "Summer16.QCD_HT1000to1500",
    "Summer16.QCD_HT1500to2000",
    "Summer16.QCD_HT2000toInf",
    ]
    
    Summer16_TTJets = [
    "Summer16.TTJets_TuneCUETP8M1_13TeV",
    ]

    Summer16_WJetsToLNu = [
    #"Summer16.WJetsToLNu_TuneCUETP8M1",
    "Summer16.WJetsToLNu_HT-100To200",
    "Summer16.WJetsToLNu_HT-200To400",
    "Summer16.WJetsToLNu_HT-400To600",
    "Summer16.WJetsToLNu_HT-600To800",
    "Summer16.WJetsToLNu_HT-800To1200",
    "Summer16.WJetsToLNu_HT-1200To2500",
    "Summer16.WJetsToLNu_HT-2500ToInf",
    ]
    
    Summer16_ZJetsToNuNu = [
    "Summer16.ZJetsToNuNu_HT-100To200",
    "Summer16.ZJetsToNuNu_HT-200To400",
    "Summer16.ZJetsToNuNu_HT-400To600",
    "Summer16.ZJetsToNuNu_HT-600To800",
    "Summer16.ZJetsToNuNu_HT-800To1200",
    "Summer16.ZJetsToNuNu_HT-1200To2500",
    "Summer16.ZJetsToNuNu_HT-2500ToInf",
    ]
    
    Summer16_WW = [
    "Summer16.WW_TuneCUETP8M1",
    ]

    Summer16_WZ = [
    "Summer16.WZ_TuneCUETP8M1",
    ]
    
    Summer16_ZZ = [
    "Summer16.ZZ_TuneCUETP8M1",
    ]

    ## Data samples
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
   
    ## Signal samples
    #mc_signal = [
    #"RunIISummer16MiniAODv3.SMS-T1qqqq",
    #"RunIISummer16MiniAODv3.SMS-T2bt",
    #]

    samples=[]
    samples.extend(Summer16_DYJetsToLL)
    samples.extend(Summer16_QCD)
    samples.extend(Summer16_TTJets)
    samples.extend(Summer16_WJetsToLNu)
    samples.extend(Summer16_ZJetsToNuNu)
    samples.extend(Summer16_WW)
    samples.extend(Summer16_WZ)
    samples.extend(Summer16_ZZ)
    samples.extend(Run2016_MET)
    samples.extend(Run2016_SingleMuon)
    samples.extend(Run2016_SingleElectron)
    #samples.extend(mc_signal)

    #Input list for each process
    make_inputlist(samples)

    #Split list for number of files per job
    nfpj = 100
    split_inputlist(nfpj)

