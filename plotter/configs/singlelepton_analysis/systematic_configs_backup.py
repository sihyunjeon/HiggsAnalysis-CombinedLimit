systematic_configs = {

    "Luminosity" : {
        "variation" : "lognormal",
        "type" : "uncorrelated",
        "2016preVFP" : "1.012",
        "2016postVFP" : "1.012",
        "2017" : "1.023",
        "2018" : "1.025",
    },
    "JetRes" : {
        "variation" : "updown",
        "type" : "uncorrelated"
    },
    "JetEn" : {
        "variation" : "updown",
        "type" : "uncorrelated"
    },
    "JetMassScale" : {
        "variation" : "updown",
        "type" : "uncorrelated"
    },
    "JetMassRes" : {
        "variation" : "updown",
        "type" : "uncorrelated"
    },
    "UnclEn" : {
        "variation" : "updown",
        "type" : "uncorrelated"
    },
    "MuonEn" : {
        "variation" : "updown",
        "type" : "uncorrelated"
    },
    "MuonRecoSF" : {
        "variation" : "updown",
        "type" : "uncorrelated"
    },
    "MuonIDSF" : {
        "variation" : "updown",
        "type" : "uncorrelated"
    },
    "MuonISOSF" : {
        "variation" : "updown",
        "type" : "uncorrelated"
    },
    "MuonTriggerSF" : {
        "variation" : "updown",
        "type" : "uncorrelated"
    },
    "ElectronRes" : {
        "variation" : "updown",
        "type" : "uncorrelated"
    },
    "ElectronEn" : {
        "variation" : "updown",
        "type" : "uncorrelated"
    },
    "ElectronRecoSF" : {
        "variation" : "updown",
        "type" : "uncorrelated"
    },
    "ElectronIDSF" : {
        "variation" : "updown",
        "type" : "uncorrelated"
    },
    "ElectronTriggerSF" : {
        "variation" : "updown",
        "type" : "uncorrelated"
    },
    "Pileup" : {
        "variation" : "updown",
        "type" : "uncorrelated"
    },
    "Prefire" : {
        "variation" : "updown",
        "type" : "uncorrelated"
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

