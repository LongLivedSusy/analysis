from ROOT import *
from shared_utils import *
import os, sys
gStyle.SetOptStat(0)
gROOT.SetBatch(1)

try: mode = sys.argv[1]
except: 
    mode = 'HE_0p001'
    mode = 'SV'
    mode = 'LambdaSim'

simulation = True
doublgaussmode = False
if 'Lambda' in mode: doublgaussmode = True

if simulation: datamc = 'MC'
else: datamc = 'data'

'''
to draw full ensemble for study:
python tools/SvSignalExtractDraw.py HE_0p001
python tools/SvSignalExtractDraw.py HE_0p010
python tools/SvSignalExtractDraw.py HE_0p100
python tools/SvSignalExtractDraw.py HE_0p500
python tools/SvSignalExtractDraw.py HE_1p000



python tools/SvSignalExtractDraw.py HE_0p02
python tools/SvSignalExtractDraw.py HE_0p05
python tools/SvSignalExtractDraw.py HE_0p003638
python tools/SvSignalExtractDraw.py HE_0p009431
'''

if 'HE' in mode:
    if simulation: name='/nfs/dust/cms/user/tewsalex/CMSSW_10_5_0/src/plots/2020_03_02_V0Fitter/Simulation/'+mode+'.root'    
    else: name='/nfs/dust/cms/user/tewsalex/CMSSW_10_5_0/src/plots/2020_03_02_V0Fitter/HEToVoComparison/Comparison_'+mode+'.root'
    infile=TFile(name)
    hmass = infile.Get('h_tracksWithSV_invMass_KShort')

if mode=='SV' or 'V0' in mode:
    #infile = TFile('V0FitterResult_dcaLTp02.root')
    #infile = TFile('v1fiter_kshort_nochi2.root')
    #canvas = infile.Get('canvas')
    #lops = canvas.GetListOfPrimitives()
    #for p in lops:
    #    print p.GetName()
    #hmass = canvas.GetPrimitive('mass__1').Clone()
    if simulation: infile = TFile('/nfs/dust/cms/user/tewsalex/CMSSW_10_5_0/src/plots/2020_03_02_V0Fitter/Simulation/V0_1p00.root')    
    else: infile = TFile('/nfs/dust/cms/user/tewsalex/CMSSW_10_5_0/src/plots/2020_03_02_V0Fitter/HEToVoComparison/Comparison_V0_0p50.root')
    hmass = infile.Get('mass').Clone('hmass')
    
if mode=='LambdaSim':
    #iname = 'vertex_RunIISummer16DR80PremixB64B10BA-6BA5-E911-B5B2-AC1F6B0DE348SVstuff.root'
    iname = './EDM_output/vertex_higgsino94x_susyall_mChipm100GeV_dm0p16GeV_pu35_SVstuff.root'
    infile = TFile(iname)
    hmass = infile.Get('mass_to1p5_Lambda')
if mode=='LambdaData':
    iname = 'vertex_Run2016GC8DC13E5-2297-E711-B519-0090FAA597B4SVstuff.root'
    infile = TFile(iname)
    hmass = infile.Get('mass_to1p5_Lambda')    


hmass.SetLineWidth(2)
hmass.SetLineColor(kBlack)
hmass.SetMarkerColor(kBlack)
if not hmass.GetSumw2N(): hmass.Sumw2()    
xax = hmass.GetXaxis()
lowedge, highedge = xax.GetBinLowEdge(1), xax.GetBinUpEdge(xax.GetNbins())

#newfile = TFile('rootfiles/kshorts_'+mode+'.root', 'recreate')
newfile = TFile('rootfiles/Lambda_FastSim_higgsino94x_susyall_mChipm100GeV_dm0p16GeV_pu35.root', 'recreate')
c1= mkcanvas('c1')
leg = mklegend(x1=.52, y1=.55, x2=.88, y2=.78, color=kWhite)


def funcBackground(x,par):
    return par[0]+par[1]*x[0]

if doublgaussmode:
    def funcGaussian(x,par):
        return par[0]*TMath.Exp(-(x[0]-par[1])*(x[0]-par[1])/(2*par[2]*par[2]))+par[3]*TMath.Exp(-(x[0]-par[1])*(x[0]-par[1])/(2*par[4]*par[4]))

    def funcFullModel(x,par):
        return par[0]*TMath.Exp(-(x[0]-par[1])*(x[0]-par[1])/(2*par[2]*par[2]))+par[3]+par[4]*x[0]+par[5]*TMath.Exp(-(x[0]-par[1])*(x[0]-par[1])/(2*par[6]*par[6]))

else:
    def funcGaussian(x,par):
        return par[0]*TMath.Exp(-(x[0]-par[1])*(x[0]-par[1])/(2*par[2]*par[2]))

    def funcFullModel(x,par):
        return par[0]*TMath.Exp(-(x[0]-par[1])*(x[0]-par[1])/(2*par[2]*par[2]))+par[3]+par[4]*x[0]
    
if doublgaussmode: fFullModel = TF1('fFullModel', funcFullModel, lowedge,highedge,7)
else: fFullModel = TF1('fFullModel', funcFullModel, lowedge,highedge,5)

fFullModel.SetParameter(0,200)
fFullModel.SetParameter(2,5.26132e-03)

if doublgaussmode:
    fFullModel.SetParameter(0,1.14488e+02)
    fFullModel.SetParameter(1,1.11605e+00)
    fFullModel.SetParameter(3,-3.74985e+02)
    fFullModel.SetParameter(4,3.46574e+02)
    fFullModel.SetParameter(6,2.27701e-03)
else:
    fFullModel.FixParameter(2,5.26132e-03)
    a = 1

