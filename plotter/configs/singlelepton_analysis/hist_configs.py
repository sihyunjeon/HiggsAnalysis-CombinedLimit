import math

hist_configs = {

    "masst_recopriboson" : {
        "x_label" : "m_{T}(l,E^{miss}_{T},X^{reco}) [GeV]",
        "x_latex" : "$m_{T}(\\ell,\\ETslash,X^{\\text{reco}})$",
        "x_bins" : {
            "Merged" : [500., 600., 750., 900., 1300.],
            "Resolved" : [500., 600., 750., 1300.],
        }
    },
    "mass_recosecboson" : {
        "x_label" : "m(X^{reco}) [GeV]",
        "x_latex" : "$m(X^{\\text{reco}})$",
        "x_bins" : {
            "Combined" : [0., 50., 65., 105., 145., 200., 450.],
        }
    },
    "dphi_leptonmet" : {
        "x_label" : "#Delta#phi(l,E^{miss}_{T})",
        "x_latex" : "$\\Delta\\phi(\\ell,\\ETslash)$",
        "x_bins" : {
            "Combined" : [0., 0.2, 0.5, math.pi*0.25, math.pi*0.40, math.pi],
        }
    },
    "masst_leptonmet" : {
        "x_label" : "m_{T}(l,E^{miss}_{T}) [GeV]",
        "x_latex" : "$m_{T}(\\ell,\\ETslash)$",
        "x_bins" : {
            "Combined" : [250., 300., 350., 400., 850.],
        }
    },
    "met" : {
        "x_label" : "E^{miss}_{T} [GeV]",
        "x_latex" : "$\\ETslash$",
        "x_bins" : {
            "Combined" : [100., 150., 200., 250., 650.],
        }
    },
    "n_jet" : {
        "x_label" : "Number of jets",
        "x_latex" : "$N(j)$",
        "x_bins" : {
            "Combined" : [0., 1., 2., 3., 4.],
        }
    },
    "n_bjet" : {
        "x_label" : "Number of b-jets",
        "x_latex" : "$N(b)$",
        "x_bins" : {
            "Combined" : [0., 1., 2., 3., 4.],
        }
    },
    "pt_lepton" : {
        "x_label" : "p_{T}(l) [GeV]",
        "x_latex" : "$p_{T}(\\ell)$",
        "x_bins" : {
            "Combined" : [50., 100., 150., 200., 650.],
        }
    },
    "eta_lepton" : {
        "x_label" : "#eta(l)",
        "x_latex" : "$\\eta(\\ell)$",
        "x_bins" : {
            "Combined" : [-2.1, -1.6, -1.2, -0.8, -0.4, 0., 0.4, 0.8, 1.2, 1.6, 2.1],
        }
    },

}
