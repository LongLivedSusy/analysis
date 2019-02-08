#!/bin/env python
import sys, os

commands = []

cmd = 'python SkimAnalysisBins_work.py --fout=skim_g1800_chi1400_27_200970_step4_100.root'
os.system(cmd)

cmd = 'python SkimAnalysisBins_work.py --fout=skim_g1800_chi1400_27_200970_step4_100_jesUp.root --dojetsyst --nsigmajes 1'
os.system(cmd)

cmd = 'python SkimAnalysisBins_work.py --fout=skim_g1800_chi1400_27_200970_step4_100_jesDown.root --dojetsyst --nsigmajes -1'
os.system(cmd)

cmd = 'python SkimAnalysisBins_work.py --fout=skim_g1800_chi1400_27_200970_step4_100_jerUp.root --dojetsyst --applysmearing --nsigmajer 1'
os.system(cmd)

cmd = 'python SkimAnalysisBins_work.py --fout=skim_g1800_chi1400_27_200970_step4_100_jerDown.root --dojetsyst --applysmearing --nsigmajer -1'
os.system(cmd)

cmd = 'python SkimAnalysisBins_work.py --fout=skim_g1800_chi1400_27_200970_step4_100_btagUp.root --dobtagsf --nsigmabtagsf 1'
os.system(cmd)

cmd = 'python SkimAnalysisBins_work.py --fout=skim_g1800_chi1400_27_200970_step4_100_btagDown.root --dobtagsf --nsigmabtagsf -1'
os.system(cmd)

