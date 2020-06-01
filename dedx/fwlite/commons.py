#! /usr/bin/env python


"""Methods used by other scripts.
"""


import sys
from glob import glob
from array import array
from math import ceil, cosh
import numpy as np
import scipy.optimize

from ROOT import gROOT, gSystem, FWLiteEnabler, TFile, TH1F, TMath, TLorentzVector, TH2F, TTree

gROOT.SetBatch()        # don't pop up canvases
gROOT.SetStyle('Plain') # white background

gSystem.Load("libFWCoreFWLite.so")
gSystem.Load("libDataFormatsFWLite.so")
FWLiteEnabler.enable()

from DataFormats.FWLite import Events, Handle


"""Angle between two angles, returns value between -pi and +pi.
"""
def angleBetween(phi1, phi2):

	phi = TMath.ATan2(TMath.Sin(phi1) + TMath.Sin(phi2), TMath.Cos(phi1) + TMath.Cos(phi2))
	
	while phi >= TMath.Pi(): phi -= 2 * TMath.Pi()
	while phi < -TMath.Pi(): phi += 2 * TMath.Pi()
	
	return phi


"""Adds two angles, returns value between -pi and +pi.
"""
def addPhi(phi1, phi2):
	
	sumphi = phi1 + phi2
	
	while sumphi >= TMath.Pi(): sumphi -= 2 * TMath.Pi()
	while sumphi < -TMath.Pi(): sumphi += 2 * TMath.Pi()
	
	return sumphi


"""Subtracts two angles, returns value between -pi and +pi.
"""
def deltaPhi(phi1, phi2):
	
	dphi = phi1 - phi2
	
	while dphi >= TMath.Pi(): dphi -= 2 * TMath.Pi()
	while dphi < -TMath.Pi(): dphi += 2 * TMath.Pi()
	
	return dphi


"""Returns deltaR.
"""
def deltaR(eta1, eta2, phi1, phi2):

	deta = eta1 - eta2
	dphi = deltaPhi(phi1, phi2)
	
	return TMath.Sqrt(deta * deta + dphi * dphi)
	

"""Calculates isolation-variables for a track inside jets.
"""
def calcIso_jet(one, many, pv_pos, isTight):

	pt_threshold = 10
	conesize = 0.5
	
	if isTight:
		pt_threshold = 30
		conesize = 0.5
	
	ptsum = 0
	num = 0
	
	dRmin = 10
	for m in many:
		
		if not passesPreselection_iso_jet(m, pt_threshold): continue
		
		dR = deltaR(one.eta(), m.eta(), one.phi(), m.phi())
		
		if dR < dRmin and dR > 0.001:
			dRmin = dR
			
		if dR < conesize:
			ptsum += m.pt()
			num += 1
			
	return ptsum/one.pt(), dRmin, num


"""Calculates isolation-variables for a PF inside PFs.
"""
def calcIso_pf(one, many, pv_pos, isTight):

	pt_threshold = 0
	conesize = 0.3
	
	if isTight:
		pt_threshold = 0.3
		conesize = 0.1
	
	ptsum = -one.pt()
	num = -1
	
	if not passesPreselection_iso_pfc(one, pv_pos, pt_threshold):
		ptsum = 0
		num = 0
	
	dRmin = 999
	for m in many:
		
		if not passesPreselection_iso_pfc(m, pv_pos, pt_threshold): continue

		dR = deltaR(one.eta(), m.eta(), one.phi(), m.phi())
		
		if dR < dRmin and dR > 0.001:
			dRmin = dR
			
		if dR < conesize:
			ptsum += m.pt()
			num += 1
			
	return ptsum/one.pt(), dRmin, num


"""Calculates isolation-variables for a track inside tracks.
"""
def calcIso_track(one, many, pv_pos, isTight):
	
	dz_threshold = 1
	dxy_threshold = 1
	pt_threshold = 0
	conesize = 0.3
	
	if isTight:
		dz_threshold = 0.15
		dxy_threshold = 0.15
		pt_threshold = 1
		conesize = 0.3
	
	ptsum = -one.pt()
	num = -1
	
	if not passesPreselection_iso_track(one, pv_pos, dz_threshold, dxy_threshold, pt_threshold):			
		ptsum = 0
		num = 0

	dRmin = 10	
	for m in many:
		
		if not passesPreselection_iso_track(m, pv_pos, dz_threshold, dxy_threshold, pt_threshold): continue
		
		dR = deltaR(one.eta(), m.eta(), one.phi(), m.phi())
		
		if dR < dRmin and dR > 0.001:
			dRmin = dR
			
		if dR < conesize:
			ptsum += m.pt()
			num += 1
			
	return ptsum/one.pt(), dRmin, num


"""Calculates isolation-variables for a gen-particle inside tracks.
"""
def calcIso_gen(one, many, pv_pos, isTight):
	
	dz_threshold = 1
	dxy_threshold = 1
	pt_threshold = 0
	conesize = 0.3
	
	if isTight:
		dz_threshold = 0.15
		dxy_threshold = 0.15
		pt_threshold = 1
		conesize = 0.3
	
	oneTlv = TLorentzVector()
	oneTlv.SetPxPyPzE(one.px(), one.py(), one.pz(), one.energy())

	ptsum = 0
	num = 0
	
	dRmin = 999
	for m in many:
		
		if not passesPreselection_iso_track(m, pv_pos, dz_threshold, dxy_threshold, pt_threshold): continue
		
		dR = deltaR(one.eta(), m.eta(), one.phi(), m.phi())
		
		if dR < dRmin and dR > 0.001:
			dRmin = dR
			
		if dR < conesize:
			ptsum += m.pt()
			num += 1
			
	return ptsum/one.pt(), dRmin, num


"""Returns last copy of a gen. particle.
"""
def getLastCopy(gp):
		
	i = 0
	while not gp.status() == 1:
		for idx in range(gp.numberOfDaughters()):
			if gp.pdgId() == gp.daughter(idx).pdgId():
				gp = gp.daughter(idx)
				break
		i += 1
		if i > 100: return None
		
	return gp


"""Returns lepton and neutrino from chi1pm decay to chi10.
"""
def findLeptonNeutrino(gp):
		
	leptonDaughterFound = False
	neutrinoDaughterFound = False
	
	lepton = None
	neutrino = None
	
	for i in range(gp.numberOfDaughters()):
		
		pdgIdDaughter = abs(gp.daughter(i).pdgId())
			
		if pdgIdDaughter == 11 or pdgIdDaughter == 13:
			
			leptonDaughterFound = True
			lepton = gp.daughter(i)
			
		if pdgIdDaughter == 12 or pdgIdDaughter == 14:
			
			neutrinoDaughterFound = True
			neutrino = gp.daughter(i)
			
		if leptonDaughterFound and neutrinoDaughterFound: break
		
	if not (leptonDaughterFound and neutrinoDaughterFound): return None, None
	if not abs(lepton.pdgId()) + 1 == abs(neutrino.pdgId()): return None, None
	if not lepton.charge() * gp.charge() > 0: return None, None
	
	lepton = getLastCopy(lepton)
	neutrino = getLastCopy(neutrino)
	
	return lepton, neutrino
	
	
"""Returns pion from chi1pm decay to chi10.
"""
def findPion(gp):
	
	pionDaughterFound = False
	
	pion = None
	
	for i in range(gp.numberOfDaughters()):
		
		pdgIdDaughter = abs(gp.daughter(i).pdgId())
		
		if pdgIdDaughter == 211:
			
			pionDaughterFound = True
			pion = gp.daughter(i)
			
		if pionDaughterFound: break
		
	if not pionDaughterFound: return None
	if not pion.charge() * gp.charge() > 0: return None
	
	pion = getLastCopy(pion)
				
	return pion	
	

"""Returns lepton pair from chi20 decay to chi10.
"""
def findLeptons(gp):
	
	oneleptonDaughterFound = False
	
	twoleptonDaughtersFound = False
	
	lepton1 = None
	lepton2 = None
	
	for i in range(gp.numberOfDaughters()):
		
		pdgIdDaughter = abs(gp.daughter(i).pdgId())
			
		if pdgIdDaughter == 11 or pdgIdDaughter == 13:
			
			if oneleptonDaughterFound:
				twoleptonDaughtersFound = True
				lepton2 = gp.daughter(i)
			else:
				oneleptonDaughterFound = True
				lepton1 = gp.daughter(i)
				
		if twoleptonDaughtersFound: break

	if not twoleptonDaughtersFound: return None, None
	
	if not abs(lepton1.pdgId()) == abs(lepton2.pdgId()): return None, None
	
	if not lepton1.charge() * lepton2.charge() < 0: return None, None
	
	lepton1 = getLastCopy(lepton1)
	
	lepton2 = getLastCopy(lepton2)
	
	return lepton1, lepton2
	
"""Returns invariant mass from the TLorentzVectors of a pair of electrons
"""
def invariantMass(electron1, electron2):

	electronTlv1 = TLorentzVector()
	
	electronTlv2 = TLorentzVector()
	
	electronTlv1.SetPxPyPzE(electron1.px(), electron1.py(), electron1.pz(), electron1.energy())	
	
	electronTlv2.SetPxPyPzE(electron2.px(), electron2.py(), electron2.pz(), electron2.energy())	

	invMass = (electronTlv1+electronTlv2).M()
	
	return invMass
"""Returns invariant mass from the TLorentzVectors of a pair of tracks
"""
def invariantMassTracks(track1, track2):

	trkTlv1 = TLorentzVector()
	
	trkTlv2 = TLorentzVector()
	
	#trkTlv1.SetPxPyPzE(track1.px(), track1.py(), track1.pz(), track1.pt()*np.cosh(track1.eta()))	
	
	#trkTlv2.SetPxPyPzE(track2.px(), track2.py(), track2.pz(), track2.pt()*np.cosh(track2.eta()))
	trkTlv1.SetPtEtaPhiM(track1.pt(), track1.eta(), track1.phi(), 0.13957018)
		
	trkTlv2.SetPtEtaPhiM(track2.pt(), track2.eta(), track2.phi(), 0.13957018)		
	
	invMass = (trkTlv1 +trkTlv2).M()
	
	return invMass
	
"""Returns invariant mass from the TLorentzVectors of a pair of tracks assuming pion mass
"""
def invariantMassTracksAsPions(track1, track2):

	trkTlv1 = TLorentzVector()
	
	trkTlv2 = TLorentzVector()
	
	trkTlv1.SetPtEtaPhiM(track1.pt(), track1.eta(), track1.phi(), 0.13957018)
		
	trkTlv2.SetPtEtaPhiM(track2.pt(), track2.eta(), track2.phi(), 0.13957018)	
	
	invMass = (trkTlv1 +trkTlv2).M()
	
	return invMass

	
"""Defines basic preselection for PFs.
"""
def passesPreselection_basic_pfc(pfc):
	
	if pfc.trackRef().isNull(): return False
	
	if not passesPreselection_basic_track(pfc.trackRef().get()): return False
	
	return True


"""Defines preselection used for calculation of isolation-variables for PFs.
"""
def passesPreselection_iso_pfc(pfc, pv_pos, pt_threshold):
	
	if pfc.trackRef().isNull(): return False
	
	if pfc.trackRef().get().numberOfValidHits() == 0: return False
	
	if pfc.trackRef().get().ndof() == 0: return False
	
	if pfc.trackRef().get().charge() == 0: return False
	
	if abs(pfc.trackRef().get().dz(pv_pos)) > 1: return False
	
	if pfc.pt() <= pt_threshold: return False
	
	return True


"""Defines preselection used for BDT for PFs.
"""
def passesPreselection_final_pfc(pfc, pv_pos):

	if not passesPreselection_basic_pfc(pfc): return False
	
	if pfc.pt() <= 0.7: return False
	
	return True


