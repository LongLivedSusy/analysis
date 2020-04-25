#!/bin/env python
import os, glob
from optparse import OptionParser
import commands
from natsort import natsorted, ns
import sys
from GridEngineTools import runParallel
import json

def hadd_histograms(folder, runmode, delete_input_files = False, start = False, use_custom_hadd = True):

    if folder[-1] == "/":
        folder = folder[:-1]

    samples = []
    for item in glob.glob(folder + "/*root"):

        # ignore broken HT binning labels
        ignore_item = False
        ignore_list = ["-100to20_", "-10to200_", "-200to40_", "-20to400_", "-40to600_", "-600to80_", "-20To400_", "-400To60_", "-40To600_", "HT100to1500_", "HT1500to200_", "HT200toInf_", "-200toInf_", "-80to1200_", "-200To40_", "-250toInf_", "-1200to250_", "-800to120_", "-120to2500_", "1000to150_", "-60ToInf_", "400to60_", "100To20_", "HT150to2000_", "HT200to30_", "HT1000to150_", "Run218", "Run217", "Run216"]
        for i_ignore in ignore_list:
            if i_ignore in item:
                ignore_item = True
        if ignore_item: continue

        sample_name = item.split("/")[-1].split("AOD_")[0]
        sample_name = sample_name.replace("_ext1","").replace("_ext2","").replace("_ext3","")
        sample_name = sample_name.split("_RA2AnalysisTree")[0]

        if sample_name[-1] == "-":
            sample_name = sample_name[:-1]

        if "Run201" in sample_name:
            if sample_name[-1].isdigit():
                sample_name = sample_name[:-1]

        if sample_name[-3:] == "AOD":
            sample_name = sample_name[:-3]

        samples.append(sample_name)

    samples = list(set(samples))
    print "Merging samples of folder %s:" % folder
    for sample in samples:
        print sample

    cmds = []
    for i, sample in enumerate(samples):
        if use_custom_hadd:
            #command = "./terahadd.py %s_merged/%s.root %s/%s*.root " % (folder, sample, folder, sample)
            command = "hadd %s_merged/%s.root %s/%s*.root " % (folder, sample, folder, sample)
        else:
            command = "hadd -f %s_merged/%s.root %s/%s*.root " % (folder, sample, folder, sample)
        if delete_input_files:
            command += " && rm %s/%s*.root " % (folder, sample)
            if " *" in command:
                print "Wildcard rm command found, this should never happen!"
                quit()
        cmds.append(command)

    runParallel(cmds, runmode, ncores_percentage=0.5, condorDir="%s_merged.condor" % folder, dontCheckOnJobs=True, confirm=(not start), use_more_time=False)
    os.system("cp %s/*py %s_merged/" % (folder, folder))


def merge_json_files(folder, years = ["2016"], datastreams = ["MET", "SingleElectron", "SingleMuon"], json_cleaning = True):

    if folder[-1] == "/":
        folder = folder[:-1]

    for year in years:
        for datastream in datastreams:
        
            filename = "%s_merged/Run%s_%s.json" % (folder, year, datastream)

            print "Doing datastream Run%s_%s" % (year, datastream)
        
            combined_json = {}
            #filelist = sorted(glob.glob("%s/*Run%s*%s*json" % (folder, year, datastream)))
            filelist = sorted(glob.glob("%s/*Run%s*%s*.json" % (folder, year, datastream)))
            
            for i_ifile, ifile in enumerate(filelist):
                               
                if i_ifile % 100 == 0:
                     sys.stderr.write("%s/%s\n" % (i_ifile, len(filelist)))
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
                                    indices_to_be_deleted.append(i)
                                elif combined_json[run][i-1][1] >= combined_json[run][i][0]:
                                    combined_json[run][i-1][1] = combined_json[run][i][1]
                                    indices_to_be_deleted.append(i)
                        
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
           
    print "Getting lumi for %s..." % json_file_name
    
    status, out = commands.getstatusoutput("export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH; brilcalc lumi -u /fb -c offsite -i %s --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json; grep '|' %s.briloutput | tail -n1" % (json_file_name, json_file_name))
    
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


def get_lumis(folder, cern_username):

    lumis = {}
    for json_file in glob.glob("%s_merged/*.json" % folder):

        try:
            lumi = get_lumi_from_bril(json_file, cern_username)
            lumis[json_file.split("/")[-1].split(".json")[0]] = lumi
        except:
            print "Couldn't get lumi for %s. Empty JSON?" % json_file
        
    with open("%s_merged/luminosity.py" % folder, "w+") as fout:
        output = json.dumps(lumis)
        print output
        fout.write(output)

    print "Closing SSH tunnel..."
    os.system("pkill -f itrac5117")
    

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--json", dest="json", action="store_true")
    parser.add_option("--bril", dest="bril", action="store_true")
    parser.add_option("--hadd", dest="hadd", action="store_true")
    parser.add_option("--runmode", dest="runmode", default="grid")
    parser.add_option("--start", dest="start", action="store_true")
    parser.add_option("--cern_username", dest="cern_username", default="vkutzner")
    (options, args) = parser.parse_args()

    if len(args) > 0:
        folder = args[0]
    else:
        print "Merge everything: run with ./merge_samples.py output_skim_14_moredata/"
        print "For brilcalc, make sure that you have brilws installed (pip install --user brilws)"
        print "Set your CERN username with --cern_username"
        quit()

    if not os.path.exists("%s_merged" % folder):
        os.system("mkdir -p %s_merged" % folder)

    # do everything by default
    if not options.hadd and not options.json and not options.bril:
        options.hadd = True
        options.json = True
        options.bril = True

    # make sure we have a tunnel for running bril
    if options.bril:
        status, out = commands.getstatusoutput('ps axu | grep "itrac5117-v.cern.ch:1012" | grep -v grep')
        if status != 0:
            print "Opening SSH tunnel for brilcalc..."
            os.system("ssh -f -N -L 10121:itrac5117-v.cern.ch:10121 %s@lxplus.cern.ch" % options.cern_username)
        else:
            print "Existing tunnel for brilcalc found"

    if options.hadd:
        hadd_histograms(folder, options.runmode, start = options.start)
    if options.json:
        #merge_json_files(folder, years = ["2016", "2017", "2018", "2016B", "2016C", "2016D", "2016E", "2016F", "2016G", "2016H", "2017B", "2017C", "2017D", "2017E", "2017F", "2018A", "2018B", "2018C", "2018D"], datastreams = ["JetHT", "MET", "SingleElectron", "SingleMuon"])
        #merge_json_files(folder, years = ["2016", "2016B", "2016C", "2016D", "2016E", "2016F", "2016G", "2016H"], datastreams = ["JetHT", "MET", "SingleElectron", "SingleMuon"])
        merge_json_files(folder, years = ["2017", "2017B", "2017C", "2017D", "2017E", "2017F"], datastreams = ["JetHT", "MET", "SingleElectron", "SingleMuon"])
        #merge_json_files(folder, years = ["2018", "2018A", "2018B", "2018C", "2018D"], datastreams = ["JetHT", "MET", "EGamma", "SingleMuon"])
    if options.bril:
        get_lumis(folder, options.cern_username)
    
