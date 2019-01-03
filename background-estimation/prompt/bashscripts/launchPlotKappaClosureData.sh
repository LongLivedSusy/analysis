#python tools/ahadd.py -f mergedRoots/mergedRun2016SingleEl_Split.root output/smallchunks/PromptBkgHists_*SingleEl*.root && python tools/ahadd.py -f mergedRoots/mergedRun2016SingleMu_Split.root output/smallchunks/PromptBkgHists_*SingleMu*.root
python tools/PlotKappaClosureAndDataSplit.py PixOnly
python tools/PlotKappaClosureAndDataSplit.py PixAndStrips
python tools/PlotKappaClosureAndDataSplit.py PixOrStrips 
