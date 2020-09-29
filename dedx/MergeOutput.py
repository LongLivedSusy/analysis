#this module should work just like hadd
from ROOT import *
import glob, sys, os
import commands
import numpy as np
from natsort import natsorted, ns
import json
from shared_utils import *

MC = []
MC.append('Summer16.DYJetsToLL_M-50_TuneCUETP8M1')
MC.append('Summer16.DYJetsToLL_M-50_HT-100to200')
MC.append('Summer16.DYJetsToLL_M-50_HT-200to400')
MC.append('Summer16.DYJetsToLL_M-50_HT-400to600')
MC.append('Summer16.DYJetsToLL_M-50_HT-600to800')
MC.append('Summer16.DYJetsToLL_M-50_HT-800to1200')
MC.append('Summer16.DYJetsToLL_M-50_HT-1200to2500')
MC.append('Summer16.DYJetsToLL_M-50_HT-2500toInf')
MC.append('Summer16.QCD_HT200to300')
MC.append('Summer16.QCD_HT300to500')
MC.append('Summer16.QCD_HT500to700')
MC.append('Summer16.QCD_HT700to1000')
MC.append('Summer16.QCD_HT1000to1500')
MC.append('Summer16.QCD_HT1500to2000')
MC.append('Summer16.QCD_HT2000toInf')
MC.append('Summer16.TTJets')
MC.append('Summer16.WJetsToLNu_TuneCUETP8M1')
MC.append('Summer16.WJetsToLNu_HT-100To200')
MC.append('Summer16.WJetsToLNu_HT-200To400')
MC.append('Summer16.WJetsToLNu_HT-400To600')
MC.append('Summer16.WJetsToLNu_HT-600To800')
MC.append('Summer16.WJetsToLNu_HT-800To1200')
MC.append('Summer16.WJetsToLNu_HT-1200To2500')
MC.append('Summer16.WJetsToLNu_HT-2500ToInf')
MC.append('Summer16.ZJetsToNuNu_HT-100To200')
MC.append('Summer16.ZJetsToNuNu_HT-200To400')
MC.append('Summer16.ZJetsToNuNu_HT-400To600')
MC.append('Summer16.ZJetsToNuNu_HT-600To800')
MC.append('Summer16.ZJetsToNuNu_HT-800To1200')
MC.append('Summer16.ZJetsToNuNu_HT-1200To2500')
MC.append('Summer16.ZJetsToNuNu_HT-2500ToInf')
MC.append('Summer16.WW')
MC.append('Summer16.WZ')
MC.append('Summer16.ZZ')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-1')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-50')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-150')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-200')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-400')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-600')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-800')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-900')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-1000')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-1100')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-1200')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-1300')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-1400')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-1500')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-1600')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-1700')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-1800')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-2000')

#MC.append('RunIIFall17MiniAODv2.DYJetsToLL_M-50_TuneCP5')
#MC.append('RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-100to200')
#MC.append('RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-200to400')
#MC.append('RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-400to600')
#MC.append('RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-600to800')
#MC.append('RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-800to1200')
#MC.append('RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-1200to2500')
#MC.append('RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-2500toInf')
#MC.append('RunIIFall17MiniAODv2.QCD_HT200to300')
#MC.append('RunIIFall17MiniAODv2.QCD_HT300to500')
#MC.append('RunIIFall17MiniAODv2.QCD_HT500to700')
#MC.append('RunIIFall17MiniAODv2.QCD_HT700to1000')
#MC.append('RunIIFall17MiniAODv2.QCD_HT1000to1500')
#MC.append('RunIIFall17MiniAODv2.QCD_HT1500to2000')
#MC.append('RunIIFall17MiniAODv2.QCD_HT2000toInf')
#MC.append('RunIIFall17MiniAODv2.TTJets_TuneCP5')
#MC.append('RunIIFall17MiniAODv2.TTJets_HT-600to800')
#MC.append('RunIIFall17MiniAODv2.TTJets_HT-800to1200')
#MC.append('RunIIFall17MiniAODv2.TTJets_HT-1200to2500')
#MC.append('RunIIFall17MiniAODv2.TTJets_HT-2500toInf')
#MC.append('RunIIFall17MiniAODv2.WJetsToLNu_HT-100To200')
#MC.append('RunIIFall17MiniAODv2.WJetsToLNu_HT-200To400')
#MC.append('RunIIFall17MiniAODv2.WJetsToLNu_HT-400To600')
#MC.append('RunIIFall17MiniAODv2.WJetsToLNu_HT-600To800')
#MC.append('RunIIFall17MiniAODv2.WJetsToLNu_HT-800To1200')
#MC.append('RunIIFall17MiniAODv2.WJetsToLNu_HT-1200To2500')
#MC.append('RunIIFall17MiniAODv2.WJetsToLNu_HT-2500ToInf')
#MC.append('RunIIFall17MiniAODv2.ZJetsToNuNu_HT-100To200')
#MC.append('RunIIFall17MiniAODv2.ZJetsToNuNu_HT-200To400')
#MC.append('RunIIFall17MiniAODv2.ZJetsToNuNu_HT-400To600')
#MC.append('RunIIFall17MiniAODv2.ZJetsToNuNu_HT-600To800')
#MC.append('RunIIFall17MiniAODv2.ZJetsToNuNu_HT-800To1200')
#MC.append('RunIIFall17MiniAODv2.ZJetsToNuNu_HT-1200To2500')
#MC.append('RunIIFall17MiniAODv2.ZJetsToNuNu_HT-2500ToInf')
#MC.append('RunIIFall17MiniAODv2.WWTo1L1Nu2Q')
#MC.append('RunIIFall17MiniAODv2.WZTo1L1Nu2Q')
#MC.append('RunIIFall17MiniAODv2.WZTo1L3Nu')
#MC.append('RunIIFall17MiniAODv2.ZZTo2L2Q')
#MC.append('RunIIFall17MiniAODv2.WZZ_TuneCP5')

Data=[]
Data.append('Run2016B-SingleMuon')
Data.append('Run2016C-SingleMuon')
Data.append('Run2016D-SingleMuon')
Data.append('Run2016E-SingleMuon')
Data.append('Run2016F-SingleMuon')
Data.append('Run2016G-SingleMuon')
Data.append('Run2016H-SingleMuon')
Data.append('Run2016B-SingleElectron')
Data.append('Run2016C-SingleElectron')
Data.append('Run2016D-SingleElectron')
Data.append('Run2016E-SingleElectron')
Data.append('Run2016F-SingleElectron')
Data.append('Run2016G-SingleElectron')
Data.append('Run2016H-SingleElectron')
Data.append('Run2016B-MET')
Data.append('Run2016C-MET')
Data.append('Run2016D-MET')
Data.append('Run2016E-MET')
Data.append('Run2016F-MET')
Data.append('Run2016G-MET')
Data.append('Run2016H-MET')
Data.append('Run2017B-SingleMuon')
Data.append('Run2017C-SingleMuon')
Data.append('Run2017D-SingleMuon')
Data.append('Run2017E-SingleMuon')
Data.append('Run2017F-SingleMuon')
Data.append('Run2017B-SingleElectron')
Data.append('Run2017C-SingleElectron')
Data.append('Run2017D-SingleElectron')
Data.append('Run2017E-SingleElectron')
Data.append('Run2017F-SingleElectron')

def merge_json_files(folder, datastreams = ["SingleMuon"], json_cleaning = True):

    print 'Merging json files for datastreams : {}'.format(datastreams)
    for datastream in datastreams:
        
        filename = "{}/{}.json".format(outdir, datastream)

        #if os.path.exists(filename):
        #    continue

        print "Doing datastream {}".format(datastream)
        
        combined_json = {}
        filelist = sorted(glob.glob("{}/{}*json".format(folder, datastream)))
            
        for i_ifile, ifile in enumerate(filelist):	
            #if i_ifile % 100 == 0:
            #     sys.stderr.write("%s/%s\n" % (i_ifile, len(filelist)))
            idict = ""
            with open(ifile, "r") as fin:
                idict = fin.read()
            idict = eval(idict) 
            for run in idict:
                if run not in combined_json:
                    combined_json[run] = []
                combined_json[run] += idict[run]
                combined_json[run] = natsorted(combined_json[run])
        
                if json_cleaning:
                    #test for overlap:
                    indices_to_be_deleted = []
                    if len(combined_json[run])>1:
                        for i in range(1, len(combined_json[run])):
                            
                            if combined_json[run][i-1][1] >= combined_json[run][i][1]:
                                #print "overlap", combined_json[run][i-1], combined_json[run][i]
                                #print "removing", combined_json[run][i]
                                indices_to_be_deleted.append(i)
                            elif combined_json[run][i-1][1] >= combined_json[run][i][0]:
                                #print "overlap", combined_json[run][i-1], combined_json[run][i]
                                combined_json[run][i-1][1] = combined_json[run][i][1]
                                indices_to_be_deleted.append(i)
                                #print "removing", combined_json[run][i], "keeping", combined_json[run][i-1]
                    
                    cleaned_list = []
                    for i in range(len(combined_json[run])):
                        if i not in indices_to_be_deleted:
                            cleaned_list.append(combined_json[run][i])
          
                    combined_json[run] = cleaned_list
                    
        combined_json_text = str(combined_json).replace("'", '"')
    
        with open(filename, "w+") as fout:
            fout.write(combined_json_text)
    
            print "%s written" % filename


