#!/bin/env python
from submit import *
from optparse import OptionParser

parser = OptionParser()
(options, args) = parser.parse_args()
if len(args) > 0:
    files_per_job = int(args[0])
else:
    files_per_job = 10

def get_data_sample_names(folder, globstring = "/*root"):
    
    samples = []
    for item in glob.glob(folder + globstring):
                
        sample_name = "_".join( item.split("/")[-1].split(".root")[0].split("_")[:-2] )
        samples.append(sample_name)

    samples = list(set(samples))

    return samples
    

def get_userlist():

    # get list of users with NtupleHub at DESY:

    userlist = []
    hub_folders = glob.glob("/pnfs/desy.de/cms/tier2/store/user/*/NtupleHub/")
    for hub_folder in hub_folders:
        userlist.append(hub_folder.split("/")[-3])

    return userlist


ntuples = {}
for user in get_userlist():
    print "user", user
    if user == "sbein":
        folder = "/pnfs/desy.de/cms/tier2/store/user/%s/NtupleHub/ProductionRun2v4" % user
    else:
        folder = "/pnfs/desy.de/cms/tier2/store/user/%s/NtupleHub/ProductionRun2v3" % user
    ntuples[folder] = get_data_sample_names(folder)

    
ntuples["/nfs/dust/cms/user/beinsam/CommonNtuples/MC_BSM/LongLivedSMS/ntuple_sidecar"] = [
    "g1800_chi1400_27_200970_step4_10",
    "g1800_chi1400_27_200970_step4_30",
    "g1800_chi1400_27_200970_step4_50",
    "g1800_chi1400_27_200970_step4_100",
    "g1800_chi1400_27_200970_step4_1000",
]
    
ntuples["/nfs/dust/cms/user/kutznerv/DisappTrksSignalMC/april19-Summer16sig"] = [
    "Summer16.g1800_chi1400_27_200970_step4_10AODSIM",
    "Summer16.g1800_chi1400_27_200970_step4_30AODSIM",
    "Summer16.g1800_chi1400_27_200970_step4_50AODSIM",
    "Summer16.g1800_chi1400_27_200970_step4_100AODSIM",
]

ntuples["/nfs/dust/cms/user/kutznerv/DisappTrksSignalMC/april19-Autumn18sig"] = [
    "Autumn18.g1800_chi1400_27_200970_step4_10AODSIM",
    "Autumn18.g1800_chi1400_27_200970_step4_30AODSIM",
    "Autumn18.g1800_chi1400_27_200970_step4_50AODSIM",
    "Autumn18.g1800_chi1400_27_200970_step4_100AODSIM",
]

#command = "./looper_ng.py --input $INPUT --output $OUTPUT --fakerate_file output_fakerate_5_loose_merged/fakerate.root"
command = "./looper_ng.py --input $INPUT --output $OUTPUT --fakerate_file output_fakerate_5_loose_merged/fakerate.root --loose_dxy"
output_folder = "output_skim_6_loose"
commands = []
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

    commands += prepare_command_list(folder, ntuples[folder], output_folder, command=command, files_per_job=files_per_job, nowildcard=nowildcard)

do_submission(commands, output_folder, executable = "looper_ng.py")
