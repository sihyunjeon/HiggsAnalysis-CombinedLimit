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

        "m_{N} = 500GeV" : {
            "process" : ["WtoLNtoLNuHtoLNuBB_TypeIHeavyN-Mu_MN500_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-Mu_MN500_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-Mu_MN500_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-Mu_MN500_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuHtoLNuBB_TypeIHeavyN-El_MN500_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-El_MN500_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-El_MN500_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-El_MN500_TuneCP5_13TeV-amcatnlo-pythia8"],
            "color" : ROOT.kBlack,
            "style" : 1,
            "scale" : 100.
        },

        "m_{N} = 1000GeV" : {
            "process" : ["WtoLNtoLNuHtoLNuBB_TypeIHeavyN-Mu_MN1000_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-Mu_MN1000_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-Mu_MN1000_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-Mu_MN1000_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuHtoLNuBB_TypeIHeavyN-El_MN1000_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-El_MN1000_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-El_MN1000_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-El_MN1000_TuneCP5_13TeV-amcatnlo-pythia8"],
            "color" : ROOT.kBlack,
            "style" : 2,
            "scale" : 100.
        },


    },

    "background" : {
        "V" : {
            "process" : ["WJets_Sherpa", "DYJetsToEE_MiNNLO", "DYJetsToMuMu_MiNNLO", "DYJetsToTauTau_MiNNLO"],
            "color" : ROOT.kBlue-4
        },
        "VV" : {
            "process" : ["WW_pythia", "WZ_pythia", "ZZ_pythia"],
            "color" : ROOT.kGreen+1
        },
        "TOP" : {
            "process" : ["SingleTop_sch_Lep", "SingleTop_tW_antitop_NoFullyHad", "SingleTop_tW_top_NoFullyHad", "SingleTop_tch_antitop_Incl", "SingleTop_tch_top_Incl", "TTLJ_powheg", "TTLL_powheg", "TTJJ_powheg"],
            "color" : ROOT.kRed-4
        },
        "QCD" : {
            "process" : ["QCD_Pt-15to20_EMEnriched", "QCD_Pt-20to30_EMEnriched", "QCD_Pt-30to50_EMEnriched", "QCD_Pt-50to80_EMEnriched", "QCD_Pt-80to120_EMEnriched", "QCD_Pt-120to170_EMEnriched", "QCD_Pt-170to300_EMEnriched", "QCD_Pt-300toInf_EMEnriched", "QCD_Pt-120To170_MuEnriched", "QCD_Pt-15To20_MuEnriched", "QCD_Pt-170To300_MuEnriched", "QCD_Pt-20To30_MuEnriched", "QCD_Pt-300To470_MuEnriched", "QCD_Pt-30To50_MuEnriched", "QCD_Pt-470To600_MuEnriched", "QCD_Pt-50To80_MuEnriched", "QCD_Pt-600To800_MuEnriched", "QCD_Pt-800To1000_MuEnriched", "QCD_Pt-80To120_MuEnriched"],
            "color" : ROOT.kGray+1
        },
        "others" : {
            "process" : [],
            "color" : ROOT.kYellow-3
        },
    },
}
'''
    "background" : {
        "WJets" : {
            "process" : ["WJets_Sherpa"],
            "color" : ROOT.kBlue-4
        },
        "DYJets" : {
            "process" : ["DYJetsToEE_MiNNLO", "DYJetsToMuMu_MiNNLO", "DYJetsToTauTau_MiNNLO"],
            "color" : ROOT.kAzure+9
        },
        "VV" : {
            "process" : ["WW_pythia", "WZ_pythia", "ZZ_pythia"],
            "color" : ROOT.kGreen+1
        },
        "single top" : {
            "process" : ["SingleTop_sch_Lep", "SingleTop_tW_antitop_NoFullyHad", "SingleTop_tW_top_NoFullyHad", "SingleTop_tch_antitop_Incl", "SingleTop_tch_top_Incl"],
            "color" : ROOT.kOrange-2
        },
        "top" : {
            "process" : ["TTLJ_powheg", "TTLL_powheg", "TTJJ_powheg"],
            "color" : ROOT.kRed-4
        },
        "QCD" : {
            "process" : ["QCD_Pt-15to20_EMEnriched", "QCD_Pt-20to30_EMEnriched", "QCD_Pt-30to50_EMEnriched", "QCD_Pt-50to80_EMEnriched", "QCD_Pt-80to120_EMEnriched", "QCD_Pt-120to170_EMEnriched", "QCD_Pt-170to300_EMEnriched", "QCD_Pt-300toInf_EMEnriched", "QCD_Pt-120To170_MuEnriched", "QCD_Pt-15To20_MuEnriched", "QCD_Pt-170To300_MuEnriched", "QCD_Pt-20To30_MuEnriched", "QCD_Pt-300To470_MuEnriched", "QCD_Pt-30To50_MuEnriched", "QCD_Pt-470To600_MuEnriched", "QCD_Pt-50To80_MuEnriched", "QCD_Pt-600To800_MuEnriched", "QCD_Pt-800To1000_MuEnriched", "QCD_Pt-80To120_MuEnriched"],
            "color" : ROOT.kGray+1
        },
        "others" : {
            "process" : [],
            "color" : ROOT.kYellow-3
        },
     }
'''
