################################################### LIBRARIES
import matplotlib.pyplot as plt
import numpy as np
from lifelines.datasets import load_waltons
from lifelines.plotting import add_at_risk_counts
from lifelines import *
import os # info about file
import sys # better management of the exceptions
import pandas as pd # open excel file
from termcolor import colored # customize ui
import elisa_settings as esettings

################################################### CONSTANTS
dataLocation ='constellations.xlsx' # file name

################################################### CODE

######### defining wrapper class for SurvivalFit Object
class SurvivalFit(object):
    groupname = ""
    time = []
    events = []
    survivalFit = ()

    def __init__(self, groupname, time, events, survivalFit):
        self.groupname = groupname
        self.time = time
        self.events = events
        self.survivalFit = survivalFit

class main:

    ########## start method
    def __init__(self):
        try:
            settings = esettings.getSettings() # loading plot settings
            self.generateUImessage(settings.welcomeText,settings.textColor) # welcome message
            self.survivalAnalysis(settings) # Survival Analysis
            self.generateUImessage(settings.greetingText,settings.textColor) # goodbye message
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(colored(str(e), 'red'))
            print(colored(str(exc_tb.tb_frame.f_code.co_filename) + " at  line " + str(exc_tb.tb_lineno), 'red'))

    ########## generate UI message method
    def generateUImessage(self, message, textColor):
        print(colored("--------------------------------------------------------------------------------------",textColor))
        print(colored("--------------------------------------------------------------------------------------",textColor))
        print(colored(message, textColor))
        print(colored("--------------------------------------------------------------------------------------",textColor))
        print(colored("--------------------------------------------------------------------------------------",textColor))

    ########## ending method
    def survivalAnalysis(self,settings):
        try:
            print(colored(settings.workingText, settings.textColor))
            #workbook = pd.ExcelFile(dataLocation) # open excel file
            data = load_waltons() # returns a Pandas DataFrame            
            self.plottingFits(settings,data)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(colored(str(e), 'red'))
            print(colored(str(exc_tb.tb_frame.f_code.co_filename) + " at  line " + str(exc_tb.tb_lineno), 'red'))

    ########## plotting 
    def plottingFits(self, settings, data ):
        try:
            T = data['T']
            E = data['E']
            groups = data['group']
            ix = (groups == 'miR-137')
            upperX = self.calculateXUpperLimit(data['T'].max(),settings.xbase)
            timeLine = np.linspace(0.0, upperX, settings.tableRowsNumber)
            group2kpfit = {}
            dictionary = settings.functionDictionary
            sfList = [SurvivalFit('control', T[~ix], E[~ix], None),
                        SurvivalFit('miR-137', T[ix], E[ix], None)]
            for function in dictionary:
                fitList = []
                plotTitle = self.generatePlotTitle(settings.title, function)
                fig, ax = plt.subplots(1, 1, figsize=(settings.figsize_x, settings.figsize_y))
                for sf in sfList:      
                    fit = dictionary[function]().fit(sf.time,sf.events, label=sf.groupname)
                    ax = fit.plot_survival_function(ci_show=True, show_censors=True, censor_styles={'ms': 6, 'marker': 's'})
                    sf.survivalFit = fit
                    fitList.append(fit)
                    group2kpfit[function +  "_" + sf.groupname] = fit 
                if settings.showSummaryTables:
                    add_at_risk_counts(*fitList)
                ax.set_title(plotTitle,fontsize=settings.titleFontSize)
                ########## x axis settings
                ax.set_xlim(settings.xlim[0],upperX)
                ax.set_xlabel(settings.xlabel,fontsize=settings.axisLabelFontSize)
                ########## y axis settings
                ax.set_ylim(settings.ylim[0],settings.ylim[1])
                ax.set_ylabel(settings.ylabel,fontsize=settings.axisLabelFontSize)
                if settings.changeScale:
                    ax.set_yticks(settings.yticks)
                    ax.set_yticklabels(settings.yticksLabel)
                ax.legend(fontsize=settings.LabelFontSize)
                plt.tight_layout()
                plt.savefig(function + settings.plotName, dpi=settings.dpi)
                
            self.generateExcelFile(settings, timeLine, group2kpfit)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(colored(str(e), 'red'))
            print(colored(str(exc_tb.tb_frame.f_code.co_filename) + " at  line " + str(exc_tb.tb_lineno), 'red'))

    ########## custom ceiling method
    def calculateXUpperLimit(self, maxValue, base):
        offset = 0
        if maxValue % base == 0:
            offset = base
        return (-(maxValue // -base)*base)+offset

    ########## generate plot title
    def generatePlotTitle(self, title, function):
        return title + ' (' + function + ')'

    ########## save results in an excel file
    def generateExcelFile(self, settings, timeline, group2kpfit):
        try:
            with pd.ExcelWriter(settings.excelFile) as writer:  
                for group in group2kpfit:
                    survivalFunction = group2kpfit[group].survival_function_at_times(timeline) # get survival function (panda series)
                    survivaltable =  survivalFunction.reset_index() # get results in table format
                    confidenceInterval = group2kpfit[group].confidence_interval_
                    events = group2kpfit[group].event_table
                    table = pd.concat([events, confidenceInterval], axis=1).reset_index()
                    table.rename(columns={ table.columns[0]: settings.timeColumnName}, inplace=True) # inplace attribute prevents from creating a copy 
                    # print(survivaltable.sort_values(by=['index'],ignore_index=True)
                    # print(colored("--------------------------------------------------------------------------------------",textColor))
                    survivaltable.to_excel(writer, sheet_name=group[:settings.truncate], index=False, header=[settings.timeColumnName,settings.survivalColumnName])
                    table.to_excel(writer, sheet_name=(group+'_overview')[:settings.truncate], index=False)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(colored(str(e), 'red'))
            print(colored(str(exc_tb.tb_frame.f_code.co_filename) + " at  line " + str(exc_tb.tb_lineno), 'red'))