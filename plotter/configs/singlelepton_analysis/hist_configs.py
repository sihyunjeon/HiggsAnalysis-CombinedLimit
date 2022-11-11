import math

hist_configs = {

    "dphi_leptonmet" : {
        "x_label" : "#Delta#phi(l,E^{miss}_{T})",
        "x_bins" : {
            "Combined" : [0., 0.2, 0.5, math.pi*0.25, math.pi*0.40, math.pi],
        }
    },
    "mass_recosecboson" : {
        "x_label" : "m(X^{reco}) [GeV]",
        "x_bins" : {
            "Combined" : [0., 50., 65., 105., 145., 200., 450.],
        }
    },
    "masst_recopriboson" : {
        "x_label" : "m_{T}(l,E^{miss}_{T},J) [GeV]",
        "x_bins" : {
            "Merged" : [500., 600., 750., 900., 1300.],
            "Resolved" : [500., 600., 750., 1300.],
        }
    },
    "masst_leptonmet" : {
        "x_label" : "m_{T}(l,E^{miss}_{T}) [GeV]",
        "x_bins" : {
            "Combined" : [250., 300., 350., 400., 850.],
        }
    },
    "met" : {
        "x_label" : "E^{miss}_{T} [GeV]",
        "x_bins" : {
            "Combined" : [100., 150., 200., 250., 650.],
        }
    },
    "n_jet" : {
        "x_label" : "Number of jets",
        "x_bins" : {
            "Combined" : [0., 1., 2., 3., 4.],
        }
    },
    "n_bjet" : {
        "x_label" : "Number of b-jets",
        "x_bins" : {
            "Combined" : [0., 1., 2., 3., 4.],
        }
    },
    "pt_lepton" : {
        "x_label" : "p_{T}(l) [GeV]",
        "x_bins" : {
            "Combined" : [50., 100., 150., 200., 650.],
        }
    },


}