def get_lumi_from_bril(json_file_name, cern_username, retry=False):
    status, out = commands.getstatusoutput('ps axu | grep "itrac5117-v.cern.ch:1012" | grep -v grep')
    print 'status,out : ', status, out
    if status != 0:
        print "Opening SSH tunnel for brilcalc..."
        os.system("ssh -f -N -L 10121:itrac5117-v.cern.ch:10121 %s@lxplus.cern.ch" % cern_username)
    else:
        print "Existing tunnel for brilcalc found"
        
    print "Getting lumi for %s..." % json_file_name
    
    status, out = commands.getstatusoutput("export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH; brilcalc lumi -u /fb -c offsite -i %s --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json > %s.briloutput; grep '|' %s.briloutput | tail -n1" % (json_file_name, json_file_name, json_file_name))
    
    if status != 0:
        if not retry:
            print "Trying to re-establish the tunnel..."
            os.system("pkill -f itrac5117")
            get_lumi_from_bril(json_file_name, cern_username, retry=True)
        else:
            print "Error while running brilcalc!"
            if cern_username == "vkutzner":
                print "Did you set your CERN username with '--cern_username'?"
        lumi = -1
    else:
        lumi = float(out.split("|")[-2])
    
    print "lumi:", lumi
    return lumi


def get_lumis(outdir, cern_username):
    lumis = {}
    for json_file in glob.glob(outdir+"/*.json"):
	try:
    	    lumi = get_lumi_from_bril(json_file, cern_username)
    	    lumis[json_file.split("/")[-1].split(".json")[0]] = lumi
    	except:
    	    print "Couldn't get lumi for %s . Empty JSON?" % json_file
        
    with open("./output_mediumchunks/luminosity.py", "w+") as fout:
        fout.write(json.dumps(lumis))

    print "Closing SSH tunnel..."
    os.system("pkill -f itrac5117")

if __name__ == "__main__" : 
    
    folder = "./output_smallchunks/"
    outdir = folder.replace('smallchunks','mediumchunks')
    
    if not os.path.exists(outdir):
        os.system("mkdir -p %s"%outdir)

    for keyword in MC:
        command = 'python ahadd.py -f %s/unwghtd'%outdir+keyword+'.root '+folder+'/*'+keyword+'*.root'
        print 'command', command
        if not istest: os.system(command)    
        fuw = TFile(outdir+'/unwghtd'+keyword+'.root')
        fw = TFile(outdir+'/'+keyword+'.root', 'recreate')
        hHt = fuw.Get('hHT_unweighted')
        nentries = hHt.GetEntries()
        keys = fuw.GetListOfKeys()
        for key in keys:
        	name = key.GetName()
        	if not len(name.split('/'))>0: continue
        	hist = fuw.Get(name)
        	hist.Scale(1.0/nentries)
        	fw.cd()
        	hist.Write()
        fuw.Close()
        command = 'rm %s/unwghtd'%outdir+keyword+'.root'
        print command
        if not istest: os.system(command)
        fw.Close()
    
    #for keyword in Data:
    #    command = 'python ahadd.py -f %s/'%outdir+keyword+'.root '+folder+'/*'+keyword+'*.root'
    #    print 'command', command
    #    if not istest: os.system(command)    
    #    #fw.Close()


    #merge_json_files(folder, datastreams = Data)
    #merge_json_files(folder, datastreams = ["Run2016B-SingleMuon","Run2016C-SingleMuon"])
    #get_lumis(outdir,"spak")
