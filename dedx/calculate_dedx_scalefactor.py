#!/bin/env/python

if __name__=='__main__' :
    print 'Calculating dE/dx intercalibration scale factor'
    
    gausmean_barrel={}
    gausmean_endcap={}
    scalefactor_barrel={}
    scalefactor_endcap={}
   
    # Barrel
    gausmean_barrel['Summer16'] = 2.866
    gausmean_barrel['Fall17'] = 2.958
    
    gausmean_barrel['Run2016B'] = 2.434
    gausmean_barrel['Run2016C'] = 2.365
    gausmean_barrel['Run2016D'] = 2.312
    gausmean_barrel['Run2016E'] = 2.217
    gausmean_barrel['Run2016F'] = 2.185
    gausmean_barrel['Run2016G'] = 2.083
    gausmean_barrel['Run2016H'] = 2.097
    
    gausmean_barrel['Run2017B'] = 2.961
    gausmean_barrel['Run2017C'] = 2.379
    gausmean_barrel['Run2017D'] = 2.386
    gausmean_barrel['Run2017E'] = 2.725
    gausmean_barrel['Run2017F'] = 2.515
    
    gausmean_barrel['Run2018A'] = 2.502
    gausmean_barrel['Run2018B'] = 2.412
    gausmean_barrel['Run2018C'] = 2.384
    gausmean_barrel['Run2018D'] = 2.314
    
    # Endcap 
    gausmean_endcap['Summer16'] = 2.866
    gausmean_endcap['Fall17'] = 3.01
    
    gausmean_endcap['Run2016B'] = 2.413
    gausmean_endcap['Run2016C'] = 2.396
    gausmean_endcap['Run2016D'] = 2.387
    gausmean_endcap['Run2016E'] = 2.332
    gausmean_endcap['Run2016F'] = 2.248
    gausmean_endcap['Run2016G'] = 2.197
    gausmean_endcap['Run2016H'] = 2.196
    
    gausmean_endcap['Run2017B'] = 2.705
    gausmean_endcap['Run2017C'] = 2.413
    gausmean_endcap['Run2017D'] = 2.362
    gausmean_endcap['Run2017E'] = 2.374
    gausmean_endcap['Run2017F'] = 2.199
    
    gausmean_endcap['Run2018A'] = 2.333
    gausmean_endcap['Run2018B'] = 2.249
    gausmean_endcap['Run2018C'] = 2.206
    gausmean_endcap['Run2018D'] = 2.256
   
    # Barrel scale factor
    scalefactor_barrel['Run2016B']=gausmean_barrel['Summer16']/gausmean_barrel['Run2016B']
    scalefactor_barrel['Run2016C']=gausmean_barrel['Summer16']/gausmean_barrel['Run2016C']
    scalefactor_barrel['Run2016D']=gausmean_barrel['Summer16']/gausmean_barrel['Run2016D']
    scalefactor_barrel['Run2016E']=gausmean_barrel['Summer16']/gausmean_barrel['Run2016E']
    scalefactor_barrel['Run2016F']=gausmean_barrel['Summer16']/gausmean_barrel['Run2016F']
    scalefactor_barrel['Run2016G']=gausmean_barrel['Summer16']/gausmean_barrel['Run2016G']
    scalefactor_barrel['Run2016H']=gausmean_barrel['Summer16']/gausmean_barrel['Run2016H']

    scalefactor_barrel['Run2017B']=gausmean_barrel['Summer16']/gausmean_barrel['Run2017B']
    scalefactor_barrel['Run2017C']=gausmean_barrel['Summer16']/gausmean_barrel['Run2017C']
    scalefactor_barrel['Run2017D']=gausmean_barrel['Summer16']/gausmean_barrel['Run2017D']
    scalefactor_barrel['Run2017E']=gausmean_barrel['Summer16']/gausmean_barrel['Run2017E']
    scalefactor_barrel['Run2017F']=gausmean_barrel['Summer16']/gausmean_barrel['Run2017F']

    scalefactor_barrel['Run2018A']=gausmean_barrel['Summer16']/gausmean_barrel['Run2018A']
    scalefactor_barrel['Run2018B']=gausmean_barrel['Summer16']/gausmean_barrel['Run2018B']
    scalefactor_barrel['Run2018C']=gausmean_barrel['Summer16']/gausmean_barrel['Run2018C']
    scalefactor_barrel['Run2018D']=gausmean_barrel['Summer16']/gausmean_barrel['Run2018D']

    # Endcap scale factor 
    scalefactor_endcap['Run2016B']=gausmean_barrel['Summer16']/gausmean_endcap['Run2016B']
    scalefactor_endcap['Run2016C']=gausmean_barrel['Summer16']/gausmean_endcap['Run2016C']
    scalefactor_endcap['Run2016D']=gausmean_barrel['Summer16']/gausmean_endcap['Run2016D']
    scalefactor_endcap['Run2016E']=gausmean_barrel['Summer16']/gausmean_endcap['Run2016E']
    scalefactor_endcap['Run2016F']=gausmean_barrel['Summer16']/gausmean_endcap['Run2016F']
    scalefactor_endcap['Run2016G']=gausmean_barrel['Summer16']/gausmean_endcap['Run2016G']
    scalefactor_endcap['Run2016H']=gausmean_barrel['Summer16']/gausmean_endcap['Run2016H']

    scalefactor_endcap['Run2017B']=gausmean_barrel['Summer16']/gausmean_endcap['Run2017B']
    scalefactor_endcap['Run2017C']=gausmean_barrel['Summer16']/gausmean_endcap['Run2017C']
    scalefactor_endcap['Run2017D']=gausmean_barrel['Summer16']/gausmean_endcap['Run2017D']
    scalefactor_endcap['Run2017E']=gausmean_barrel['Summer16']/gausmean_endcap['Run2017E']
    scalefactor_endcap['Run2017F']=gausmean_barrel['Summer16']/gausmean_endcap['Run2017F']

    scalefactor_endcap['Run2018A']=gausmean_barrel['Summer16']/gausmean_endcap['Run2018A']
    scalefactor_endcap['Run2018B']=gausmean_barrel['Summer16']/gausmean_endcap['Run2018B']
    scalefactor_endcap['Run2018C']=gausmean_barrel['Summer16']/gausmean_endcap['Run2018C']
    scalefactor_endcap['Run2018D']=gausmean_barrel['Summer16']/gausmean_endcap['Run2018D']

template = '''
\begin{table}[]
\centering
\begin{tabular}{|r|l|l|l|}
\hline
correction factor & pixel barrel & pixel endcap \\
\hline
 Run2016B    & 1.176               & 1.175        \\
\hline
 Run2016C    & 1.209               & 1.188        \\
\hline
 Run2016D    & 1.234               & 1.194        \\
\hline
 Run2016E    & 1.290               & 1.228        \\
\hline
 Run2016F    & 1.313               & 1.270        \\
\hline
 Run2016G    & 1.375               & 1.301        \\
\hline
 Run2016H    & 1.367               & 1.300        \\
\hline
 Run2017B    & 0.968               & 1.044        \\
\hline
 Run2017C    & 1.212               & 1.188        \\
\hline
 Run2017D    & 1.203               & 1.202        \\
\hline
 Run2017E    & 1.057               & 1.181        \\
\hline
 Run2017F    & 1.146               & 1.272        \\
\hline
 Run2018A    & 1.145               & 1.213        \\
\hline
 Run2018B    & 1.185               & 1.255        \\
\hline
 Run2018C    & 1.202               & 1.286        \\
\hline
 Run2018D    & 1.238               & 1.262        \\
\hline
 Summer16 MC & 1.0                 & 0.956          \\
\hline
 Fall17 MC   & 0.970               & 0.955        \\
\hline
\end{tabular}
\caption{The dE/dx correction factor extracted from muon-matched tracks.}
\label{tab:dedxsf}
\end{table}
'''
