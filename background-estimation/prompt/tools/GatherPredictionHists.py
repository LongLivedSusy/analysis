from ROOT import *
from utils import *

fofinterest = TFile('output/totalweightedbkgsDataDrivenMC.root')
fofinterest.ls()


hElectron = fofinterest.Get('hElBaseline_BinNumberMethod')
hMuon = fofinterest.Get('hMuBaseline_BinNumberMethod')
hPion = fofinterest.Get('hPiBaseline_BinNumberMethod')


fnew = TFile('prompt-bg-results.root','recreate')

hElectron.Write()
hMuon.Write()
hPion.Write()


print 'just created', fnew.GetName()

fnew.Close()