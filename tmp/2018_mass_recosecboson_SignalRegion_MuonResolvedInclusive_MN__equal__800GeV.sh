cd /data9/Users/shjeon/THESIS_PROJECTS/ANALYSIS/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/workspace/2018//mass_recosecboson/
text2workspace.py SignalRegion_MuonResolvedInclusive_MN__equal__800GeV.txt -m 125 -o SignalRegion_MuonResolvedInclusive_MN__equal__800GeV.root
combine -M FitDiagnostics SignalRegion_MuonResolvedInclusive_MN__equal__800GeV.root -m 125 --rMin -5 --rMax 5 --saveShapes --saveWithUncertainties --name SignalRegion_MuonResolvedInclusive_MN__equal__800GeV > SignalRegion_MuonResolvedInclusive_MN__equal__800GeV.log
cd /data9/Users/shjeon/THESIS_PROJECTS/ANALYSIS/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit
