#!/bin/env python
import os, glob
import commands
from optparse import OptionParser
import GridEngineTools
import time

def remove_failed_output_files(condor_dir):
    status, failed_jobs = commands.getstatusoutput("grep Failed %s/*.sh.o*" % condor_dir)
    jobs_list = failed_jobs.split("\n")

    for i_job, job in enumerate(jobs_list):

        if i_job % 100 == 0:
            print "%s / %s" % (i_job, len(jobs_list) )

        job_dir = job.split("/")[-2]
        job_id = job.split("/")[-1].split(".")[0]

        status, job_command = commands.getstatusoutput("cat %s/args | sed '%s!d'" % (job_dir, int(job_id)+1) )

        output_root_file = job_command.split("--output")[1]
        output_json_file = output_root_file.replace(".root", ".json")

        print "removing", output_root_file, output_json_file
        os.system("rm %s" % output_root_file)
        os.system("rm %s" % output_json_file)


def get_info(condor_dir, showfailed = False):
    status, failed_jobs = commands.getstatusoutput("grep Failed %s/*.sh.o* | wc -l" % condor_dir)
    status, succeeded_jobs = commands.getstatusoutput("grep Success %s/*.sh.o* | wc -l" % condor_dir)
    status, all_jobs = commands.getstatusoutput("wc -l %s/args" % condor_dir)

    n_failed_jobs = int(failed_jobs.split()[0])
    n_succeeded_jobs = int(succeeded_jobs.split()[0])
    n_all = int(all_jobs.split()[0])

    print "%s / %s jobs succeeded (%s failed): %.2f done" % (n_succeeded_jobs, n_all, n_failed_jobs, float(n_succeeded_jobs)/n_all)

    if showfailed and failed_jobs>0:
        os.system("grep Failed %s/*.sh.o*" % condor_dir)
        
    return {"success": n_succeeded_jobs, "njobs": n_all, "fail": n_failed_jobs, "percent_done": float(n_succeeded_jobs)/n_all}


def rewrite_failed_args(condor_dir):
    if condor_dir[-1] == "/":
        condor_dir = condor_dir[:-1]

    #print "Warning, currently this works ONCE!"

    #os.system("cp -n %s/args %s/args.complete" % (condor_dir, condor_dir))

    status, succeeded_jobs = commands.getstatusoutput("grep Success %s/*.sh.o*" % condor_dir)
    status, failed_jobs = commands.getstatusoutput("grep Failed %s/*.sh.o*" % condor_dir)
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
        #index = int(arg.split("--index")[-1])
        if i_arg not in succeeded_jobs:
            failed_args.append(arg)
        #if i_arg in failed_jobs: 
        #    failed_args.append(arg)

    #print failed_args

    condor_resubmit_dir = condor_dir + "." + str(int(time.time()))
    os.system("mkdir -p %s" % condor_resubmit_dir)
    os.system("cp %s/*.sh %s" % (condor_dir, condor_resubmit_dir))
    os.system("cp %s/*.submit %s" % (condor_dir, condor_resubmit_dir))

    #if not status: quit()

    with open("%s/args" % condor_resubmit_dir, "w+") as fout:
        fout.write("\n".join(failed_args))

    #os.system("rm %s/*.sh.*" % condor_dir)

    #update condor queue statement:
    os.system("sed -i '/%s/%s' %s/runjobs.submit" % (condor_dir, condor_resubmit_dir, condor_resubmit_dir))
    os.system("sed -i '/Queue/c\        Queue %s' %s/runjobs.submit" % (len(failed_args)-1, condor_resubmit_dir))

    return condor_resubmit_dir


def resubmit(condor_dir):
    condor_resubmit_dir = rewrite_failed_args(condor_dir)
    raw_input("Resubmit?...")
    os.system("cd %s; condor_submit runjobs.submit > cluster_info" % condor_resubmit_dir)
    GridEngineTools.babysit_jobs(condor_resubmit_dir)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--rmfailed", dest="rmfailed", action="store_true")
    parser.add_option("--info", dest="info", action="store_true")
    parser.add_option("--babysit", dest="babysit", action="store_true")
    parser.add_option("--resubmit", dest="resubmit", action="store_true")
    (options, args) = parser.parse_args()

    condor_dir = args[0]

    get_info(condor_dir, showfailed = True)

    if options.rmfailed:
        remove_failed_output_files(condor_dir)

    if options.babysit:
        GridEngineTools.babysit_jobs(condorDir)
    
    if options.resubmit:
        resubmit(condor_dir)

