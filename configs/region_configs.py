region_configs = {

    "Muon" : {
        '''
        "Preselection_Muon" : {
            "Preselection" : True,
            "MergedSR" : True,
            "ResolvedSR" : True,

        },
        '''
        "Control_Muon" : {
            "ControlRegionXbb-InvB" : True,
            "ControlRegionXbb-InvMt" : True,
            "ControlRegionXbb-InvDeltaPhi" : True,
            "ControlRegionXqq-InvB" : True,
            "ControlRegionXqq-InvMt" : True,
            "ControlRegionXqq-InvDeltaPhi" : True,
        },
        "Signal_Muon" : {
            "SignalRegionXbb-HighMassHighPtJ" : False,
            "SignalRegionXbb-HighMassLowPtJ" : False,
            "SignalRegionXbb-LowMassHighPtJ" : False,
            "SignalRegionXbb-LowMassLowPtJ" : False,
            "SignalRegionXqq-HighMassHighPtJ" : False,
            "SignalRegionXqq-HighMassLowPtJ" : False,
            "SignalRegionXqq-LowMassHighPtJ" : False,
            "SignalRegionXqq-LowMassLowPtJ" : False,
        },
    },
    "Electron" : {
        "Preselection_Electron" : {
            "Preselection" : True
        },
        "Control_Electron" : {
            "ControlRegionXbb-InvB" : True,
            "ControlRegionXbb-InvMt" : True,
            "ControlRegionXbb-InvDeltaPhi" : True,
            "ControlRegionXqq-InvB" : True,
            "ControlRegionXqq-InvMt" : True,
            "ControlRegionXqq-InvDeltaPhi" : True,
        },
        "Signal_Electron" : {
            "SignalRegionXbb-HighMassJ" : False,
            "SignalRegionXbb-LowMassJ" : False,
            "SignalRegionXqq-LowMassJ" : False,
        },
    }
}

