#!/bin/env python
# comments: viktor.kutzner@desy.de

import os, sys
from glob import glob
from time import sleep
import datetime
import subprocess
import multiprocessing
import commands

def ShellExec(command):
    os.system(command)


def runParallel(mycommands, runmode, condorDir="bird", cmsbase=False, qsubOptions=False, ncores_percentage=0.60, dontCheckOnJobs=True, use_more_mem=False, use_more_time=False, confirm=True):

    if runmode == "multiprocessing" or runmode == "multi" or runmode == "single":

        if runmode == "single":
            nCores = 1
        else:
            nCores = int(multiprocessing.cpu_count() * ncores_percentage)
        print "Using %i core(s)..." % nCores

        pool = multiprocessing.Pool(nCores)
        return pool.map(ShellExec, mycommands)

    elif runmode == "grid":
        
        if not cmsbase:
            if "CMSSW_BASE" in os.environ:
                cmsbase = os.environ["CMSSW_BASE"]
            else:
                print "Warning, no CMSSW environment set!"
                cmsbase = False

        print "Using CMSSW base", cmsbase

        return runCommands(mycommands, condorDir=condorDir, cmsbase=cmsbase, qsubOptions=qsubOptions, dontCheckOnJobs=dontCheckOnJobs, use_more_mem=use_more_mem, use_more_time=use_more_time, confirm=confirm)


def babysit_jobs(condorDir):

    status, output = commands.getstatusoutput("grep submitted %s/cluster_info" % condorDir)
    cluster_number = output.split()[-1].replace(".", "")

    print "Watching jobs on cluster #%s" % cluster_number

    print "OWNER    BATCH_NAME     SUBMITTED   DONE   RUN    IDLE   HOLD  TOTAL JOB_IDS"
    while True:
        status, line = commands.getstatusoutput("condor_q | grep %s" % cluster_number)
        if status != 0:
            break
        print line

        jobs_done = line.split()[5].replace("_", "0")
        jobs_running = line.split()[6].replace("_", "0")
        jobs_total = line.split()[8]
        if jobs_done == jobs_total:
            break

        sleep(200)

    print "Jobs completed!"
    return 0


def runCommands(mycommands, condorDir="bird", cmsbase=False, qsubOptions=False, dontCheckOnJobs=False, useGUI=False, use_more_mem=False, use_more_time=False, confirm=True):

    jobscript = '''#!/bin/bash
    echo "$QUEUE $JOB $HOST"
    source /cvmfs/cms.cern.ch/cmsset_default.sh
    export SCRAM_ARCH=slc6_amd64_gcc530
    cd CMSBASE
    eval `scramv1 runtime -sh`
    echo $CMSSW_BASE
    cd CWD
    export PYTHONDONTWRITEBYTECODE=1
    export PYTHONPATH=$PYTHONPATH:$(pwd)/../
    export PYTHONPATH=$PYTHONPATH:$(pwd)/../tools
    export PYTHONPATH=$PYTHONPATH:$(pwd)/../../tools
    PROCESSNUM=$(($1 + 1))
    CMD=$(sed ''"$PROCESSNUM"'q;d' BIRDDIR/args)
    echo $CMD
    eval $CMD
    if [ $? -eq 0 ]
    then
        echo "Success"
        exit 0
    else
        echo "Failed"
        exit 112
    fi
    '''
    
    # make some adjustments for running at KNU:
    if 'knu' in os.uname()[1] :
        jobscript = jobscript.replace("slc6_amd64_gcc530", "slc6_amd64_gcc630")
        jobscript = jobscript.replace("cd CWD", "cd CWD \n export PYTHONPATH=$PYTHONPATH:CMSBASE/src/analysis/tools")
    
    cwd = os.getcwd()

    if qsubOptions == False:
        qsubOptions = "h_vmem=4G,h_fsize=100G"

    os.system("mkdir -p %s" % condorDir)

    jobs = []
    nJobsDone = 0
    nJobsFailed = 0

    with open("%s/args" % condorDir, "w+") as fout:
        fout.write("\n".join(mycommands) + "\n")

    with open("%s/runjobs.sh" % condorDir, "w+") as fout:
        jobscript = jobscript.replace('CWD',cwd)
        jobscript = jobscript.replace('BIRDDIR', condorDir)
        if cmsbase:
            jobscript = jobscript.replace('CMSBASE',cmsbase)
        fout.write(jobscript)

    os.chdir(condorDir)

    additional_parameters = ""
    if use_more_mem:
        if use_more_mem == 1:
            use_more_mem = 4096
        additional_parameters += "RequestMemory = %s\n" % use_more_mem
    if use_more_time:
        if use_more_time == 1:
            use_more_time = 86400
        additional_parameters += "+RequestRuntime = %s\n" % use_more_time

    submission_file_content = """
        universe = vanilla
        should_transfer_files = IF_NEEDED
        log = $(Process).log
        executable = /bin/bash
        arguments = runjobs.sh $(Process)
        initialdir = %s
        error = $(Process).sh.e
        output = $(Process).sh.o
        notification = Never
        %s
        max_materialize = 1500
        priority = 0
        Queue %s
    """ % (cwd + "/" + condorDir, additional_parameters, len(mycommands))

    with open("runjobs.submit", 'w') as outfile:
        outfile.write(submission_file_content)

    if confirm:
        raw_input("About to start %s jobs!" % len(mycommands))

    print "Starting submission..."
    os.system("rm %s/*.sh.*" % condorDir)
    os.system("condor_submit runjobs.submit > cluster_info")
    os.chdir("..")
 
    status = babysit_jobs(condorDir)

    return status

