#!/bin/env python
import os, glob
from GridEngineTools import runParallel

def prepare_command_list(ntuples_folder, samples, output_folder, files_per_job = 5, files_per_sample = -1, command = "./looper.py $INPUT $OUTPUT 0 0"):

    commands = []

    for sample in samples:

        ifile_list = sorted(glob.glob(ntuples_folder + "/" + sample + "*.root"))
        
        if files_per_sample != -1:
            ifile_list = ifile_list[:files_per_sample]
        
        if len(ifile_list)==0:
            continue

        print "Looping over %s files (%s)" % (len(ifile_list), sample)
       
        file_segments = [ifile_list[x:x+files_per_job] for x in range(0,len(ifile_list),files_per_job)]

        for inFile_segment in file_segments:
                
            out_tree = output_folder + "/" + inFile_segment[0].split("/")[-1].split(".root")[0] + "_fakes.root"
            cmd = command.replace("$INPUT", str(inFile_segment).replace(", ", ",").replace("[", "").replace("]", ""))
            cmd = cmd.replace("$OUTPUT", out_tree)
            commands.append(cmd)
                        
    return commands


def do_submission(commands, output_folder, executable = "looper.py", runmode = "grid"):

    raw_input("submit %s jobs?" % len(commands))
    os.system("mkdir -p %s" % output_folder)
    os.system("cp %s %s/" % (executable, output_folder))
    runParallel(commands, runmode, dontCheckOnJobs=True)

