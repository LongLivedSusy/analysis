#!/bin/env python
import os, glob
from optparse import OptionParser
from GridEngineTools import runParallel

n_duplicates = 0

def prepare_command_list(ntuples_folder, samples, output_folder, files_per_job = 5, files_per_sample = -1, command = "./looper.py $INPUT $OUTPUT 0 0", nowildcard=False, list_of_duplicates = []):

    global n_duplicates

    commands = []

    for sample in samples:

        ifile_list = sorted(glob.glob(ntuples_folder + "/" + sample + "*.root"))

        if nowildcard:
            ifile_list = sorted(glob.glob(ntuples_folder + "/" + sample + ".root"))
        
        if files_per_sample != -1:
            ifile_list = ifile_list[:files_per_sample]
        
        if len(ifile_list)==0:
            continue

        #if list_of_duplicates and len(list_of_duplicates)>0:
        #    for duplicate in list_of_duplicates:
        #        if duplicate in ifile_list:
        #            ifile_list.remove(duplicate)
        #            n_duplicates += 1
        #    print "Removed %s duplicates in total!" % n_duplicates

        print "Looping over %s files (%s)" % (len(ifile_list), sample)
       
        file_segments = [ifile_list[x:x+files_per_job] for x in range(0,len(ifile_list),files_per_job)]

        for inFile_segment in file_segments:
            cmd = ""
            for inFile in inFile_segment:
                #in_tree = str(inFile_segment).replace(", ", ",").replace("[", "").replace("]", "")
                out_tree = output_folder + "/" + inFile.split("/")[-1].split(".root")[0] + "_skim.root"
                cmd += command.replace("$INPUT", inFile).replace("$OUTPUT", out_tree) + "; "
            commands.append(cmd)
                        
    return commands


def do_submission(commands, output_folder, condorDir = "bird", executable = "looper.py", runmode = "grid", dontCheckOnJobs=True, confirm=True):

    print "Submitting \033[1m%s jobs\033[0m, output folder will be \033[1m%s\033[0m." % (len(commands), output_folder)
    os.system("mkdir -p %s" % output_folder)
    os.system("cp %s %s/" % (executable, output_folder))
    return runParallel(commands, runmode, condorDir=condorDir, dontCheckOnJobs=dontCheckOnJobs, use_more_mem=False, use_more_time=False, confirm = confirm)


def get_data_sample_names(folder, globstring = "*"):
    
    samples = []
        
    for item in glob.glob(folder + "/" + globstring + ".root"):
                
        sample_name = "_".join( item.split("/")[-1].split(".root")[0].split("_")[:-2] )
        samples.append(sample_name)

    samples = list(set(samples))

    return samples
    

def get_userlist():

    userlist = []
    hub_folders = glob.glob("/pnfs/desy.de/cms/tier2/store/user/*/NtupleHub/")
    for hub_folder in hub_folders:
        userlist.append(hub_folder.split("/")[-3])

    return userlist


def get_ntuple_datasets(globstring_list, add_signals = True):

    globstrings = globstring_list.split(",")

    ntuples = {}
    for user in get_userlist():
        print "Adding NtupleHub contents from %s..." % user
        if user == "sbein":
            folder = "/pnfs/desy.de/cms/tier2/store/user/%s/NtupleHub/ProductionRun2v4" % user
        else:
            folder = "/pnfs/desy.de/cms/tier2/store/user/%s/NtupleHub/ProductionRun2v3" % user
        if folder not in ntuples:
            ntuples[folder] = []
        for i_globstring in globstrings:
            ntuples[folder] += get_data_sample_names(folder, globstring = i_globstring)
    
    if add_signals:

        #ntuples["/nfs/dust/cms/user/beinsam/CommonNtuples/MC_BSM/LongLivedSMS/ntuple_sidecar"] = [
        #    "g1800_chi1400_27_200970_step4_10",
        #    "g1800_chi1400_27_200970_step4_30",
        #    "g1800_chi1400_27_200970_step4_50",
        #    "g1800_chi1400_27_200970_step4_100",
        #    "g1800_chi1400_27_200970_step4_1000",
        #]
    
        ntuples["/nfs/dust/cms/user/kutznerv/DisappTrksSignalMC/april19-Summer16sig"] = [
            "Summer16.g1800_chi1400_27_200970_step4_10AODSIM_RA2AnalysisTree",
            "Summer16.g1800_chi1400_27_200970_step4_30AODSIM_RA2AnalysisTree",
            "Summer16.g1800_chi1400_27_200970_step4_50AODSIM_RA2AnalysisTree",
            "Summer16.g1800_chi1400_27_200970_step4_100AODSIM_RA2AnalysisTree",
        ]
       
        #ntuples["/nfs/dust/cms/user/kutznerv/DisappTrksSignalMC/april19-Autumn18sig"] = [
        #    "Autumn18.g1800_chi1400_27_200970_step4_10AODSIM_RA2AnalysisTree",
        #    "Autumn18.g1800_chi1400_27_200970_step4_30AODSIM_RA2AnalysisTree",
        #    "Autumn18.g1800_chi1400_27_200970_step4_50AODSIM_RA2AnalysisTree",
        #    "Autumn18.g1800_chi1400_27_200970_step4_100AODSIM_RA2AnalysisTree",
        #]
  
    return ntuples
    

from collections import defaultdict
def list_duplicates(seq):
    tally = defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)
    return ((key,locs) for key,locs in tally.items() 
                            if len(locs)>1)


def get_list_of_duplicates(ntuples):

    #os.system("rm delete_duplicates.sh")
    list_of_duplicates = []

    file_names = []
    full_paths = []

    print "Checking for duplicates..."

    for folder in ntuples:
        for identifier in ntuples[folder]:
            file_names += glob.glob(folder + "/" + identifier + "*.root")

    for i in range(len(file_names)):
        full_paths.append(file_names[i])
        file_names[i] = file_names[i].split("/")[-1]

    unique_files = list(set(file_names))

    if len(file_names) != len(unique_files):

        print "# present files =", len(file_names)
        print "# unique files  =", len(unique_files)
        print "# dupes         =", len(file_names) - len(unique_files)
        
        indices_to_be_removed = []
        for dup_indices in list(list_duplicates(file_names)):
            indices = dup_indices[1]
            if len(indices)>1:
                indices_to_be_removed += indices[1:]

        indices_to_be_removed = list(set(indices_to_be_removed))

        print "Found %s duplicates!" % len(indices_to_be_removed)

        removed_files = []
        for i in indices_to_be_removed:
            #cmd = "gfal-rm srm://dcache-se-cms.desy.de/%s" % full_paths[i]
            #os.system("echo '%s' >> delete_duplicates.sh" % cmd)
            list_of_duplicates.append(full_paths[i])

    else:

        print "No duplicates"

    return list_of_duplicates


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--nfiles", dest="files_per_job", default=60)
    parser.add_option("--start", dest="start", action="store_true")
    parser.add_option("--command", dest="command")
    parser.add_option("--dataset", dest="dataset")
    parser.add_option("--output_folder", dest="output_folder")
    (options, args) = parser.parse_args()

    mc_summer16 = "Summer16.DYJetsToLL*,Summer16.QCD*,Summer16.WJetsToLNu*,Summer16.ZJetsToNuNu*,Summer16.WW_TuneCUETP8M1*,Summer16.WZ_TuneCUETP8M1*,Summer16.ZZ_TuneCUETP8M1*,Summer16.TTJets_TuneCUETP8M1_13TeV*,Summer16.TTJets_HT*"
    mc_fall17 = "RunIIFall17MiniAODv2.DYJetsToLL*,RunIIFall17MiniAODv2.QCD*,RunIIFall17MiniAODv2.WJetsToLNu*,RunIIFall17MiniAODv2.ZJetsToNuNu*,RunIIFall17MiniAODv2.WW*,RunIIFall17MiniAODv2.WZ*,RunIIFall17MiniAODv2.ZZ*,RunIIFall17MiniAODv2.TTJets_Tune*,RunIIFall17MiniAODv2.TTJets_HT*,RunIIFall17MiniAODv2.GJets_HT*"
    data_phase0 = "Run2016*MET*"
    data_phase1 = "Run2017*,Run2018*"

    ######## defaults ########
    if not options.command:
        options.command = "./skimmer.py --input $INPUT --output $OUTPUT"
    if not options.dataset:
        options.dataset = mc_summer16 + "," + data_phase0
        #options.dataset = mc_fall17 + "," + data_phase1
    if not options.output_folder:
        options.output_folder = "skim_16DataMC"
    ######## defaults ########

    commands = []
    ntuples = get_ntuple_datasets(options.dataset, add_signals = True)

    for folder in ntuples:
    
        def is_string_in_list(text, mylist):
            for item in mylist:
                if text in item:
                    return True
            return False
       
        if is_string_in_list("g1800", ntuples[folder]):
            nowildcard = True
        else:
            nowildcard = False
    
        commands += prepare_command_list(folder, ntuples[folder], options.output_folder, command=options.command, files_per_job=int(options.files_per_job), nowildcard=nowildcard)
    
    do_submission(commands, options.output_folder, condorDir=options.output_folder + ".condor", executable=options.command.split()[0], confirm=not options.start)

    #print "Merging..."
    #os.system("./merge_samples.py --start --hadd %s" % options.output_folder)

