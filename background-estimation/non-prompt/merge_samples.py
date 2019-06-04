#!/bin/env python
import os, glob
from optparse import OptionParser
import commands
from natsort import natsorted, ns
import sys

# merge skim output

parser = OptionParser()
(options, args) = parser.parse_args()
if len(args) > 0:
    folder = args[0]
else:
    print "usage: ./merge_samples.py <folder>"
    quit()

if folder[-1] == "/":
    folder = folder[:-1]

samples = []
for item in glob.glob(folder + "/*root"):

    # ignore broken HT binning labels
    ignore_item = False
    ignore_list = ["-100to20_", "-10to200_", "-200to40_", "-20to400_", "-40to600_", "-600to80_", "-20To400_", "-400To60_", "-40To600_", "HT100to1500_", "HT1500to200_", "HT200toInf_", "-200toInf_", "-80to1200_", "-200To40_", "-250toInf_", "-1200to250_", "-800to120_", "-120to2500_", "-60ToInf_", "Run218", "Run217", "Run216"]
    for i_ignore in ignore_list:
        if i_ignore in item:
            ignore_item = True
    if ignore_item: continue

    sample_name = "_".join( item.split("/")[-1].split(".root")[0].split("_")[:-3] )
    sample_name = sample_name.replace("_ext1","").replace("_ext2","").replace("_ext3","")
    sample_name = sample_name.replace("AOD","")

    if "Run201" in sample_name:
        if sample_name[-1].isdigit():
            sample_name = sample_name[:-1]

    samples.append(sample_name)

samples = list(set(samples))

print "Merging samples of folder %s:" % folder
for sample in samples:
    print sample

os.system("mkdir -p %s_merged" % folder)
for sample in samples:
    os.system("hadd -f %s_merged/%s.root %s/%s*.root" % (folder, sample, folder, sample))

os.system("cp %s/*py %s_merged/" % (folder, folder))


# merge lumisection JSON:
print "merging jsons..."

def get_json(folder, years = ["2016"], datastreams = ["MET", "SingleElectron", "SingleMuon"]):

    json_cleaning = True

    for year in years:
        for datastream in datastreams:
        
            print "Doing datastream Run%s_%s" % (year, datastream)
        
            combined_json = {}
            filelist = sorted(glob.glob("%s/*Run%s*%s*json" % (folder, year, datastream)))
            
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
            
            #if json_cleaning:
            #    # compact lumisections:
            #    combined_json_compacted = []
            #    for i in range(len(combined_json[run])):
            #        if len(combined_json_compacted) == 0:
            #            combined_json_compacted.append()
            
            combined_json_text = str(combined_json).replace("'", '"')
            filename = "%s_merged/Run%s_%s.json" % (folder, year, datastream)
        
            with open(filename, "w") as fout:
                fout.write(combined_json_text)
        
                print "%s written" % filename
      

get_json(folder, years = ["2016", "2017", "2018"], datastreams = ["JetHT", "MET", "SingleElectron", "SingleMuon"])    


