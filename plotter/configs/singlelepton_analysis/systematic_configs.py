systematic_configs = {

    "Luminosity" : {
        "variation" : "lognormal",
        "type" : "uncorrelated",
        "2016" : "1.012",
        "2017" : "1.023",
        "2018" : "1.025",
    },
    "JetRes" : {
        "variation" : "updown",
        "type" : "correlated"
    },
    "JetEn" : {
        "variation" : "updown",
        "type" : "correlated"
    },
    "JetMassScale" : {
        "variation" : "updown",
        "type" : "correlated"
    },
#    "JetMassRes" : {
#        "variation" : "updown",
#        "type" : "uncorrelated"
#    },
    "UnclEn" : {
        "variation" : "updown",
        "type" : "correlated"
    },
    "MuonEn" : {
        "variation" : "updown",
        "type" : "correlated"
    },
    "MuonRecoSF" : {
        "variation" : "updown",
        "type" : "correlated"
    },
    "MuonIDSF" : {
        "variation" : "updown",
        "type" : "correlated"
    },
    "MuonISOSF" : {
        "variation" : "updown",
        "type" : "correlated"
    },
    "MuonTriggerSF" : {
        "variation" : "updown",
        "type" : "uncorrelated"
    },
    "ElectronRes" : {
        "variation" : "updown",
        "type" : "correlated"
    },
    "ElectronEn" : {
        "variation" : "updown",
        "type" : "correlated"
    },
    "ElectronRecoSF" : {
        "variation" : "updown",
        "type" : "correlated"
    },
    "ElectronIDSF" : {
        "variation" : "updown",
        "type" : "correlated"
    },
    "ElectronTriggerSF" : {
        "variation" : "updown",
        "type" : "uncorrelated"
    },
    "Pileup" : {
        "variation" : "updown",
        "type" : "correlated"
    },
    "Prefire" : {
        "variation" : "updown",
        "type" : "correlated"
    },
    "BTagCorrH" : {
        "variation" : "updown",
        "type" : "correlated"
    },
    "BTagCorrL" : {
        "variation" : "updown",
        "type" : "correlated"
    },
    "BTagUnCorrH" : {
        "variation" : "updown",
        "type" : "uncorrelated"
    },
    "BTagUnCorrL" : {
        "variation" : "updown",
        "type" : "uncorrelated"
    },
    "TopPtReweight" : {
        "variation" : "other",
        "name" : "TopPtReweight",
        "type" : "correlated",
        "sample" : "Top__space__Pair"
    },
    "Scale" : {
        "variation" : "other",
        "name" : "Scale",
        "type" : "correlated",
        "sample" : "MN__equal",
        "value" : "1.001"
    },
    "PDF" : {
        "variation" : "other",
        "name" : "PDF",
        "type" : "correlated",
        "sample" : "MN__equal",
        "value" : "1.005"
    }
}

