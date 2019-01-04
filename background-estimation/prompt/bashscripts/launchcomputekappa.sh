python tools/mergeMcHists.py "RawKappaMaps/RawKapps_TTJets_PixOnly.root" "output/smallchunks/TagnProbeHists_TTJets*PixOnly.root"
python tools/mergeMcHists.py "RawKappaMaps/RawKapps_DYJets_PixOnly.root" "output/smallchunks/TagnProbeHists_DYJets*PixOnly.root"
python tools/mergeMcHists.py "RawKappaMaps/RawKapps_WJets_PixOnly.root" "output/smallchunks/TagnProbeHists_WJetsToLNu*PixOnly.root"
python tools/mergeMcHists.py "RawKappaMaps/RawKapps_AllMC_PixOnly.root" "output/smallchunks/TagnProbeHists_*Tune*PixOnly.root"
python tools/ahadd.py -f      RawKappaMaps/RawKapps_Run2016_PixOnly.root output/smallchunks/TagnProbeHists_Run2016*PixOnly.root

python tools/ComputeKappa.py RawKappaMaps/RawKapps_TTJets_PixOnly.root KappaTTJets_PixOnly.root
mv KappaTTJets_PixOnly.root usefulthings/ 
python tools/ComputeKappa.py RawKappaMaps/RawKapps_DYJets_PixOnly.root KappaDYJets_PixOnly.root
mv KappaDYJets_PixOnly.root usefulthings/
python tools/ComputeKappa.py RawKappaMaps/RawKapps_AllMC_PixOnly.root KappaAllMC_PixOnly.root
mv KappaAllMC_PixOnly.root usefulthings/
python tools/ComputeKappa.py RawKappaMaps/RawKapps_WJets_PixOnly.root KappaWJets_PixOnly.root
mv KappaWJets_PixOnly.root usefulthings/
python tools/ComputeKappa.py RawKappaMaps/RawKapps_Run2016_PixOnly.root KappaRun2016_PixOnly.root
mv KappaRun2016_PixOnly.root usefulthings/


python tools/mergeMcHists.py "RawKappaMaps/RawKapps_TTJets_PixAndStrips.root" "output/smallchunks/TagnProbeHists_TTJets*PixAndStrips.root"
python tools/mergeMcHists.py "RawKappaMaps/RawKapps_DYJets_PixAndStrips.root" "output/smallchunks/TagnProbeHists_DYJets*PixAndStrips.root"
python tools/mergeMcHists.py "RawKappaMaps/RawKapps_AllMC_PixAndStrips.root" "output/smallchunks/TagnProbeHists_*Tune*PixAndStrips.root"
python tools/mergeMcHists.py "RawKappaMaps/RawKapps_WJets_PixAndStrips.root" "output/smallchunks/TagnProbeHists_WJetsToLNu_*PixAndStrips.root"
python tools/ahadd.py -f     RawKappaMaps/RawKapps_Run2016_PixAndStrips.root  output/smallchunks/TagnProbeHists_Run2016*PixAndStrips.root

python tools/ComputeKappa.py RawKappaMaps/RawKapps_TTJets_PixAndStrips.root KappaTTJets_PixAndStrips.root
mv KappaTTJets_PixAndStrips.root usefulthings/ 
python tools/ComputeKappa.py RawKappaMaps/RawKapps_DYJets_PixAndStrips.root KappaDYJets_PixAndStrips.root
mv KappaDYJets_PixAndStrips.root usefulthings/ 
python tools/ComputeKappa.py RawKappaMaps/RawKapps_AllMC_PixAndStrips.root KappaAllMC_PixAndStrips.root
mv KappaAllMC_PixAndStrips.root usefulthings/ 
python tools/ComputeKappa.py RawKappaMaps/RawKapps_WJets_PixAndStrips.root KappaWJets_PixAndStrips.root
mv KappaWJets_PixAndStrips.root usefulthings/
python tools/ComputeKappa.py RawKappaMaps/RawKapps_Run2016_PixAndStrips.root KappaRun2016_PixAndStrips.root
mv KappaRun2016_PixAndStrips.root usefulthings/

'''
python tools/mergeMcHists.py "RawKappaMaps/RawKapps_TTJets_PixOrStrips.root" "output/smallchunks/TagnProbeHists_TTJets*PixOrStrips.root"
python tools/mergeMcHists.py "RawKappaMaps/RawKapps_DYJets_PixOrStrips.root" "output/smallchunks/TagnProbeHists_DYJets*PixOrStrips.root"
python tools/mergeMcHists.py "RawKappaMaps/RawKapps_AllMC_PixOrStrips.root" "output/smallchunks/TagnProbeHists_*Tune*PixOrStrips.root"
python tools/mergeMcHists.py "RawKappaMaps/RawKapps_WJets_PixOrStrips.root" "output/smallchunks/TagnProbeHists_WJetsToLNu_*PixOrStrips.root"
python tools/ahadd.py -f      RawKappaMaps/RawKapps_Run2016_PixOrStrips.root output/smallchunks/TagnProbeHists_Run2016*PixOrStrips.root


python tools/ComputeKappa.py RawKappaMaps/RawKapps_TTJets_PixOrStrips.root KappaTTJets_PixOrStrips.root
mv KappaTTJets_PixOrStrips.root usefulthings/
python tools/ComputeKappa.py RawKappaMaps/RawKapps_DYJets_PixOrStrips.root KappaDYJets_PixOrStrips.root
mv KappaDYJets_PixOrStrips.root usefulthings/
python tools/ComputeKappa.py RawKappaMaps/RawKapps_AllMC_PixOrStrips.root KappaAllMC_PixOrStrips.root
mv KappaAllMC_PixOrStrips.root usefulthings/
python tools/ComputeKappa.py RawKappaMaps/RawKapps_WJets_PixOrStrips.root KappaWJets_PixOrStrips.root
mv KappaWJets_PixOrStrips.root usefulthings/
python tools/ComputeKappa.py RawKappaMaps/RawKapps_Run2016_PixOrStrips.root KappaRun2016_PixOrStrips.root
mv KappaRun2016_PixOrStrips.root usefulthings/
'''

echo python tools/CompareInvariantMass.py
echo python tools/PlotKappaClosureAndDataSplit.py PixOnly && python tools/PlotKappaClosureAndDataSplit.py PixAndStrips 
#echo python tools/PlotKappaClosureAndDataSplit.py PixOrStrips