# Random Grid Search
## Cut-based optimization (RGS)

Let's get systematic with the optimization. Many tools exist that help to select events with a good sensitivity. The main challenge is that an exaustive scan over all possible cut values on all observables in an n-dimensional space of observables becomes computationally intensive or prohibitive for n>3. 

One interesting tool that seeks to overcome this curse of dimensionality is called a random grid search (RGS), which is documented in the publication, "Optimizing Event Selection with the Random Grid Search" https://arxiv.org/abs/1706.09907. RGS performs a scan over the observable hyperplane, using a set of available simulated signal (or background) events to define steps in the scan. For each step in the scan (each simulated event), a proposed selection set is defined taking the cut values to be the values of the observables of the event. We are going to run RGS on the signal/background samples, and compare the sensitivity of the selection to the hand-picked cuts you obtained previously.  


```
git clone https://github.com/hbprosper/RGS.git
cd RGS/
make
source setup.sh #whenever intending to use RGS
cd ../
pwd
```

The first script to run is tools/rgs_train.py. Open this script up, edit the lumi appropriately (to 35900/pb), give the path to the signal event file you just created, and tweak anything else as you see fit. When finished, save and open tools/LLSUSY.cuts. This file specifies the observables you want RGS to scan over and cut on, as well as the type of cut to apply (greater than, less than, equal to, etc.). Run the (first) training RGS script:

```
python rgs_train.py
```
This creates the file LLSUSY.root which contains a tree of signal and background counts for each possible selection set in the scan. To determine the most optimal cut set, run the (second) analysis RGS script:

```
python rgs_analyze.py
```
This will print the optimum set of thresholds to the screen, as well as the signal and background count corresponding to each set of cuts, and an estimate of the signal significance, z.  How does the RGS optimal selection compare to your hand-picked selection? Hopefully better - if not, you are pretty darn good at eyeball optimization!

You'll have noticed the script also draws a canvas. The scatter plot depicts the ROC cloud, which shows the set of signal and background efficiencies corresponding to each step of the scan. The color map in the background indicates the highest value of the significance of the various cut sets falling into each bin. 

Open up tools/rgs_analyze.py and have a look. You'll notice the significance measure is the simplified z = s/sqrt(b+db^2), where the user can specify the systematic uncertainty (SU) db. The fractional SU is currently set to 0.05. Try changing this value to something larger and rerunning rgs_analyze.py script. 

<b style='color:black'>Question 5. What happened to the optimum thresholds after doubling the SU? How about the expected significance? </b>

<b style='color:black'>Question 6. What value of the systematic uncertainty would correspond to a significance of 2 sigma? This is the worst case uncertainty that would allow us to exclude this signal model. </b>

