#!/bin/env python
# comments: viktor.kutzner@desy.de

import os, sys
from glob import glob
from time import sleep
import datetime
import subprocess
import multiprocessing

def runParallel(commands, runmode, dryrun=False, cmsbase=False, qsubOptions=False, ncores_percentage=0.70, dontCheckOnJobs=True, use_more_mem=False, use_more_time=False, burst_mode=False):

    if runmode == "multi":

        nCores = int(multiprocessing.cpu_count() * ncores_percentage)
        print "Using %i cores" % nCores

        pool = multiprocessing.Pool(nCores)
        return pool.map(ShellExec, commands)

    if runmode == "grid":
        
        if not cmsbase:
            if "CMSSW_BASE" in os.environ:
                cmsbase = os.environ["CMSSW_BASE"]
            else:
                print "Warning, no CMSSW environment set!"
                cmsbase = False

        print "Using CMSSW base", cmsbase

        return runCommands(commands, dryrun=dryrun, cmsbase=cmsbase, qsubOptions=qsubOptions, dontCheckOnJobs=dontCheckOnJobs, use_more_mem=use_more_mem, use_more_time=use_more_time, burst_mode=burst_mode)


def runCommands(commands, dryrun=False, birdDir="bird", cmsbase=False, qsubOptions=False, dontCheckOnJobs=False, useGUI=False, use_more_mem=False, use_more_time=False, burst_mode=False):

    jobscript = '''#!/bin/bash
    echo "$QUEUE $JOB $HOST"
    source /cvmfs/cms.cern.ch/cmsset_default.sh
    export SCRAM_ARCH=slc6_amd64_gcc530
    cd CMSBASE
    eval `scramv1 runtime -sh`
    echo $CMSSW_BASE
    cd CWD
    PROCESSNUM=$(($1 + 1))
    CMD=$(sed ''"$PROCESSNUM"'q;d' BIRDDIR/args)
    eval $CMD
    if [ $? -eq 0 ]
    then
        echo "Success"
    else
        echo "Failed"
    fi
    '''
    
    # make some adjustments for running at KNU:
    if 'knu' in os.uname()[1] :
        jobscript = jobscript.replace("slc6_amd64_gcc530", "slc6_amd64_gcc630")
        jobscript = jobscript.replace("cd CWD", "cd CWD \n export PYTHONPATH=$PYTHONPATH:CMSBASE/src/analysis/tools")
    
    cwd = os.getcwd()

    if qsubOptions == False:
        qsubOptions = "h_vmem=4G,h_fsize=100G"

    os.system("mkdir -p %s" % birdDir)

    with open("%s/args" % birdDir, "w+") as fout:
        fout.write("\n".join(commands) + "\n")

    with open("%s/runjobs.sh" % birdDir, "w+") as fout:
        jobscript = jobscript.replace('CWD',cwd)
        jobscript = jobscript.replace('BIRDDIR', birdDir)
        if cmsbase:
            jobscript = jobscript.replace('CMSBASE',cmsbase)
        fout.write(jobscript)

    os.chdir(birdDir)

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
        max_materialize = 1000
        priority = 0
        Queue %s
    """ % (cwd + "/" + birdDir, additional_parameters, len(commands))

    with open("runjobs.submit", 'w') as outfile:
        outfile.write(submission_file_content)

    print "Starting submission..."
    os.system("condor_submit runjobs.submit")
    os.chdir("..")

    print "Jobs are running!"

    if dontCheckOnJobs: return

    # Check if jobs are finished:

    if not useGUI:

        interval = 5
        counter = 0
        while(len(jobs) != nJobsDone + nJobsFailed):
            counter += 1
            nJobsDone = 0
            nJobsFailed = 0
            for job in jobs:
                try:
                    jobOutputFile = glob("%s/%s.sh.o*" % (birdDir,job))[0]
                    ofile = open(jobOutputFile)
                    ofileContents = ofile.read()
                    if "Success" in ofileContents:
                        nJobsDone += 1
                    if "Failed" in ofileContents:
                        nJobsFailed += 1
                except:
                    pass

            PercentProcessed = int( 20 * float(nJobsDone + nJobsFailed) / len(jobs) )
            line = "[" + PercentProcessed*"#" + (20-PercentProcessed)*" " + "]\t" + "%s jobs, running: %s, done: %s, failed: %s. Running since %is..." % (len(jobs), len(jobs)-nJobsDone-nJobsFailed, nJobsDone, nJobsFailed, counter*interval)
            print line

            sleep(interval)
            
        return 0

    else:
   
        line = ""
        import curses

        class curses_screen:
            def __enter__(self):
                self.stdscr = curses.initscr()
                curses.cbreak()
                curses.noecho()
                self.stdscr.keypad(1)
                SCREEN_HEIGHT, SCREEN_WIDTH = self.stdscr.getmaxyx()
                return self.stdscr
            def __exit__(self,a,b,c):
                curses.nocbreak()
                self.stdscr.keypad(0)
                curses.echo()
                curses.endwin()

        with curses_screen() as stdscr:

            interval = 5
            counter = 0

            while(len(jobs) != nJobsDone + nJobsFailed):
                counter += 1
                nJobsDone = 0
                nJobsFailed = 0
                for job in jobs:
                    try:
                        jobOutputFile = glob("%s/%s.sh.o*" % (birdDir,job))[0]
                        ofile = open(jobOutputFile)
                        ofileContents = ofile.read()
                        if "Success" in ofileContents:
                            nJobsDone += 1
                        if "Failed" in ofileContents:
                            nJobsFailed += 1
                    except:
                        pass

                PercentProcessed = int( 20 * float(nJobsDone + nJobsFailed) / len(jobs) )
                line = "[" + PercentProcessed*"#" + (20-PercentProcessed)*" " + "]\t" + "%s jobs, running: %s, done: %s, failed: %s. Running since %is..." % (len(jobs), len(jobs)-nJobsDone-nJobsFailed, nJobsDone, nJobsFailed, counter*interval)
                stdscr.addstr(2,4, line)
                stdscr.refresh()

                sleep(interval)

        print line

    if nJobsFailed>0:

        print "There were failed jobs. Check error output files:\n"
        jobErrorFiles = glob("%s/%s.sh.e*" % (birdDir,job))
        for jobErrorFile in jobErrorFiles:
            print jobErrorFile

        print "\nAfter checking, resubmit with the following commands:"
        for shFile in glob("%s/%s.sh" % (birdDir,job)):
            print 'qsub -l %s -cwd ' % qsubOptions + shFile + '&'

        quit()

    return 0

