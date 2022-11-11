cd /data9/Users/shjeon/THESIS_PROJECTS/ANALYSIS/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/workspace/2016postVFP//masst_recopriboson/
text2workspace.py SignalRegion_ElectronResolvedInclusive_MN__equal__500GeV.txt -m 125 -o SignalRegion_ElectronResolvedInclusive_MN__equal__500GeV.root
combine -M FitDiagnostics SignalRegion_ElectronResolvedInclusive_MN__equal__500GeV.root -m 125 --rMin -5 --rMax 5 --saveShapes --saveWithUncertainties --name SignalRegion_ElectronResolvedInclusive_MN__equal__500GeV > SignalRegion_ElectronResolvedInclusive_MN__equal__500GeV.log
cd /data9/Users/shjeon/THESIS_PROJECTS/ANALYSIS/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit
