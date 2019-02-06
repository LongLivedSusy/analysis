# Non-prompt background estimation

## How to run

* Configure and run ```submit_fakerate.py``` to create a skim of the fake rate estimation regions
* Run ```plot_fakerate_maps.py``` to create the fake rate maps depending on HT and pile-up. The result will be saved in ```fakerate.root```.
* Configure and run ```submit_skim.py``` to create a skim and apply the fake rate to the control region (signal region without any DTs).
* Run ```plot_closure.py``` to merge the MC and data output files and to create the closure plot.
