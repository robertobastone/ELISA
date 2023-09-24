######################### LIBRARIES #########################
from lifelines import KaplanMeierFitter, WeibullFitter, ExponentialFitter

######################### CODE #########################

class getSettings:

    def __init__(self):

        self.numversion = "1.04"

        ######################### FIT SETTINGS
        self.functionDictionary = { "Kaplan Meier": KaplanMeierFitter,
                                    "Weibull Fitter":  WeibullFitter,
                                    "Exponential Fitter": ExponentialFitter
        } # list here the fitter function of the lifeline library

        ######################### UI SETTINGS
        self.textColor = "blue"
        self.exceptionColor = "red"
        self.welcomeText = "ELISA VERSION " + self.numversion + " IS PUTTING ON HER GLASSES"
        self.workingText = "ELISA VERSION " + self.numversion + " IS ANALYSING THE DATA"
        self.greetingText = "ELISA VERSION " + self.numversion + " HAS COMPLETED THE ANALYSIS"

        ######################### PLOT SETTINGS
        ########## plot size
        self.figsize_x = 13
        self.figsize_y = 10
        ########## plot title
        self.title = 'Survival Function' 
        ########## plot font size
        self.titleFontSize = 20
        self.axisLabelFontSize = 15
        self.LabelFontSize = 15 
        ########## x axis settings
        self.xlim = [0,None]
        self.xlabel = 'Time'
        self.xbase = 10
        self.showSummaryTables = True
        if self.showSummaryTables:
            self.xlim = [None,None] # if true, no limits should be forced, this way the table will be aligned to the x ticks
        ########## x axis settings
        self.ylim = [0,1.05]
        self.ylabel = 'Population Survival (percentage)'
        self.changeScale = True
        self.yticks = [0.2,0.4,0.6,0.8,1.0]
        self.yticksLabel = [20,40,60,80,100]
        ########## save settings
        self.dpi = 150
        self.plotName = '_elisa.png'

        ######################### TABLE SETTINGS
        ########## table settings
        self.tableRowsNumber = 31
        ########## preventing from naming sheets with more than specified number of characters
        self.truncate = 30
        ########## table settings
        self.timeColumnName = 'Time'
        self.survivalColumnName = 'Survival Probability (percentage)'
        ########## save settings
        self.excelFile = 'results.xlsx'
        
        