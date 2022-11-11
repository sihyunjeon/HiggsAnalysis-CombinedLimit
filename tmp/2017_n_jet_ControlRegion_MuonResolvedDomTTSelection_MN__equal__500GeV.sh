cd /data9/Users/shjeon/THESIS_PROJECTS/ANALYSIS/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/workspace/2017//n_jet/
text2workspace.py ControlRegion_MuonResolvedDomTTSelection_MN__equal__500GeV.txt -m 125 -o ControlRegion_MuonResolvedDomTTSelection_MN__equal__500GeV.root
combine -M FitDiagnostics ControlRegion_MuonResolvedDomTTSelection_MN__equal__500GeV.root -m 125 --rMin -5 --rMax 5 --saveShapes --saveWithUncertainties --name ControlRegion_MuonResolvedDomTTSelection_MN__equal__500GeV > ControlRegion_MuonResolvedDomTTSelection_MN__equal__500GeV.log
cd /data9/Users/shjeon/THESIS_PROJECTS/ANALYSIS/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit
