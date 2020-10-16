#!/bin/bash
    echo "$QUEUE $JOB $HOST"
    source /cvmfs/cms.cern.ch/cmsset_default.sh
    export SCRAM_ARCH=slc6_amd64_gcc530
    cd /afs/desy.de/user/k/kutznerv/cmssw/CMSSW_10_1_7
    eval `scramv1 runtime -sh`
    echo $CMSSW_BASE
    cd /nfs/dust/cms/user/kutznerv/shorttrack/analysis/disappearing-track-tag/2017-long-tracks-may20-dxy-chi2-v2
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
    