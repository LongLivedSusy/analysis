from ROOT import *
from utils import *
import os, sys


os.system("find /nfs/dust/cms/user/beinsam/CommonSamples/MC_BSM/CompressedHiggsino/RadiativeMu_2016Fast/v2/ -type f -printf \"%f\n\" | sed 's/_pu.*//g' | sort --unique > uniquehiggsinos.txt")

ftext = open('uniquehiggsinos.txt')
text = ftext.readlines()
ftext.close()

c1 = mkcanvas('c1')
hist = TH2F('','',100,80,680,100,0,6)
histoStyler(hist, kBlack)
xax = hist.GetXaxis()
yax = hist.GetYaxis()
xax.SetTitle('m(#chi^{#pm}_{1}) (GeV)')
yax.SetTitle('#Deltam^{#pm} (GeV)')
for iline, line in enumerate(text):
    masschipm = float(line.split('mChipm')[-1].split('GeV_')[0].replace('p','.'))
    dm = float(line.split('dm')[-1].split('GeV')[0].replace('p','.'))
    print 'got', masschipm, dm
    hist.Fill(masschipm, dm)
    if iline==0: hist.Fill(masschipm, dm)

hist.Draw('colz')
c1.Update()
pause()


