#!/bin/env python
import os, sys
from glob import glob
from time import sleep
import datetime
import subprocess
import multiprocessing
from optparse import OptionParser
import time
import commands

# condor grid submission tool
# comments: viktor.kutzner@desy.de
#
# ===============mysubmit.py================
# import os
# import GridEngineTools
# 
# os.system("mkdir -p test")
# commands = ["ls -l > test/out1", "ls -lha > test/out2", "whoami > test/out3"]
# GridEngineTools.runParallel(commands, "grid")
# # ===============mysubmit.py================
#
# $ ./mysubmit.py                         # submit jobs
# $ python GridEngineTools.py             # check jobs
# $ python GridEngineTools.py --resubmit  # resubmit failed jobs


def ShellExec(command):
    os.system(command)


def runParallel(mycommands, runmode, condorDir="condor", cmsbase=False, qsubOptions=False, ncores_percentage=0.60, dontCheckOnJobs=True, use_more_mem=False, use_more_time=False, confirm=True, babysit = True):

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

        return runCommands(mycommands, condorDir=condorDir, cmsbase=cmsbase, qsubOptions=qsubOptions, dontCheckOnJobs=dontCheckOnJobs, use_more_mem=use_more_mem, use_more_time=use_more_time, confirm=confirm, babysit=babysit)


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


def runCommands(mycommands, condorDir="condor", cmsbase=False, qsubOptions=False, dontCheckOnJobs=False, useGUI=False, use_more_mem=False, use_more_time=False, confirm=True, babysit=True):

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
 
    if babysit:
        status = babysit_jobs(condorDir)
        return status


def get_info(condor_dir, showfailed = False):

    #status, failed_jobs = commands.getstatusoutput("grep Failed %s/*.sh.o* | wc -l" % condor_dir)
    status, failed_jobs = commands.getstatusoutput("grep -L 'Normal termination' %s/*.log | wc -l" % condor_dir)
    #status, succeeded_jobs = commands.getstatusoutput("grep Success %s/*.sh.o* | wc -l" % condor_dir)
    status, succeeded_jobs = commands.getstatusoutput("grep 'Normal termination' %s/*.log | wc -l" % condor_dir)
    status, all_jobs = commands.getstatusoutput("wc -l %s/args" % condor_dir)

    n_failed_jobs = int(failed_jobs.split()[0])
    n_succeeded_jobs = int(succeeded_jobs.split()[0])
    n_all = int(all_jobs.split()[0])

    print "%s / %s jobs succeeded (%s failed): %.2f done" % (n_succeeded_jobs, n_all, n_failed_jobs, float(n_succeeded_jobs)/n_all)

    if showfailed and failed_jobs>0:
        os.system("grep -L 'Normal termination' %s/*.log" % condor_dir)

    return {"success": n_succeeded_jobs, "njobs": n_all, "fail": n_failed_jobs, "percent_done": float(n_succeeded_jobs)/n_all}


def resubmit(condor_dir):

    if condor_dir[-1] == "/":
        condor_dir = condor_dir[:-1]

    status, succeeded_jobs = commands.getstatusoutput("grep Success %s/*.sh.o*" % condor_dir)
    status, failed_jobs = commands.getstatusoutput("grep -L 'Normal termination' %s/*.log" % condor_dir)
    #status, failed_jobs = commands.getstatusoutput("grep Failed %s/*.sh.o*" % condor_dir)
    status, all_args = commands.getstatusoutput("cat %s/args" % condor_dir)

    succeeded_jobs = succeeded_jobs.split("\n")
    failed_jobs = failed_jobs.split("\n")
    all_args = all_args.split("\n")
    failed_args = []

    for i, succeeded_job in enumerate(succeeded_jobs):
        succeeded_jobs[i] = int( succeeded_job.split("/")[-1].split(".")[0] )

    for i, failed_job in enumerate(failed_jobs):
        failed_jobs[i] = int( failed_job.split("/")[-1].split(".")[0] )
       
    for i_arg, arg in enumerate(all_args):
        if i_arg not in succeeded_jobs:
            failed_args.append(arg)

    condor_resubmit_dir = condor_dir + "." + str(int(time.time()))
    os.system("mkdir -p %s" % condor_resubmit_dir)
    os.system("cp %s/*.sh %s" % (condor_dir, condor_resubmit_dir))
    os.system("cp %s/*.submit %s" % (condor_dir, condor_resubmit_dir))

    with open("%s/args" % condor_resubmit_dir, "w+") as fout:
        fout.write("\n".join(failed_args))

    # update condor queue statement:
    #os.system("sed -i '/%s/%s' %s/runjobs.submit" % (condor_dir, condor_resubmit_dir, condor_resubmit_dir))
    os.system("sed -i '/Queue/c\        Queue %s' %s/runjobs.submit" % (len(failed_args)-1, condor_resubmit_dir))

    # update condor output directory path:
    os.system("sed -i '/initialdir/c\        initialdir = %s' %s/runjobs.submit" % (os.path.abspath(condor_resubmit_dir), condor_resubmit_dir))

    raw_input("Resubmit?...")
    os.system("cd %s; condor_submit runjobs.submit > cluster_info" % condor_resubmit_dir)
    babysit_jobs(condor_resubmit_dir)


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--info", dest="info", action="store_true")
    parser.add_option("--babysit", dest="babysit", action="store_true")
    parser.add_option("--resubmit", dest="resubmit", action="store_true")
    (options, args) = parser.parse_args()

    if len(args)>0:
        condor_dir = args[0]
    else:
        jobs.condor = "condor"

    get_info(condor_dir, showfailed = True)

    if options.babysit:
        babysit_jobs(condorDir)
    
    if options.resubmit:
        resubmit(condor_dir)

