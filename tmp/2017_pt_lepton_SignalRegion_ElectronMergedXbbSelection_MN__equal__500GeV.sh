cd /data9/Users/shjeon/THESIS_PROJECTS/ANALYSIS/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/workspace/2017//pt_lepton/
text2workspace.py SignalRegion_ElectronMergedXbbSelection_MN__equal__500GeV.txt -m 125 -o SignalRegion_ElectronMergedXbbSelection_MN__equal__500GeV.root
combine -M FitDiagnostics SignalRegion_ElectronMergedXbbSelection_MN__equal__500GeV.root -m 125 --rMin -5 --rMax 5 --saveShapes --saveWithUncertainties --name SignalRegion_ElectronMergedXbbSelection_MN__equal__500GeV > SignalRegion_ElectronMergedXbbSelection_MN__equal__500GeV.log
cd /data9/Users/shjeon/THESIS_PROJECTS/ANALYSIS/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit
