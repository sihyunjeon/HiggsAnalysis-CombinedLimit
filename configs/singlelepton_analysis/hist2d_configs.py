import math
import array

math_pi = math.pi

hist_configs = {

    "masst_leptonmet_vs_dphi_leptonmet" : {

        "x_min" : 0.,
        "x_max" : 1000.,
        "x_rebin" : array.array("f", [0., 40., 60., 80., 100., 120., 160., 200., 400., 1000.]),
        "x_label" : "M_{T}(l,#slash{E}_{T}^{miss})",

        "y_min" : 0.,
        "y_max" : 3.2, #1.0*math_pi,
        "y_rebin" : array.array("f", [0., 2.]), #[-1.0*math_pi. -0.8*math_pi, -0.6*math_pi, -0.4*math_pi, -0.2*math_pi, 0., 0.2*math_pi, 0.4*math_pi, 0.6*math_pi, 0.8*math_pi, 1.0*math_pi] ),
        "y_label" : "#DeltaPhi(l,#slash{E}_{T}^{miss})",
        "contour" : [
            [300, 0.0], [300, 0.0]
        ]
    },

    "masst_leptonmet_vs_cosdphi_leptonmet" : {

        "x_min" : 0.,
        "x_max" : 1000.,
        "x_rebin" : array.array("f", [0., 40., 60., 80., 100., 120., 160., 200., 400., 1000.]),
        "x_label" : "M_{T}(l,#slash{E}_{T}^{miss})",

        "y_min" : -1.0,
        "y_max" : 1.0, #1.0*math_pi,
        "y_rebin" : array.array("f", [0., 2.]), #[-1.0*math_pi. -0.8*math_pi, -0.6*math_pi, -0.4*math_pi, -0.2*math_pi, 0., 0.2*math_pi, 0.4*math_pi, 0.6*math_pi, 0.8*math_pi, 1.0*math_pi] ),
        "y_label" : "#DeltaPhi(l,#slash{E}_{T}^{miss})",
        "contour" : [
            [300, 0.0], [300, 0.0]
        ]
    },


}

