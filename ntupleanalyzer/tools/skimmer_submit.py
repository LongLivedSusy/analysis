#!/bin/env python
import os, glob
from optparse import OptionParser
from GridEngineTools import runParallel
import more_itertools

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def prepare_command_list(ntuples_folder, samples, output_folder, files_per_job = 5, files_per_sample = -1, command = "./looper.py $INPUT $OUTPUT 0 0", process_files_individually=False):
 
    # note: process_files_individually will create a huge number of files (n_outputfile = n_inputfile) ! 
    # samples: list of data sample identifiers, e.g.: ["Run2016B-17Jul2018_ver2-v1.METAOD", "..."] 

    commands = []

    verify_outfiles = []
    verify_ntotal = 0

    print "looping over %s" % (ntuples_folder)

    for sample in samples:

        #ifile_list = sorted(glob.glob(ntuples_folder + "/" + sample + "*.root"))
        #ifile_list = glob.glob(ntuples_folder + "/" + sample + "*.root")
        ifile_list = glob.glob(ntuples_folder + "/" + sample + "_*.root")
        
        if files_per_sample != -1:
            ifile_list = ifile_list[:files_per_sample]
        
        if len(ifile_list)==0:
            continue
        
        #print "%s: looping over %s files (%s)" % (ntuples_folder, len(ifile_list), sample)
       
        file_segments = [ifile_list[x:x+files_per_job] for x in range(0,len(ifile_list),files_per_job)]

        for i_inFile_segment, inFile_segment in enumerate(file_segments):

            if process_files_individually:
                cmd = ""
                for inFile in inFile_segment:
                    out_tree = output_folder + "/" + inFile.split("/")[-1].split(".root")[0] + "_skim.root"
                    cmd += command.replace("$INPUT", inFile).replace("$OUTPUT", out_tree) + "; "
            else:
                #inFile = str(inFile_segment).replace(", ", ",").replace("[", "").replace("]", "")
                inFile = ",".join(inFile_segment)
                #out_tree = "%s/%s_%s_skim.root" % (output_folder, sample, i_inFile_segment)
                out_tree = output_folder + "/" + inFile_segment[0].split("/")[-1].replace("_RA2AnalysisTree.root", "") + "_skim.root"
                cmd = command.replace("$INPUT", inFile).replace("$OUTPUT", out_tree) + " ; "
                verify_outfiles.append(out_tree)
                verify_ntotal += len(ifile_list)
            commands.append(cmd)

    return commands


def do_submission(commands, output_folder, condorDir = "bird", executable = "looper.py", runmode = "grid", dontCheckOnJobs=False, confirm=True, use_more_mem=False, use_more_time=False):

    print "Submitting \033[1m%s jobs\033[0m, output folder will be \033[1m%s\033[0m." % (len(commands), output_folder)
    os.system("mkdir -p %s" % output_folder)
    os.system("cp %s %s/" % (executable, output_folder))
    os.system("cp ../../tools/shared_utils.py %s/" % (output_folder))
    runParallel(commands, runmode, condorDir=condorDir, dontCheckOnJobs=dontCheckOnJobs, use_more_mem=use_more_mem, use_more_time=use_more_time, confirm = confirm, cmsbase="/afs/desy.de/user/k/kutznerv/cmssw/CMSSW_11_2_3")
    #runParallel(commands, runmode, condorDir=condorDir, dontCheckOnJobs=dontCheckOnJobs, use_more_mem=False, use_more_time=21600, confirm = confirm, cmsbase="/afs/desy.de/user/k/kutznerv/cmssw/CMSSW_11_2_3")


def get_data_sample_names(folder, globstring = "*"):
    
    samples = []
    for item in glob.glob(folder + "*/" + globstring + ".root"):
        sample_name = "_".join( item.split("/")[-1].split(".root")[0].split("_")[:-2] )
        if sample_name not in samples:
            samples.append(sample_name)
    samples = list(set(samples))
    return samples
    

def get_ntuple_datasets(globstring_list, lowstats=False):

    globstrings = globstring_list.split(",")

    hub_folders = [
                    "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/ProductionRun2v3",
                    "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/ProductionRun2v3_jarieger",
                    "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/ProductionRun2v3_jsonneve",
                    "/pnfs/desy.de/cms/tier2/store/user/spak/NtupleHub/ProductionRun2v3",
                    "/pnfs/desy.de/cms/tier2/store/user/ssekmen/NtupleHub/ProductionRun2v3",
                    "/pnfs/desy.de/cms/tier2/store/user/tokramer/NtupleHub/ProductionRun2v3",
                    "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3",
                    "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3_restored",
                    "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3_SMS2",
                    "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3_SMS3",
                    "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3_akshansh",
                    "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3_vormwald",
                    "/pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/ProductionRun2v3",
                  ]

    ntuples = {}
    for folder in hub_folders:
        print "Searching for dataset identifiers in %s..." % folder
        ntuples[folder] = []
        for i_globstring in globstrings:
            #if "FSv3.SMS" in i_globstring and "SMS2" not in folder:
            if "FSv3.SMS" in i_globstring and not ("SMS2" in folder or "SMS3" in folder):
                #don't add SMS from any other folder...
                continue
                
            ntuples[folder] += get_data_sample_names(folder, globstring = i_globstring)
      
    return ntuples
    

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--nfiles", dest="files_per_job", default = 20)
    parser.add_option("--njobs", dest="njobs", default = -1)
    parser.add_option("--start", dest="start", action = "store_true")
    parser.add_option("--checkcomplete", dest="checkcomplete", action = "store_true")
    parser.add_option("--command", dest="command")
    parser.add_option("--cuts", dest="cuts", default = "")
    parser.add_option("--dataset", dest="dataset")
    parser.add_option("--output_folder", dest="output_folder")
    (options, args) = parser.parse_args()
    options.njobs = int(options.njobs)
    options.files_per_job = int(options.files_per_job)
    
    mc_summer16 = "Summer16.DYJetsToLL*,Summer16.QCD*,Summer16.WJetsToLNu*,Summer16.ZJetsToNuNu*,Summer16.WW_TuneCUETP8M1*,Summer16.WZ_TuneCUETP8M1*,Summer16.ZZ_TuneCUETP8M1*,Summer16.TT*"
    mc_fall17 = "RunIIFall17MiniAODv2.DYJetsToLL*,RunIIFall17MiniAODv2.QCD*,RunIIFall17MiniAODv2.WJetsToLNu*,RunIIFall17MiniAODv2.ZJetsToNuNu*,RunIIFall17MiniAODv2.WW*,RunIIFall17MiniAODv2.WZ*,RunIIFall17MiniAODv2.ZZ*,RunIIFall17MiniAODv2.TT*,RunIIFall17MiniAODv2.GJets_HT*"
    data_phase0 = "Run2016*"
    data_phase1 = "Run2017*,Run2018*"
    mc_sms = "RunIISummer16MiniAODv3.SMS*"

    sms_pmssm = "RunIIFall17FS.PMSSM*,RunIIAutumn18FS.PMSSM*,RunIIAutumn18FSv3.PMSSM*"
    #sms_pmssm = "RunIIAutumn18FSv3.PMSSM*"
    
    do_lumi   = 0
    do_pmssm  = 1
    do_all    = 0
    do_mc     = 0
    do_signal = 0
    do_signal_genloop = 0

    use_more_mem = False
    use_more_time = True

    if do_lumi:
        options.command = "./skimmer.py --input $INPUT --output $OUTPUT --lumi_report "
        options.dataset = "Run2016*,Run2017*,Run2018*"
        #options.dataset = "Run2016*AOD90*,Run2017*AOD90*,Run2018*AOD90*"
        skimname = "skim_lumiFeb21"
        options.start = True
        options.files_per_job = 10
        options.njobs = 5000
    elif do_pmssm:
        options.command = "./skimmer.py --input $INPUT --output $OUTPUT --sparse "
        options.dataset = sms_pmssm
        skimname = "skim_pmssmMay8"
        options.start = True
        options.files_per_job = 15
        options.njobs = 5000
        use_more_time = 36000
    elif do_all:
        options.command = "./skimmer.py --input $INPUT --output $OUTPUT "
        options.dataset = "Run201*,RunIIFall17MiniAODv2.Fast*,RunIISummer16MiniAODv3.SMS*," + mc_fall17 + "," + mc_summer16
        skimname = "skim_Feb15complete"
        options.start = True
        options.files_per_job = 15
        options.njobs = 5000
    elif do_mc:
        options.command = "./skimmer.py --input $INPUT --output $OUTPUT "
        options.dataset = "RunIIFall17MiniAODv2.Fast*,RunIISummer16MiniAODv3.SMS*," + mc_summer16 + "," + mc_fall17
        skimname = "skim_mc17omega7"
        options.start = True
        options.files_per_job = 15
        options.njobs = 3000
    elif do_signal:
        options.command = "./skimmer.py --input $INPUT --output $OUTPUT "
        #options.dataset = "RunIIFall17MiniAODv2.Fast*,RunIISummer16MiniAODv3.SMS*"
        options.dataset = "RunIIFall17FSv3.SMS*,RunIIAutumn18FSv3.SMS*"
        skimname = "skim_signalLabXY2"
        options.start = True
        options.files_per_job = 15
        options.njobs = 3000
    elif do_signal_genloop:
        options.command = "./skimmer_genloop2.py --input $INPUT --output $OUTPUT "
        options.dataset = "RunIIFall17MiniAODv2.Fast*,RunIIFall17FSv3.SMS*,RunIISummer16MiniAODv3.SMS*,RunIIAutumn18FSv3.SMS*"
        skimname = "skim_SmsGenLoop5"
        use_more_time = False
        use_more_mem = False
        options.start = True
        options.files_per_job = 10
        options.njobs = 4000
    else:
        quit()

        #options.command = "./skimmer.py --input $INPUT --output $OUTPUT "
        #options.command = "./skimmer.py --input $INPUT --output $OUTPUT --sparse "
        #options.command = "./skimmer.py --input $INPUT --output $OUTPUT --lumi_report "
        #options.command = "./skimmer.py --input $INPUT --output $OUTPUT --trigger_study "
        #options.command = "./skimmer.py --input $INPUT --output $OUTPUT --cutflow "
        #options.dataset += sms_pmssm
        #options.dataset = "Run201*,RunIIFall17MiniAODv2.Fast*,RunIISummer16MiniAODv3.SMS*," + mc_fall17 + "," + mc_summer16
        #options.dataset = "RunIIFall17MiniAODv2.Fast*,RunIISummer16MiniAODv3.SMS*," + mc_fall17 + "," + mc_summer16
        #options.dataset = "RunIISummer16MiniAODv3.SMS*," + "," + mc_summer16
        #options.dataset = "Run201*Single*,Run201*EGamma*," + mc_fall17 + "," + mc_summer16
        #options.dataset += "Run2016*SingleElectron*,Run2016*JetHT*"
        #options.dataset += "Run2016*,Run2017*,Run2018*"
        #options.dataset += "Run2016*JetHT*,Run2017*JetHT*,Run2018*JetHT*"
        #options.dataset += ","
        #options.dataset += mc_fall17 + "," + mc_summer16
        #options.dataset += ","
        ###options.dataset += "RunIIFall17MiniAODv2.Fast*,RunIISummer16MiniAODv3.SMS*,RunIIAutumn18FSv3.SMS*,RunIIFall17FSv3.SMS*"
        #options.dataset += "RunIISummer16MiniAODv3.SMS*"
        #options.dataset += "Run2016*"
        #options.dataset += ","
        #options.dataset += "RunIIAutumn18FSv3.SMS-T2tb*,RunIIAutumn18FSv3.SMS-T2bt*,RunIIAutumn18FSv3.SMS-T1btbt*,RunIIFall17FSv3.SMS-T2tb*,RunIIFall17FSv3.SMS-T2bt*,RunIIFall17FSv3.SMS-T1btbt*"
        #options.dataset = "RunIIFall17MiniAODv2.Fast*," + mc_fall17
        #options.dataset = "RunIIFall17MiniAODv2.Fast*,RunIISummer16MiniAODv3.SMS*," + mc_fall17 + "," + mc_summer16
        #options.dataset = "RunIIAutumn18FS.*"
        #options.dataset = "Run201*Single*,Run201*JetHT*,Run2018*EGamma*"
        #options.dataset = "Run2018*EGamma*"
        #options.dataset = "Run201*MET*"
        #options.dataset = "RunIIFall17MiniAODv2.Fast*,RunIISummer16MiniAODv3.SMS*,RunIIAutumn18FSv3.SMS*,RunIIFall17FSv3.SMS*"
        #options.dataset = "RunIIFall17FS.PMSSM*,RunIIAutumn18FS.PMSSM*,RunIIFall17MiniAODv2.Fast*,RunIISummer16MiniAODv3.SMS*,RunIIAutumn18FSv3.SMS*,RunIIFall17FSv3.SMS*"
        #options.dataset = "RunIIFall17FS.PMSSM*,RunIIAutumn18FS.PMSSM*"
        #options.dataset = "Run2017F*," + mc_fall17
        #options.dataset = "RunIIFall17MiniAODv2.Fast*," + mc_fall17 
        #options.dataset = "RunIIFall17MiniAODv2.Fast*,RunIISummer16MiniAODv3.SMS*"
        #options.dataset = "RunIISummer16MiniAODv3.SMS*,Summer16.WJetsToLNu_TuneCUETP8M1*,RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq*,RunIIFall17MiniAODv2.WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM*"
        #options.dataset = "Summer16.QCD_HT500to700_TuneCUETP8M1*,RunIIFall17MiniAODv2.QCD_HT500to700_TuneCP5_13TeV*"
        #options.dataset = "RunIIAutumn18FSv3.SMS-T2bt-LLChipm-ctau10to200-mStop-400to1750-mLSP0to1650_test1-211114_042348-0005-SUS-RunIIAutumn18FSPremix-00155_54*"
        #options.dataset = "RunIIFall17MiniAODv2.FastSim-SMS-*,RunIISummer16MiniAODv3.SMS-T1qqqq*"
        #options.dataset +=  mc_summer16 + ",RunIISummer16MiniAODv3.SMS*"
        #options.dataset += "Run2016B*SingleEl*13*"

    ######## defaults ########

    if not options.output_folder:
        options.output_folder = "../" + skimname

    commands = []

    ntuples = get_ntuple_datasets(options.dataset)
    print ntuples
    with open("ntuple-identifiers", "write") as fout:
        fout.write(str(ntuples))

    for folder in ntuples:
        commands += prepare_command_list(folder, ntuples[folder], options.output_folder, command=options.command, files_per_job=options.files_per_job)
        
    os.system("mkdir -p %s" % options.output_folder + ".condor")

    ## check for already completed output files:
    if options.checkcomplete:
        newcommands = []
        for i in range(len(commands)):
            outfile = commands[i].split(" --output ")[-1].split()[0]
            if "--lumi_report" in commands[i]:
                outfile = outfile.replace(".root", ".json")
            if not os.path.exists(outfile):
                print "not done:", outfile
                newcommands.append(commands[i])
        commands = list(newcommands)

    total_number_of_outputfiles = len(commands)

    ## slim command list:
    with open("%s/%s.arguments" % (options.output_folder + ".condor", skimname), "w") as fout:
        fout.write("\n".join(commands))
    for i in range(len(commands)):
        commands[i] = "$(head -n%s %s/%s.arguments | tail -n1)" % (i+1, options.output_folder + ".condor", skimname)
   
    if options.njobs>0 and len(commands)>options.njobs:
        file_segments = [list(c) for c in more_itertools.divide(options.njobs, commands)]
        
        new_commands = []
        for file_segment in file_segments:
            command = "; ".join(file_segment)
            command = command.replace(";  ;", "; ")
            command = command.replace("; ;", "; ")
            command = command.replace(";;", "; ")
            new_commands.append(command)
        commands = new_commands

    print "total_number_of_outputfiles", total_number_of_outputfiles
   
    do_submission(commands, options.output_folder, condorDir=options.output_folder + ".condor", executable=options.command.split()[0], confirm=not options.start, use_more_mem=use_more_mem, use_more_time=use_more_time)

    #print "Merging..."
    #os.system("./merge_samples.py --start --hadd %s" % options.output_folder) # --json --bril






