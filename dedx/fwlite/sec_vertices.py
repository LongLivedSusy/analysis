import DataFormats.FWLite as fwlite
import ROOT 
import math
import numpy as np
from commons import findMinDr_track, invariantMassTracks, findMatch_tracktrack_new, invariantMassTracksAsPions
import sys
from glob import glob
from shared_utils import *
#############################################
##    Looking at secondary vertices        ##
#############################################

#python tools/sec_vertices.py "edm_RunIISummer16DR80Premix*.root"
#python tools/sec_vertices.py "edm_Run2016G*.root"
    
try: 
    inputfiles = glob(sys.argv[1])
except: 
    #inputfiles = glob("./EDM_output/edm_RunIISummer*.root")
    #inputfiles = glob("./EDM_output/edm_higgsino94x_susyall_mChipm100GeV_dm0p16GeV_pu35*.root")
    inputfiles = glob("./EDM_output/edm_Run2016G*.root")


if 'Run201' in inputfiles[0] or 'Single' in inputfiles[0] : 
	dedxcalib_barrel = Dedxcalibdict_Muon_barrel['Run2016G']
	dedxcalib_endcap = Dedxcalibdict_Muon_endcap['Run2016G']
else: 
	dedxcalib_barrel = 1
	dedxcalib_endcap = 1

print 'barrel, endcap calibs', dedxcalib_barrel, dedxcalib_endcap


events = fwlite.Events(inputfiles)
#events = fwlite.Events("signal_with_sv.root")
primaryVertices = fwlite.Handle("std::vector<reco::Vertex>")
secondaryVertices = fwlite.Handle("std::vector<reco::VertexCompositeCandidate>")
secondaryVertices_Lambda = fwlite.Handle("std::vector<reco::VertexCompositeCandidate>")
primaryVertices = fwlite.Handle("std::vector<reco::Vertex>")
tracks_handle = fwlite.Handle("std::vector<reco::Track>")

dEdxTrackHandle = fwlite.Handle ("edm::ValueMap<reco::DeDxData>");
label_dEdXtrack = 'dedxPixelHarmonic2'
#label_dEdXtrack = 'dedxHarmonic2'

protonIndices_handle = fwlite.Handle("std::vector<int>")

tlegend = ROOT.TLegend(0.17, 0.77, 0.51, 0.88)
wantPlots = False
#KShort


fnew = ROOT.TFile(inputfiles[0].replace('edm','vertex'), 'recreate')

# Lambda
mass_histogram_Lambda = ROOT.TH1F("mass_Lambda", "reconstructed #Lambda^{0} invariant mass; invariant mass [GeV]; no. of reconstructed SV", 200, 1.08, 1.16) # invariant mass of all vertices
mass_goodCosAngle_Lambda = ROOT.TH1F("mass_goodCosAngle_Lambda", "mass_goodCosAngle_Lambda; invariant mass [GeV]; no. of reconstructed SV", 200, 1.08, 1.16) #Primary vertices improve physics results: momentum vector and the displacement vector must be parallel
radialDistance_Lambda= ROOT.TH1F("radialDistance_Lambda", "#Lambda^{0} vertex radial distance; radial distance [cm]; no. of reconstructed SV", 100,0.0, 20.0) 
mass_to0p5_Lambda = ROOT.TH1F("mass_to0p5_Lambda", "radial distance 0 - 0.5 cm;invariant mass [GeV];no. of reconstructed SV;", 200, 1.08, 1.16) 
mass_to1p5_Lambda = ROOT.TH1F("mass_to1p5_Lambda", "radial distance 0.5 - 1.5 cm;invariant mass [GeV];no. of reconstructed SV;", 200, 1.08, 1.16) 
massdedx_to1p5_Proton = ROOT.TH1F("massdedx_to1p5_Proton", "radial distance 0.5 - 1.5 cm;dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 
massdedxCalib_to1p5_Proton = ROOT.TH1F("massdedxCalib_to1p5_Proton", "radial distance 0.5 - 1.5 cm;dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 
massdedx_to1p5_Rando = ROOT.TH1F("massdedx_to1p5_Rando", "radial distance 0.5 - 1.5 cm;dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 

dedx_to1p5_Proton = ROOT.TH1F("dedx_to1p5_Proton", "radial distance 0.5 - 1.5 cm;dedx;", 200, 0, 10) 
dedxCalib_to1p5_Proton = ROOT.TH1F("dedxCalib_to1p5_Proton", "radial distance 0.5 - 1.5 cm;dedx;", 200, 0, 10) 

pt_to1p5_Proton = ROOT.TH1F("pt_to1p5_Proton", "radial distance 0.5 - 1.5 cm;dedx-derived mass [GeV];", 200, 0, 5) 
pt_to1p5_Rando = ROOT.TH1F("pt_to1p5_Rando", "radial distance 0.5 - 1.5 cm;dedx-derived mass [GeV];", 200, 0, 5) 

mass_to4p0_Lambda = ROOT.TH1F("mass_to4p0_Lambda", "radial distance 1.5 - 4.0 cm;invariant mass [GeV];no. of reconstructed SV;", 200,  1.08, 1.16) 
mass_to20p0_Lambda = ROOT.TH1F("mass_to20p0_Lambda", "radial distance 4.0 - 20.0 cm;invariant mass [GeV];no. of reconstructed SV;", 200,  1.08, 1.16)


hDeDxVsP_Proton = ROOT.TH2F("hDeDxVsP_Proton", "", 100, 0.0, 5, 100, 0.0, 11) 
hDeDxCalibVsP_Proton = ROOT.TH2F("hDeDxCalibVsP_Proton", "", 100, 0.0, 5, 100, 0.0, 11) 
hDeDxVsP_Rando = ROOT.TH2F("hDeDxVsP_Rando", "", 100, 0.0, 5, 100, 0.0, 11) 

n_bins = 100
range_min = 0.4
range_max = 0.6

mass_highPurity = ROOT.TH1F("mass_highPurity", "mass_highPurity", n_bins, range_min, range_max)



rho_z_histogram = ROOT.TH2F("rho_z", "rho_z", 100, 0.0, 30.0, 100, 0.0, 10.0) # horizontal axis will represent z, the direction parallel to the beamline, and the vertical axis will represent rho, the distance from the beamline
events.toBegin()
findMatch = 0
for i, event in enumerate(events):


    event.getByLabel("SecondaryVerticesFromHighPurityTracks", "Lambda", secondaryVertices_Lambda)
    event.getByLabel("offlinePrimaryVertices", primaryVertices)
    event.getByLabel("generalTracks", tracks_handle)
    event.getByLabel("SecondaryVerticesFromHighPurityTracks", "ProtonTrackIndices", protonIndices_handle)
    event.getByLabel(label_dEdXtrack, dEdxTrackHandle)

    if i > 9999999: break
    if i%1==0: print i, "   Secondary vertices per event:", secondaryVertices_Lambda.product().size()

    tracks = tracks_handle.product()
    dEdxTrack = dEdxTrackHandle.product()
    protonIndices = protonIndices_handle.product()



    event.getByLabel("SecondaryVerticesFromHighPurityTracks", "Kshort", secondaryVertices)
    for vertex in secondaryVertices.product():
        mass_highPurity.Fill(vertex.mass())	

    # Lambda loop		
    for j, secondary in enumerate(secondaryVertices_Lambda.product()):
        ## invariant mass of all vertices	
        mass_histogram_Lambda.Fill(secondary.mass())


        protonIdx = protonIndices[j]
        protrack = tracks[protonIdx]
        #if not protrack.charge()>0: continue
        
        pt, eta = protrack.pt(), protrack.eta()
        if abs(eta)<1.5: 
	    dedx = dEdxTrack.get(protonIdx).dEdx()
	    dedxCalib = dedxcalib_barrel*dEdxTrack.get(protonIdx).dEdx()
        else: 
	    dedx = dEdxTrack.get(protonIdx).dEdx()
	    dedxCalib = dedxcalib_endcap*dEdxTrack.get(protonIdx).dEdx()
        #massfromdedx = ROOT.TMath.Log10(ROOT.TMath.Sqrt((dedx-3.01)*pow(pt*ROOT.TMath.CosH(eta),2)/1.74))
        massfromdedx = ROOT.TMath.Sqrt((dedx-2.557)*pow(pt*ROOT.TMath.CosH(eta),2)/2.579)
        massfromdedxCalib = ROOT.TMath.Sqrt((dedxCalib-2.557)*pow(pt*ROOT.TMath.CosH(eta),2)/2.579)

        newj = protonIdx-1
        if newj<0: newj = protonIdx+1
        protrack2 = tracks[newj]
        pt2, eta2 = protrack2.pt(), protrack2.eta()
        dedx2 = 1.5*dEdxTrack.get(newj).dEdx()
        #massfromdedx = ROOT.TMath.Log10(ROOT.TMath.Sqrt((dedx-3.01)*pow(pt*ROOT.TMath.CosH(eta),2)/1.74))
        massfromdedx2 = ROOT.TMath.Sqrt((dedx2-2.557)*pow(pt2*ROOT.TMath.CosH(eta2),2)/2.579)        

        ##print 'proton', protrack.pt(), 'sv daughter 1', secondary.daughter(0).pt(), 'sv daughter 2', secondary.daughter(1).pt()
    # compute displacement vectors and compare them with KS momentum vectors
        px = secondary.px()
        py = secondary.py()
        pz = secondary.pz()
        p = secondary.p()
        bestCosAngle = -1 
        radDis = -1
        for primary in primaryVertices.product():
            dx = secondary.vx() - primary.x()
            dy = secondary.vy() - primary.y()
            dz = secondary.vz() - primary.z()
            dl = math.sqrt(dx**2 + dy**2 + dz**2)
            dxy = math.sqrt(dx**2 + dy**2)
            #if i % 100 == 0: print "Normalized momentum:", px/p, py/p, pz/p,
            #if i % 100 == 0: print "Normalized displacement:", dx/dl, dy/dl, dz/dl
            dotProduct = px*dx + py*dy + pz*dz
            cosAngle = dotProduct / p / dl
            if cosAngle > bestCosAngle:
                bestCosAngle = cosAngle # update it if you've found a better one
                radDis = dxy

        
        if bestCosAngle > 0.999994:
            mass_goodCosAngle_Lambda.Fill(secondary.mass())
            radialDistance_Lambda.Fill(radDis)
            if radDis <= 0.5:
                mass_to0p5_Lambda.Fill(secondary.mass())
            if (radDis <= 2.1) and (radDis > 0.2):
                mass_to1p5_Lambda.Fill(secondary.mass())
                if abs(secondary.mass()-1.11604e+00)<2.13880e-03:
                    hDeDxVsP_Proton.Fill(protrack.p(),dedx)
                    hDeDxCalibVsP_Proton.Fill(protrack.p(),dedxCalib)
                    hDeDxVsP_Rando.Fill(protrack2.p(),dedx2)
                    massdedx_to1p5_Proton.Fill(massfromdedx)
                    massdedxCalib_to1p5_Proton.Fill(massfromdedxCalib)
                    dedx_to1p5_Proton.Fill(dedx)
                    dedxCalib_to1p5_Proton.Fill(dedxCalib)
                    massdedx_to1p5_Rando.Fill(massfromdedx2)
                    pt_to1p5_Proton.Fill(pt)
                    pt_to1p5_Rando.Fill(pt2)                    
                
                    



            if (radDis <= 4.0)and (radDis > 1.5):
                mass_to4p0_Lambda.Fill(secondary.mass())
            if (radDis <= 20) and (radDis > 1.5):
                mass_to20p0_Lambda.Fill(secondary.mass())




fnew.cd()

# Lambda
hDeDxVsP_Proton.Write()
hDeDxCalibVsP_Proton.Write()
hDeDxVsP_Rando.Write()
mass_histogram_Lambda.Write()
mass_goodCosAngle_Lambda.Write()
radialDistance_Lambda.Write()
mass_to0p5_Lambda.Write()
mass_to1p5_Lambda.Write()
massdedx_to1p5_Proton.Write()
massdedxCalib_to1p5_Proton.Write()
dedx_to1p5_Proton.Write()
dedxCalib_to1p5_Proton.Write()
pt_to1p5_Proton.Write()
pt_to1p5_Rando.Write()
massdedx_to1p5_Rando.Write()
mass_to4p0_Lambda.Write()
mass_to20p0_Lambda.Write()



mass_highPurity.Write()
rho_z_histogram.Write()

print 'just created', fnew.GetName()
fnew.Close()
