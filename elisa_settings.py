######################### LIBRARIES #########################

######################### CODE #########################

class getSettings:

    def __init__(self):

        ######################### PLOT SETTINGS
        ########## plot size
        self.figsize_x = 13
        self.figsize_y = 10
        ########## plot title
        self.title = 'Survival Function (Kaplan-Meier estimator)' 
        ########## plot font size
        self.titleFontSize = 20
        self.axisLabelFontSize = 15
        self.LabelFontSize = 15 
        ########## x axis settings
        self.xlim = [0,1.1]
        self.xlabel = 'Time'
        self.xbase = 10
        ########## x axis settings
        self.ylim = [0,1.05]
        self.ylabel = 'Population Survival (percentage)'
        self.yticks = [0.2,0.4,0.6,0.8,1.0]
        self.yticksLabel = [20,40,60,80,100]
        ########## save settings
        self.dpi = 150
        self.plotName = 'elisa.png'

        ######################### TABLE SETTINGS
        ########## table settings
        self.tableRowsNumber = 31
        ########## table settings
        self.timeColumnName = 'Time'
        self.survivalColumnName = 'Survival Probability (percentage)'
        ########## save settings
        self.excelFile = 'results.xlsx'
        
        