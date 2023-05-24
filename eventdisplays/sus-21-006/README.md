# SUS-21-006

Search for disappearing tracks

This was adapted from TOP-21-007.

## Setup
```bash
cmsrel CMSSW_10_6_20
cd CMSSW_10_6_20/src/
cmsenv
git clone https://github.com/cms-outreach/ispy-analyzers.git ISpy/Analyzers
git clone https://github.com/cms-outreach/ispy-services.git ISpy/Services
scram b
```

## Generating output files:

To pickup relevant events from the grid, and to produce `ig` file run
```bash
cmsRun ispy_SUS-21-006.py
```

## Event display in iSPY

view output in http://ispy-webgl-dev.web.cern.ch/


## Events info

| *RunNumber* | *EventNumber* | *Info* |

See separate disappearingTrackEvents.list.sorted file