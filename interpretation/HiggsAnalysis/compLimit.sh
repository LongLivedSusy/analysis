
# Example to run this script
# ./compLimit.sh datacard_13TeV_dissAppTrack_M1400.txt 1400

datacard=$1
mass=$2
combine -M AsymptoticLimits $datacard -m $mass
