cd /data9/Users/shjeon/THESIS_PROJECTS/ANALYSIS/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/workspace/2017//mass_recosecboson/
text2workspace.py SignalRegion_MuonResolvedXqqSelection_MN__equal__800GeV.txt -m 125 -o SignalRegion_MuonResolvedXqqSelection_MN__equal__800GeV.root
combine -M FitDiagnostics SignalRegion_MuonResolvedXqqSelection_MN__equal__800GeV.root -m 125 --rMin -5 --rMax 5 --saveShapes --saveWithUncertainties --name SignalRegion_MuonResolvedXqqSelection_MN__equal__800GeV > SignalRegion_MuonResolvedXqqSelection_MN__equal__800GeV.log
cd /data9/Users/shjeon/THESIS_PROJECTS/ANALYSIS/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit
