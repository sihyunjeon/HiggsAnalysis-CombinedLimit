import ROOT

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

        "MN_500" : {
            "process" : ["WtoLNtoLNuHtoLNuBB_TypeIHeavyN-Mu_MN500_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-Mu_MN500_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-Mu_MN500_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-Mu_MN500_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuHtoLNuBB_TypeIHeavyN-El_MN500_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-El_MN500_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-El_MN500_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-El_MN500_TuneCP5_13TeV-amcatnlo-pythia8"],
        },
        "MN_600" : {
            "process" : ["WtoLNtoLNuHtoLNuBB_TypeIHeavyN-Mu_MN600_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-Mu_MN600_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-Mu_MN600_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-Mu_MN600_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuHtoLNuBB_TypeIHeavyN-El_MN600_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-El_MN600_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-El_MN600_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-El_MN600_TuneCP5_13TeV-amcatnlo-pythia8"],
        },
        "MN_700" : {
            "process" : ["WtoLNtoLNuHtoLNuBB_TypeIHeavyN-Mu_MN700_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-Mu_MN700_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-Mu_MN700_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-Mu_MN700_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuHtoLNuBB_TypeIHeavyN-El_MN700_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-El_MN700_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-El_MN700_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-El_MN700_TuneCP5_13TeV-amcatnlo-pythia8"],
        },
        "MN_800" : {
            "process" : ["WtoLNtoLNuHtoLNuBB_TypeIHeavyN-Mu_MN800_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-Mu_MN800_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-Mu_MN800_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-Mu_MN800_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuHtoLNuBB_TypeIHeavyN-El_MN800_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-El_MN800_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-El_MN800_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-El_MN800_TuneCP5_13TeV-amcatnlo-pythia8"],
        },
        "MN_1000" : {
            "process" : ["WtoLNtoLNuHtoLNuBB_TypeIHeavyN-Mu_MN1000_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-Mu_MN1000_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-Mu_MN1000_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-Mu_MN1000_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuHtoLNuBB_TypeIHeavyN-El_MN1000_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-El_MN1000_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-El_MN1000_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-El_MN1000_TuneCP5_13TeV-amcatnlo-pythia8"],
        },

    },

    "background" : {
        "w_boson" : {
            "process" : ["WJets_Sherpa"],
        },
        "multiboson" : {
            "process" : ["WWW", "WWZ", "WZZ", "ZZZ", "WW_pythia", "WZ_pythia", "ZZ_pythia"],
        },
        "top_pair" : {
            "process" : ["TTLJ_powheg", "TTLL_powheg", "TTJJ_powheg"],
        },
        "top_others" : {
            "process" : ["SingleTop_sch_Lep", "SingleTop_tW_antitop_NoFullyHad", "SingleTop_tW_top_NoFullyHad", "SingleTop_tch_antitop_Incl", "SingleTop_tch_top_Incl", "ttWToLNu", "ttWToQQ", "ttZToLLNuNu", "ttZToQQ"],
        },
        "others" : {
            "process" : [
"QCD_Pt-15to20_EMEnriched", "QCD_Pt-20to30_EMEnriched", "QCD_Pt-30to50_EMEnriched", "QCD_Pt-50to80_EMEnriched", "QCD_Pt-80to120_EMEnriched", "QCD_Pt-120to170_EMEnriched", "QCD_Pt-170to300_EMEnriched", "QCD_Pt-300toInf_EMEnriched", "QCD_Pt-120To170_MuEnriched", "QCD_Pt-15To20_MuEnriched", "QCD_Pt-170To300_MuEnriched", "QCD_Pt-20To30_MuEnriched", "QCD_Pt-300To470_MuEnriched", "QCD_Pt-30To50_MuEnriched", "QCD_Pt-470To600_MuEnriched", "QCD_Pt-50To80_MuEnriched", "QCD_Pt-600To800_MuEnriched", "QCD_Pt-800To1000_MuEnriched", "QCD_Pt-1000_MuEnriched", "QCD_Pt-80To120_MuEnriched", "QCD_Pt_20to30_bcToE", "QCD_Pt_30to80_bcToE", "QCD_Pt_80to170_bcToE", "QCD_Pt_170to250_bcToE", "QCD_Pt_250toInf_bcToE",
"WplusH_HToBB_WToLNu", "WminusH_HToBB_WToLNu",
"DYJetsToEE_MiNNLO", "DYJetsToMuMu_MiNNLO", "DYJetsToTauTau_MiNNLO"],
        },
    },
}