"""Defines basic preselection for tracks.
"""
def passesPreselection_basic_track(track):
	
	if track.numberOfValidHits() == 0: return False
	
	if track.ndof() == 0: return False
	
	if track.charge() == 0: return False
	
	if track.pt() > 5: return False
	
	return True


"""Defines preselection used for calculation of isolation-variables for tracks.
"""
def passesPreselection_iso_track(track, pv_pos, dz_threshold, dxy_threshold, pt_threshold):
		
	if track.numberOfValidHits() == 0: return False
	
	if track.ndof() == 0: return False
	
	if track.charge() == 0: return False
	
	if abs(track.dz(pv_pos)) >= dz_threshold: return False
	
	if abs(track.dxy(pv_pos)) >= dxy_threshold: return False
	
	if track.pt() <= pt_threshold: return False
			
	return True


"""Defines preselection used for BDT for tracks.
"""
def passesPreselection_final_track(track, pv_pos):
	
	if not passesPreselection_basic_track(track): return False
	
	return True


"""Defines preselection used for calculation of isolation-variables for jets.
"""
def passesPreselection_iso_jet(jet, pt_threshold):
	
	if jet.pt() <= pt_threshold: return False

	return True


"""Finds matching track for lepton via dxyz.
"""
def findMatch_track_new(lepton, tracks):
	
	dxyzmin = 10
	tmin = 10
	drmin = 10
	idx = -1
	
	if lepton.pt() > 0:
	
		for itrack, track in enumerate(tracks):
			
			if not passesPreselection_basic_track(track): continue
			
			if not track.charge() * lepton.charge() > 0: continue
			
			if not abs(track.pt() - lepton.pt()) / lepton.pt() < 0.2: continue
					
			if not abs(track.eta() - lepton.eta()) < 0.1: continue
			
			if not abs(deltaPhi(track.phi(), lepton.phi())) < 1.57: continue
			
			res = scipy.optimize.minimize(distance, x0=0.0, bounds=((-1.57, 1.57),), args=(track, lepton.vertex()))  # other minimization method?
			
			dxyz = distance(res.x, track, lepton.vertex())
			
			if dxyz < dxyzmin:
					
				dxyzmin = dxyz
				tmin = res.x[0]
				drmin = deltaR(lepton.eta(), track.eta(), lepton.phi(), addPhi(track.phi(), res.x[0]))
				idx = itrack
				
	return idx, dxyzmin, tmin, drmin

"""Finds matching track for track via dxyz.
"""
def findMatch_tracktrack_new(aTrack, tracks):
	
	dxyzmin = 10
	tmin = 10
	drmin = 10
	idx = -1
	
	if aTrack.pt() > 0:
	
		for itrack, track in enumerate(tracks):
			
			if not passesPreselection_basic_track(track): continue
			
			if not track.charge() * aTrack.charge() > 0: continue
			
			if not abs(track.pt() - aTrack.pt()) / aTrack.pt() < 0.2: continue
					
			if not abs(track.eta() - aTrack.eta()) < 0.1: continue
			
			if not abs(deltaPhi(track.phi(), aTrack.phi())) < 1.57: continue
			
			res = scipy.optimize.minimize(distance, x0=0.0, bounds=((-1.57, 1.57),), args=(track, aTrack.vertex()))  # other minimization method?
			
			dxyz = distance(res.x, track, aTrack.vertex())
			
			if dxyz < dxyzmin:
					
				dxyzmin = dxyz
				tmin = res.x[0]
				drmin = deltaR(aTrack.eta(), track.eta(), aTrack.phi(), addPhi(track.phi(), res.x[0]))
				idx = itrack
				
	return idx, dxyzmin, tmin, drmin
	
"""Finds matching track for lepton via delta R.
"""
def findMinDr(lepton, tracks, threshold):
	
	drmin = 10
	idx = -1
	matchingTrack = None
	match = False
	
	if lepton.pt() > 0:
	
		for itrack, track in enumerate(tracks):
			
			if not passesPreselection_basic_track(track): continue
			
			if not track.charge() * lepton.charge() > 0: continue
			
			if not abs(track.pt() - lepton.pt()) / lepton.pt() < 0.2: continue
					
			if not abs(track.eta() - lepton.eta()) < 0.1: continue
			
			if not abs(deltaPhi(track.phi(), lepton.phi())) < 1.57: continue
			
			leptonTlv = TLorentzVector()
			leptonTlv.SetPxPyPzE(lepton.px(),lepton.py(),lepton.pz(),lepton.energy())	
			trkTlv = TLorentzVector()
			trkTlv.SetPxPyPzE(track.px(), track.py(), track.pz(), track.pt()*np.cosh(track.eta()))
			
			dr = trkTlv.DeltaR(leptonTlv)
			
			if dr < drmin:
					
				drmin = dr
				idx = itrack
				matchingTrack = track
				

	if drmin < threshold: match = True
	return match, idx, drmin, matchingTrack
	
"""Finds matching track for lepton via delta R.
"""
def findMinDr_track(aTrack, tracks, threshold):
	
	drmin = 10
	idx = -1
	matchingTrack = None
	match = False
	
	if aTrack.pt() > 0:
	
		for itrack, track in enumerate(tracks):
			
			if not passesPreselection_basic_track(track): continue
			
			if not track.charge() * aTrack.charge() > 0: continue
			
			if not abs(track.pt() - aTrack.pt()) / aTrack.pt() < 0.2: continue
					
			if not abs(track.eta() - aTrack.eta()) < 0.1: continue
			
			if not abs(deltaPhi(track.phi(), aTrack.phi())) < 1.57: continue
			
			aTrackTlv = TLorentzVector()
			aTrackTlv.SetPxPyPzE(aTrack.px(),aTrack.py(),aTrack.pz(),aTrack.pt()*np.cosh(aTrack.eta()))	
			trkTlv = TLorentzVector()
			trkTlv.SetPxPyPzE(track.px(), track.py(), track.pz(), track.pt()*np.cosh(track.eta()))
			
			dr = trkTlv.DeltaR(aTrackTlv)
			
			if dr < drmin:
					
				drmin = dr
				idx = itrack
				matchingTrack = track
				

	if drmin < threshold: match = True
	return match, idx, drmin, matchingTrack


"""Finds matching track for lepton via dxyz, random with opposite charge.
"""
def findMatch_track_new_random(lepton, tracks):
	
	dxyzmin = 10
	tmin = 10
	drmin = 10
	idx = -1
	
	if lepton.pt() > 0:
	
		for itrack, track in enumerate(tracks):
			
			if not passesPreselection_basic_track(track): continue
			
			if not track.charge() * lepton.charge() < 0: continue
			
			if not abs(track.pt() - lepton.pt()) / lepton.pt() < 0.2: continue
			
			if not abs(track.eta() - lepton.eta()) < 0.1: continue
			
			if not abs(deltaPhi(track.phi(), lepton.phi())) < 1.57: continue
			
			res = scipy.optimize.minimize(distance, x0=0.0, bounds=((-1.57, 1.57),), args=(track, lepton.vertex()))  # other minimization method?
			
			dxyz = distance(res.x, track, lepton.vertex())
			
			if dxyz < dxyzmin:
				
				dxyzmin = dxyz
				tmin = res.x[0]
				drmin = deltaR(lepton.eta(), track.eta(), lepton.phi(), addPhi(track.phi(), res.x[0]))
				idx = itrack
			
	return idx, dxyzmin, tmin, drmin


"""Finds matching pfc for lepton via deltaEta and taking distance in 3D into account.
"""
def findMatch_pfc_new(lepton, pfcands):
	
	dxyzmin = 10
	tmin = 10
	drmin = 10
	idx = -1
	
	if lepton.pt() > 0:
		
		for ipfc, pfc in enumerate(pfcands):
			
			if not passesPreselection_basic_pfc(pfc): continue
			
			if not pfc.charge() * lepton.charge() > 0: continue
			
			if not abs(pfc.pt() - lepton.pt()) / lepton.pt() < 0.2: continue
			
			if not abs(pfc.eta() - lepton.eta()) < 0.1: continue
			
			if not abs(deltaPhi(pfc.phi(), lepton.phi())) < 1.57: continue
			
			res = scipy.optimize.minimize(distance, x0=0.0, bounds=((-1.57, 1.57),), args=(pfc.trackRef().get(), lepton.vertex()))  # other minimization method?
			
			dxyz = distance(res.x, pfc.trackRef().get(), lepton.vertex())
			
			if dxyz < dxyzmin:
				
				dxyzmin = dxyz
				tmin = res.x[0]
				drmin = deltaR(lepton.eta(), pfc.eta(), lepton.phi(), addPhi(pfc.phi(), res.x[0]))
				idx = ipfc
				
	return idx, dxyzmin, tmin, drmin

"""Calculates the pointing angle betweenn the line from PV to SV and the vectoriel combined momentum of a track pair coming from the SV.
"""
def pointingAngle(track1, track2, pv_pos, sv_pos):
	
	trk1Tlv = TLorentzVector()
	trk1Tlv.SetPxPyPzE(track1.px(),track1.py(),track1.pz(),track1.pt()*np.cosh(track1.eta()))
	trk2Tlv = TLorentzVector()
	trk2Tlv.SetPxPyPzE(track2.px(),track2.py(),track2.pz(),track2.pt()*np.cosh(track2.eta()))	
	combinedMomentum =trk2Tlv-trk1Tlv
	
	PVtoSV = [sv_pos[0]-pv_pos.x(),sv_pos[1]-pv_pos.y(),sv_pos[2]-pv_pos.z()]
	
	pointingAngle=np.arctan2(PVtoSV[0] -combinedMomentum.X(),  PVtoSV[1]-combinedMomentum.Y())
	
	return pointingAngle
	

"""Finds a common vertex for two tracks if the minimin distance is smaller than 0.1 cm and returns the vertex' distance to the PV.
"""
def vertexFinder(track1, track2, pv_pos):
	
	mindist, tmin1, tmin2, p1, p2 = minDistanceTrackTrack(track1, track2)
	
	vertex = np.array([0, 0, 0])
	angletoorigin = -10
	angletopv = -10
	disttopv3D = -1
	disttopvXY = -1
	disttopvZ = -1
	if mindist < 0.2:
		
		vertex = (p1 + p2) / 2
		
		disttopv3D = np.linalg.norm(vertex - np.array([pv_pos.x(), pv_pos.y(), pv_pos.z()]))
		disttopvXY = np.linalg.norm(vertex[:2] - np.array([pv_pos.x(), pv_pos.y()]))
		disttopvZ = np.linalg.norm(vertex[2:] - np.array([pv_pos.z()]))
		
		angletoorigin = np.arctan2(vertex[1], vertex[0])
		angletopv = np.arctan2(vertex[1] - pv_pos.y(), vertex[0] - pv_pos.x())
	
	return mindist, tmin1, tmin2, vertex[0], vertex[1], vertex[2], angletoorigin, angletopv, disttopv3D, disttopvXY, disttopvZ


"""Gives minimum distance between two tracks and the corresponding points of closest approach on each track.
"""
def minDistanceTrackTrack(track1, track2):
	
	res = scipy.optimize.minimize(distanceTrackTrack, x0=[0.0, 0.0], bounds=((-1.57, 1.57), (-1.57, 1.57)), args=(track1, track2))
	
	tmin1 = res.x[0]
	tmin2 = res.x[1]
	
	d, p1, p2 = getDistanceAndPoints(res.x, track1, track2)
	
	return d, tmin1, tmin2, p1, p2


"""Distance between a specific point along a track (given by t1) and a specific point along another track (given by t2). 
Additionally returns the points.
"""
def getDistanceAndPoints(tarray, track1, track2):
	
	t1 = np.array([tarray[0]])
	t2 = np.array([tarray[1]])
	
	p1 = helix(t1, track1.phi(), track1.eta(), track1.charge(), track1.pt(), track1.vx(), track1.vy(), track1.vz())
	p2 = helix(t2, track2.phi(), track2.eta(), track2.charge(), track2.pt(), track2.vx(), track2.vy(), track2.vz())
	
	d = np.linalg.norm(p1 - p2)
	
	return d, p1, p2


"""Distance between a specific point along a track (given by t1) and a specific point along another track (given by t2).
"""
def distanceTrackTrack(tarray, track1, track2):
	
	t1 = np.array([tarray[0]])
	t2 = np.array([tarray[1]])
	
	d = np.linalg.norm(helix(t1, track1.phi(), track1.eta(), track1.charge(), track1.pt(), track1.vx(), track1.vy(), track1.vz())
					 - helix(t2, track2.phi(), track2.eta(), track2.charge(), track2.pt(), track2.vx(), track2.vy(), track2.vz()))
	
	return d


"""Helix parametrization in 3D.
"""
def helix(t, phi, eta, q, pt, vx, vy, vz):
	
	r = 87.78  # radius [cm] for particle with pT=1GeV in B=3.8T
	
	x = vx + r * q * pt * (np.sin(phi) - np.sin(phi + t))
	
	y = vy + r * q * pt * (-np.cos(phi) + np.cos(phi + t))
	
	z = vz - t * r * q * pt / np.tan(2 * np.arctan(np.exp(-eta)))
	
	return np.array([x[0], y[0], z[0]])


"""Distance between a specific point along a track (given by t) and a vertex in 3D.
"""
def distance(t, track, vertex):
	
	d = np.linalg.norm(helix(t, track.phi(), track.eta(), track.charge(), track.pt(), track.vx(), track.vy(), track.vz())
                    - np.array([vertex.x(), vertex.y(), vertex.z()]))
	
	return d


"""Distance between a specific point along a track (given by t) and a vertex in XY.
"""
def distanceXY(t, track, vertex):
	
	d = np.linalg.norm(helix(t, track.phi(), track.eta(), track.charge(), track.pt(), track.vx(), track.vy(), track.vz())[:2]
                    - np.array([vertex.x(), vertex.y()]))
	
	return d


"""Distance between a specific point along a track (given by t) and a vertex in Z.
"""
def distanceZ(t, track, vertex):
	
	d = np.linalg.norm(helix(t, track.phi(), track.eta(), track.charge(), track.pt(), track.vx(), track.vy(), track.vz())[2:]
                    - np.array([vertex.z()]))
	
	return d


"""Impact parameters in XY and Z at PCA to PV in 3D (calculated with helix extrapolation).
"""
def handmadeDxyDz(track, pv_pos):
	
	res = scipy.optimize.minimize(distance, x0=0.0, bounds=((-1.57, 1.57),), args=(track, pv_pos))
	
	dxy = distanceXY(res.x, track, pv_pos)
	dz = distanceZ(res.x, track, pv_pos)
	
	return dxy, dz


"""Impact parameters in XY and Z at PCA to PV in XY (calculated with helix extrapolation).
"""
def handmadeDxyDzTransversePCA(track, pv_pos):
	
	res = scipy.optimize.minimize(distanceXY, x0=0.0, bounds=((-1.57, 1.57),), args=(track, pv_pos))
	
	dxy = distanceXY(res.x, track, pv_pos)
	dz = distanceZ(res.x, track, pv_pos)
	
	return dxy, dz

	
"""dPhi between MET and vector from PV to PCA to PV of a track
"""
def handmadeDphiMetPCA(track, pv_pos, met):
	
	#gives the helix parameter value for which the distance is minimal
	res = scipy.optimize.minimize(distance, x0=0.0, bounds=((-1.57, 1.57),), args=(track, pv_pos))
	
	#insert found helix parameter and track parameters to get PCA
	pca = helix(res.x, track.phi(), track.eta(), track.charge(), track.pt(), track.vx(), track.vy(), track.vz())
	
	#compute phi angle of vector from PV to PCA
	phipca = np.arctan2(pca[1] - pv_pos.y(), pca[0] - pv_pos.x())
	
	#compute dPhi
	dphi = deltaPhi(phipca, met.phi())
	
	return dphi, phipca, res.x[0]
	

"""Finds matching track for lepton via dR.
"""
def findMatch_track_old(lepton, tracks):
	
	drmin = 10
	idx = -1
	
	if lepton.pt() > 0:
		
		leptonTlv = TLorentzVector()
		leptonTlv.SetPxPyPzE(lepton.px(), lepton.py(), lepton.pz(), lepton.energy())
	
		for itrack, track in enumerate(tracks):
			
			if track.numberOfValidHits() == 0: continue
			if track.ndof() == 0: continue
			if track.charge() == 0: continue
		
#			if not passesPreselection_basic_track(track): continue
			
			if not track.charge() * lepton.charge() > 0: continue
			
#			if not abs(track.pt() - lepton.pt()) / lepton.pt() < 0.2: continue
					
			trackTlv = TLorentzVector()
			trackTlv.SetPxPyPzE(track.px(), track.py(), track.pz(), track.pt()*TMath.CosH(track.eta()))
			
			dr = trackTlv.DeltaR(leptonTlv)
			
			if dr < drmin:
				
				drmin = dr
				idx = itrack
				
	return idx, drmin


"""Finds matching track for lepton via dR, random with opposite charge.
"""
def findMatch_track_old_random(lepton, tracks):
	
	drmin = 10
	idx = -1
	
	if lepton.pt() > 0:
		
		leptonTlv = TLorentzVector()
		leptonTlv.SetPxPyPzE(lepton.px(), lepton.py(), lepton.pz(), lepton.energy())
	
		for itrack, track in enumerate(tracks):
						
			if track.numberOfValidHits() == 0: continue
			if track.ndof() == 0: continue
			if track.charge() == 0: continue
			
#			if not passesPreselection_basic_track(track): continue
			
			if not track.charge() * lepton.charge() < 0: continue
			
#			if not abs(track.pt() - lepton.pt()) / lepton.pt() < 0.2: continue
					
			trackTlv = TLorentzVector()
			trackTlv.SetPxPyPzE(track.px(), track.py(), track.pz(), track.pt()*TMath.CosH(track.eta()))
			
			dr = trackTlv.DeltaR(leptonTlv)
			
			if dr < drmin:
				
				drmin = dr
				idx = itrack
				
	return idx, drmin


"""Finds matching pfc for lepton via deltaR.
"""
def findMatch_pfc_old(lepton, pfcands):
	
	drmin = 10
	idx = -1
	
	if lepton.pt() > 0:
		
		leptonTlv = TLorentzVector()
		leptonTlv.SetPxPyPzE(lepton.px(), lepton.py(), lepton.pz(), lepton.energy())
		
		for ipfc, pfc in enumerate(pfcands):
			
			if pfc.trackRef().isNull(): continue
			if pfc.trackRef().get().numberOfValidHits() == 0: continue
			if pfc.trackRef().get().ndof() == 0: continue
			if pfc.trackRef().get().charge() == 0: continue
			
#			if not passesPreselection_basic_pfc(pfc): continue
			
			if not pfc.charge() * lepton.charge() > 0: continue
			
#			if not abs(pfc.pt() - lepton.pt()) / lepton.pt() < 0.2: continue
			
			pfcTlv = TLorentzVector()
			pfcTlv.SetPxPyPzE(pfc.px(), pfc.py(), pfc.pz(), pfc.energy())
			
			dr = pfcTlv.DeltaR(leptonTlv)
			
			if dr < drmin:
				
				drmin = dr
				idx = ipfc
				
	return idx, drmin


"""Finds matching jet for lepton via deltaR.
"""
def findMatch_jet_old(lepton, jets):
	
	drmin = 10
	idx = -1
		
	for ijet, jet in enumerate(jets):
		
		dr = deltaR(lepton.eta(), jet.eta(), lepton.phi(), jet.phi())
		
		if dr < drmin:
			
			drmin = dr
			idx = ijet
				
	return idx, drmin
