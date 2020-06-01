from ROOT import *
from utils import *
from glob import glob
gStyle.SetOptStat(0)
gROOT.SetBatch(1)

rootlist = glob('rootfiles/*HE*.root')

hnsigvscut = TH1F('hnsigvscut','n(s) vs DCA cut', 1100,0,.11)
xax = hnsigvscut.GetXaxis()

x, y = [], []
for rfile in rootlist:
    f = TFile(rfile)
    h = f.Get('hsig')
    func = f.Get('fsignal')
    dcacut = float(rfile.split('/')[-1].split('HE_')[-1].split('.root')[0].replace('p','.'))
    nsig = func.Integral(func.GetParameter(1)-func.GetParameter(2), func.GetParameter(1)+func.GetParameter(2))/h.GetBinWidth(1)
    print 'nsig', nsig
    hnsigvscut.SetBinContent(xax.FindBin(dcacut), nsig)
    hnsigvscut.SetBinError(xax.FindBin(dcacut), TMath.Sqrt(nsig))

c1 = mkcanvas('c1')
hnsigvscut.GetYaxis().SetRangeUser(1,10000)
hnsigvscut.GetYaxis().SetTitle('extracted signal')
hnsigvscut.GetXaxis().SetTitle('DCA cut (DCA<X)')
hnsigvscut.SetMarkerSize(2)
hnsigvscut.SetMarkerStyle(22)
hnsigvscut.SetMarkerColor(kBlue)
hnsigvscut.Draw('p text')
hnsigvscut.Fit('pol4','','s',0,.1)
func = hnsigvscut.GetListOfFunctions()[0]
xval = 223.99
xval = 475.33
solution = func.GetX(xval)
print 'f(223.99) =',solution
tline = TLine()
tline.DrawLine(0,xval,.11,xval)
tline.DrawLine(solution,1,solution,10000)
tl.SetTextSize(.65*tl.GetTextSize())
tl.DrawLatex(.545,.53, '(%.6f, %6f)' % (solution, xval))
c1.SetLogx()
c1.SetLogy()
c1.Update()
c1.Print('nsigvsdcacut.png')
#pause()
    
