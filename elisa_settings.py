######################### LIBRARIES #########################
from lifelines import KaplanMeierFitter, WeibullFitter, ExponentialFitter
from lifelines.statistics import logrank_test, multivariate_logrank_test, survival_difference_at_fixed_point_in_time_test

######################### CODE #########################

class getSettings:

    def __init__(self):

        self.numversion = "1.09"

        ######################### ENTRY DATA
        ########## control group or first group
        self.controlSheet = 'control'
        self.controlSheetColor = '#333399'
        ########## group or second group
        self.groupSheet =  'group'
        self.groupSheetColor = '#cc1912'
        ######### third group
        self.thirdGroupSheet =  'third'
        self.thirdGroupSheetColor = '#0b5e15'
       
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
        self.title = 'Walton Data' 
        ########## plot font size
        self.titleFontSize = 20
        self.axisLabelFontSize = 15
        ########## x axis settings
        self.xlim = [0,None]
        self.xlabel = 'Time (month)'
        self.xbase = 10
        self.showSummaryTables = False
        if self.showSummaryTables:
            self.xlim = [None,None] # if true, no limits should be forced, this way the table will be aligned to the x ticks
        ########## x axis settings
        self.ylim = [0,1.05]
        self.ylabel = 'Population Survival (%)'
        self.changeScale = True
        self.yticks = [0.2,0.4,0.6,0.8,1.0]
        self.multiplier = 100
        self.yticksLabel = [int(tick * self.multiplier) for tick in self.yticks]
        ########## confidence intervals and censors settings
        self.showCI = False
        self.showCensors = False
        ########## legend settings
        self.LabelFontSize = 15
        self.hideLegend = False
        ########## save settings
        self.dpi = 150
        self.plotName = self.title + '.png'

        ######################### TABLE AND EXCEL SETTINGS
        ########## table settings
        self.tableRowsNumber = 31
        ########## preventing from naming sheets with more than specified number of characters
        self.truncate = 30
        ########## table settings
        self.timeColumnName = 'Time'
        self.survivalColumnName = 'Survival Probability (percentage)'
        ########## save settings
        self.excelFile = self.title.replace(' ', '') + 'results.xlsx'
        
        ######################### TEST SETTINGS
        self.runStatisticTests = True
        ########## list here the fitter function(s) of the lifeline library
        self.functionDictionary = { 
                                    # "Weibull Fitter":  WeibullFitter,
                                    # "Exponential Fitter": ExponentialFitter,
                                    "Kaplan Meier": KaplanMeierFitter
        } 
        ########## list here the test function(s) of the lifelines.statistics library
        self.testDictionary = {
                        # "survivalDiff": survival_difference_at_fixed_point_in_time_test,
                        "logRank": logrank_test
                        #"multiLogRank" : multivariate_logrank_test 
        } 
        ########## logrank_test
        # Comparison of two survival curves can be done using logrank_test 
        # In order to test the null hypothesis (= no difference between the population survival curves)
        # Simply put, the probability of an event occurring at any time is the same for each group
        # The method returns the p-value (evaluated from the chi squared distribution with 1 degree of freedom)
        # A very small p-value means that the observed behaviour would be unlikely under the null hypothesis
        ########## multivariate_logrank_test
        # Log Rank Test for multiple groups
        # When we consider two groups, the multivariate_logrank_test is equivalent to the logrank_test
        ########## survival_difference_at_fixed_point_in_time_test
        # Rather than comparing the entire survival curves of two groups, we can compare the probabilty at a given time
        # survival_difference_at_fixed_point_in_time_test compares it at a specific point in time using chi-squared test.
        # Be wary that this method implicitly exploits the log-log transformation
        self.pointIntime = 100
        self.excelPValuesFile = self.title.replace(' ', '') + 'pvalues.xlsx'