if 'Lambda' in mode:
    fFullModel.SetParameter(1,1.115)
    fFullModel.SetParLimits(6,0.0001,1)
else: 
    fFullModel.SetParameter(1,.5)

fFullModel.SetParLimits(2,5.26132e-03-.5*5.26132e-03,5.26132e-03+.5*5.26132e-03)



fitresult = hmass.Fit(fFullModel,'s','',lowedge,highedge)

if doublgaussmode: fGaussian = TF1('fGaussian', funcGaussian,lowedge,highedge,5)
else: fGaussian = TF1('fGaussian', funcGaussian,lowedge,highedge,3)
fGaussian.SetParameter(0,fitresult.Parameter(0))
fGaussian.SetParameter(1,fitresult.Parameter(1))
fGaussian.SetParameter(2,fitresult.Parameter(2))
if doublgaussmode:
    fGaussian.SetParameter(3,fitresult.Parameter(5))
    fGaussian.SetParameter(4,fitresult.Parameter(6))

fBackground = TF1('fBackground', funcBackground,lowedge,highedge,2)
fBackground.SetParameter(0,fitresult.Parameter(3))
fBackground.SetParameter(1,fitresult.Parameter(4))


nsig = fGaussian.Integral(lowedge,highedge)/hmass.GetBinWidth(1)
nbkg = fBackground.Integral(lowedge,highedge)/hmass.GetBinWidth(1)

print 'par 0 was', fGaussian.GetParameter(0)
peak = fGaussian.GetParameter(1)
width = abs(fGaussian.GetParameter(2))
nsigPeak = fGaussian.Integral(peak-width,peak+width)/hmass.GetBinWidth(1)
nbkgPeak = fBackground.Integral(peak-width,peak+width)/hmass.GetBinWidth(1)

print 'signal', nsig
print 'bkg', nbkg



nup = 100
hbkg = hmass.Clone('hbkg')
hbkg.Reset()
hbkg.SetTitle('linear bkg. model')
histoStyler(hbkg, kRed-7)
hbkg.SetFillColor(hbkg.GetLineColor())
for i in range(int(nup*nbkg)):
    hbkg.Fill(fBackground.GetRandom(),1./nup)


function = hmass.GetListOfFunctions()[0].Clone('fmodel')
function.SetLineColor(kBlue)
hmass.GetListOfFunctions()[0].Delete()
    
hsig = hmass.Clone('hsig')
hsig.Reset()
if 'Lambda' in mode: hsig.SetTitle('#Lambda^{0} (gauss fit)')
else: hsig.SetTitle('K_{s}^{0} (gauss fit)')
histoStyler(hsig,  kGreen-9)
hsig.SetFillColor(hsig.GetLineColor())
for i in range(int(nup*nsig)):
    hsig.Fill(fGaussian.GetRandom(),1./nup)   
#hsig.GetListOfFunctions()[0].Delete()     

if not ('Lambda' in mode or 'Data' in mode or simulation): hmass.SetTitle('data (2016G)')
else: hmass.SetTitle('Summer16 MC')
hsig_ = hsig.Clone()
#hratio, pad1, pad2 = FabDraw(c1,leg,hmass,[hbkg,hsig_],datamc=datamc,lumi=epsi, title = '', LinearScale=True, fractionthing='data / fit res.')
hratio, [pad1, pad2] = FabDraw(c1,leg,hmass,[hbkg,hsig_],datamc=datamc,lumi=epsi, title = '', LinearScale=True, fractionthing='data / fit res.')
leg.AddEntry(function, 'sig+bkg fit')

hratio.GetYaxis().SetRangeUser(0.0,2.6)	
hratio.GetXaxis().SetTitle('invariant mass [GeV]')
#hratio.GetYaxis().SetTitle('(B/A*C)/D')
#hratio.GetYaxis().SetRangeUser(-3,3)		
hratio.SetLineColor(kBlack)
for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
    if hratio.GetBinContent(ibin)==0:
        hratio.SetBinContent(ibin,-999)
histoStyler(hratio, kBlack)
hratio.SetMarkerColor(kBlack)
#hratio.GetYaxis().SetTitleSize(0.095)
hratio.GetYaxis().SetTitleOffset(.44)
hratio.SetDirectory(0)


pad1.cd()
function.Draw('same')
hmass.SetTitle('')
#hmass.GetYaxis().SetRangeUser(0,500)
#hbkg.GetYaxis().SetRangeUser(0,500)
#hsig_.GetYaxis().SetRangeUser(0,500)
hmass.Draw('p same')
hmass.Draw('e same')
tl.SetTextSize(1.1*tl.GetTextSize())
font = tl.GetTextFont()
tl.SetTextFont(extraTextFont)
tl.DrawLatex(.15,.62, mode)
tl.SetTextSize(1.0/1.1*tl.GetTextSize())
tl.SetTextFont(font)
tl.DrawLatex(.15,.55, 'n(s) @ peak#pm#sigma= %.2f '%nsigPeak)
tl.DrawLatex(.15,.5, 'n(b) @ peak#pm#sigma= %.2f '%nbkgPeak)
tl.DrawLatex(.15,.44, 'sig. purity: %.4f '% (nsigPeak/(nsigPeak+nbkgPeak)))
c1.Update()
newfile.cd()
c1.Write('./plots/c_Lambda_FastSim_higgsino94x_susyall_mChipm100GeV_dm0p16GeV_pu35')
hsig.Write()
fGaussian.Write('fsignal')
c1.Print('./plots/Lambda_FastSim_higgsino94x_susyall_mChipm100GeV_dm0p16GeV_pu35.png')
print 'just created', newfile.GetName()
newfile.Close()



