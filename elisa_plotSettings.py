######################### LIBRARIES #########################

######################### CODE #########################

class getPlotSetting:

    def __init__(self):
        ########## plot size
        self.figsize_x = 13
        self.figsize_y = 10
        ########## plot size
        self.title = 'Survival Function (Kaplan-Meier estimator)' 
        ########## plot font size
        self.titleFontSize = 20
        self.axisLabelFontSize = 15
        self.LabelFontSize = 15 
        ########## x axis settings
        self.xlim = [0,1.1]
        self.xlabel = 'Time'
        self.yticks = [0.2,0.4,0.6,0.8,1.0]
        self.yticksLabel = [20,40,60,80,100]
        ########## x axis settings
        self.ylim = [0,1.1]
        self.ylabel = 'Population Survival (percentage)'
        ########## save settings
        self.dpi = 150
        self.plotName = 'elisa.png'
        
        