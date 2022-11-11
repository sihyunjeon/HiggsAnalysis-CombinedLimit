sample_configs = {

    "data" : {

        "Muon" : {
            "SingleMuon" : {
                "2016preVFP" : ["B_ver2", "C", "D", "E", "F"],
                "2016postVFP" : ["F", "G", "H"],
                "2017" : ["B", "C", "D", "E", "F"],
                "2018" : ["A", "B", "C", "D"]
            }
        },
        "Electron" : {
            "SingleElectron" : {
                "2016preVFP" : ["B_ver2", "C", "D", "E", "F"],
                "2016postVFP" : ["F", "G", "H"],
                "2017" : ["B", "C", "D", "E", "F"],
            },
            "EGamma" :{
                "2018" : ["A", "B", "C", "D"]
            }
        }
    },

    "signal" : {

        "MN__equal__500GeV" : {
            "process" : ["WtoLNtoLNuHtoLNuBB_TypeIHeavyN-Mu_MN500_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-Mu_MN500_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-Mu_MN500_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-Mu_MN500_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuHtoLNuBB_TypeIHeavyN-El_MN500_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-El_MN500_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-El_MN500_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-El_MN500_TuneCP5_13TeV-amcatnlo-pythia8"],
            "style" : 1,
            "scale" : 1.,
            "draw" : False
        },
        "MN__equal__600GeV" : {
            "process" : ["WtoLNtoLNuHtoLNuBB_TypeIHeavyN-Mu_MN600_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-Mu_MN600_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-Mu_MN600_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-Mu_MN600_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuHtoLNuBB_TypeIHeavyN-El_MN600_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-El_MN600_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-El_MN600_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-El_MN600_TuneCP5_13TeV-amcatnlo-pythia8"],
            "style" : 1,
            "scale" : 1.,
            "draw" : True
        },
        "MN__equal__700GeV" : {
            "process" : ["WtoLNtoLNuHtoLNuBB_TypeIHeavyN-Mu_MN700_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-Mu_MN700_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-Mu_MN700_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-Mu_MN700_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuHtoLNuBB_TypeIHeavyN-El_MN700_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-El_MN700_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-El_MN700_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-El_MN700_TuneCP5_13TeV-amcatnlo-pythia8"],
            "style" : 1,
            "scale" : 1.,
            "draw" : False
        },
        "MN__equal__800GeV" : {
            "process" : ["WtoLNtoLNuHtoLNuBB_TypeIHeavyN-Mu_MN800_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-Mu_MN800_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-Mu_MN800_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-Mu_MN800_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuHtoLNuBB_TypeIHeavyN-El_MN800_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-El_MN800_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-El_MN800_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-El_MN800_TuneCP5_13TeV-amcatnlo-pythia8"],
            "style" : 1,
            "scale" : 1.,
            "draw" : False
        },
        "MN__equal__1000GeV" : {
            "process" : ["WtoLNtoLNuHtoLNuBB_TypeIHeavyN-Mu_MN1000_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-Mu_MN1000_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-Mu_MN1000_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-Mu_MN1000_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuHtoLNuBB_TypeIHeavyN-El_MN1000_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-El_MN1000_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-El_MN1000_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-El_MN1000_TuneCP5_13TeV-amcatnlo-pythia8"],
            "style" : 1,
            "scale" : 1.,
            "draw" : True
        },
        "MN__equal__1200GeV" : {
            "process" : ["WtoLNtoLNuHtoLNuBB_TypeIHeavyN-Mu_MN1200_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-Mu_MN1200_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-Mu_MN1200_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-Mu_MN1200_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuHtoLNuBB_TypeIHeavyN-El_MN1200_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-El_MN1200_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-El_MN1200_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-El_MN1200_TuneCP5_13TeV-amcatnlo-pythia8"],
            "style" : 1,
            "scale" : 1.,
            "draw" : False
        },
        "MN__equal__1500GeV" : {
            "process" : ["WtoLNtoLNuHtoLNuBB_TypeIHeavyN-Mu_MN1500_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-Mu_MN1500_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-Mu_MN1500_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-Mu_MN1500_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuHtoLNuBB_TypeIHeavyN-El_MN1500_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-El_MN1500_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-El_MN1500_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-El_MN1500_TuneCP5_13TeV-amcatnlo-pythia8"],
            "style" : 1,
            "scale" : 1.,
            "draw" : False
        },
        "MN__equal__2000GeV" : {
            "process" : ["WtoLNtoLNuHtoLNuBB_TypeIHeavyN-Mu_MN2000_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-Mu_MN2000_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-Mu_MN2000_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-Mu_MN2000_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuHtoLNuBB_TypeIHeavyN-El_MN2000_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-El_MN2000_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-El_MN2000_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-El_MN2000_TuneCP5_13TeV-amcatnlo-pythia8"],
            "style" : 1,
            "scale" : 1.,
            "draw" : False
        },

    },

    "background" : {
        "V__plus__Jets" : {
            "process" : ["WJets_Sherpa", "DYJetsToEE_MiNNLO", "DYJetsToMuMu_MiNNLO", "DYJetsToTauTau_MiNNLO"],
        },
        "VV__comma__VVV" : {
            "process" : ["WWW", "WWZ", "WZZ", "ZZZ", "WW_pythia", "WZ_pythia", "ZZ_pythia", "WplusH_HToBB_WToLNu", "WminusH_HToBB_WToLNu"],
        },
        "Top__space__Pair" : {
            "process" : ["TTLJ_powheg", "TTLL_powheg", "TTJJ_powheg"],
        },
        "Single__space__Top" : {
            "process" : ["SingleTop_sch_Lep", "SingleTop_tW_antitop_NoFullyHad", "SingleTop_tW_top_NoFullyHad", "SingleTop_tch_antitop_Incl", "SingleTop_tch_top_Incl", "ttWToLNu", "ttWToQQ", "ttZToLLNuNu", "ttZToQQ"],
        },
        "Others" : {
            "process" : ["QCD_Pt-15to20_EMEnriched", "QCD_Pt-20to30_EMEnriched", "QCD_Pt-30to50_EMEnriched", "QCD_Pt-50to80_EMEnriched", "QCD_Pt-80to120_EMEnriched", "QCD_Pt-120to170_EMEnriched", "QCD_Pt-170to300_EMEnriched", "QCD_Pt-300toInf_EMEnriched", "QCD_Pt-120To170_MuEnriched", "QCD_Pt-15To20_MuEnriched", "QCD_Pt-170To300_MuEnriched", "QCD_Pt-20To30_MuEnriched", "QCD_Pt-300To470_MuEnriched", "QCD_Pt-30To50_MuEnriched", "QCD_Pt-470To600_MuEnriched", "QCD_Pt-50To80_MuEnriched", "QCD_Pt-600To800_MuEnriched", "QCD_Pt-800To1000_MuEnriched", "QCD_Pt-1000_MuEnriched", "QCD_Pt-80To120_MuEnriched", "QCD_Pt_20to30_bcToE", "QCD_Pt_30to80_bcToE", "QCD_Pt_80to170_bcToE", "QCD_Pt_170to250_bcToE", "QCD_Pt_250toInf_bcToE"]
        },
    },
}

try:
    import ROOT
    sample_configs["signal"]["MN__equal__500GeV"]["color"] = ROOT.kGray+3
    sample_configs["signal"]["MN__equal__600GeV"]["color"] = ROOT.kTeal+10
    sample_configs["signal"]["MN__equal__700GeV"]["color"] = ROOT.kTeal+10
    sample_configs["signal"]["MN__equal__800GeV"]["color"] = ROOT.kTeal+10
    sample_configs["signal"]["MN__equal__1000GeV"]["color"] = ROOT.kTeal+10
    sample_configs["signal"]["MN__equal__1200GeV"]["color"] = ROOT.kTeal+10
    sample_configs["signal"]["MN__equal__1500GeV"]["color"] = ROOT.kTeal+10
    sample_configs["signal"]["MN__equal__2000GeV"]["color"] = ROOT.kTeal+10
    sample_configs["background"]["V__plus__Jets"]["color"] = ROOT.kAzure-3
    sample_configs["background"]["VV__comma__VVV"]["color"] = ROOT.kTeal+10
    sample_configs["background"]["Top__space__Pair"]["color"] = ROOT.kRed-4
    sample_configs["background"]["Single__space__Top"]["color"] = ROOT.kOrange-3
    sample_configs["background"]["Others"]["color"] = ROOT.kYellow-3

except:
    pass
