from ROOT import *
import numpy as np


def main():
    hData = TH1F('hData','hData',18,-3,3)
    histoStyler(hData,kBlack)
    hData.SetMarkerStyle(20)
    
    hTemplate1 = TH1F('hTemplate1','hTemplate1',18,-3,3)
    histoStyler(hTemplate1,kAzure+2)
    hTemplate1.SetFillColor(kAzure)
    hTemplate2 = TH1F('hTemplate2','hTemplate2',18,-3,3)
    histoStyler(hTemplate2,kRed+2)
    hTemplate1.SetFillColor(kRed)
    
    hData.FillRandom('gaus',500)
    hData.FillRandom('pol2',1000)
    hTemplate1.FillRandom('gaus',100000)
    hTemplate2.FillRandom('pol2',100000)
    
    c1 = mkcanvas()
    shapeArray = TObjArray(2)
    shapeArray.Add(hTemplate1)
    shapeArray.Add(hTemplate2)
    
    fit = TFractionFitter(hData, shapeArray)
    #alternatively:
    #fit.SetData(hData)
    #fit.SetMC(0,hTemplate1)
    
    fit.Constrain(0, 0.0, 10.0)
    fit.Constrain(1, 0.0, 10.0)
    status = fit.Fit()
    
    norm1_FromFit = np.zeros(1, dtype=float)
    norm1err_FromFit =np.zeros(1, dtype=float)
    fit.GetResult(0, norm1_FromFit, norm1err_FromFit)
    norm2_FromFit = np.zeros(2, dtype=float)
    norm2err_FromFit =np.zeros(2, dtype=float)
    fit.GetResult(1, norm2_FromFit, norm2err_FromFit)
    
    print 'extracted fit par: n1 =', norm1_FromFit, '+/-', norm1err_FromFit
    print 'extracted fit par: n2 =', norm2_FromFit, '+/-', norm2err_FromFit
    
    result = fit.GetPlot()
    hData.GetYaxis().SetRangeUser(0,1.5*hData.GetMaximum())
    hData.Draw("Ep same")
    print 'this is the data'
    c1.Update()
    pause()
    
    result.SetLineColor(kViolet)
    result.SetLineWidth(2)
    result.Draw("same")
    c1.Update()
    print 'this is the post-fit model'
    pause()
    
    hTemplate1.SetFillStyle(3005)
    hTemplate1.Scale(hData.Integral() * norm1_FromFit[0]/hTemplate1.Integral())
    hTemplate2.Scale(hData.Integral() * norm2_FromFit[0]/hTemplate2.Integral())
    hTemplate1.Draw('hist same')
    hTemplate2.SetFillStyle(3004)
    hTemplate2.SetFillColor(kBlue)
    hTemplate2.Draw('hist same')
    c1.Update()
    print 'these are the templates'
    pause()
    

def pause(str_='push enter key when ready'):
        import sys
        print str_
        sys.stdout.flush() 
        raw_input('')
        
def histoStyler(h,color):
    h.SetLineWidth(2)
    h.SetLineColor(color)
    h.SetMarkerColor(color)
    size = 0.055
    font = 132
    h.GetXaxis().SetLabelFont(font)
    h.GetYaxis().SetLabelFont(font)
    h.GetXaxis().SetTitleFont(font)
    h.GetYaxis().SetTitleFont(font)
    h.GetYaxis().SetTitleSize(size)
    h.GetXaxis().SetTitleSize(size)
    h.GetXaxis().SetLabelSize(size)   
    h.GetYaxis().SetLabelSize(size)
    h.GetXaxis().SetTitleOffset(1.0)
    h.GetYaxis().SetTitleOffset(1.05)
    h.Sumw2()

def mkcanvas(name='c1'):
    c1 = TCanvas(name,name,700,630)
    c1.SetBottomMargin(.15)
    c1.SetLeftMargin(.14)
    return c1    

main()
