#!/bin/bash
    echo "$QUEUE $JOB $HOST"
    ls -l
    pwd
    # set up cmssw
    source /cvmfs/cms.cern.ch/cmsset_default.sh
    export SCRAM_ARCH=slc6_amd64_gcc530
    #if [[ ! -f $(which voms-proxy-info) ]]
    # then
      source /cvmfs/grid.desy.de/etc/profile.d/grid-ui-env.sh
    # fi
    cd /afs/desy.de/user/k/kutznerv/cmssw/CMSSW_11_2_3
    eval `scramv1 runtime -sh`
    echo $CMSSW_BASE
    # set up proxy
    cd ~
    export X509_USER_PROXY=$(pwd)/proxy
    echo X509_USER_PROXY $X509_USER_PROXY
    voms-proxy-info
    # all done, now prepare to run command
    cd /nfs/dust/cms/user/kutznerv/shorttrack/analysis/disappearing-track-tag/2017-short-tracks-may21
    export PYTHONDONTWRITEBYTECODE=1
    export PYTHONPATH=$PYTHONPATH:$(pwd)/../
    export PYTHONPATH=$PYTHONPATH:$(pwd)/../tools
    export PYTHONPATH=$PYTHONPATH:$(pwd)/../../tools
    PROCESSNUM=$(($1 + 1))
    CMD=$(sed ''"$PROCESSNUM"'q;d' condor/args)
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
    