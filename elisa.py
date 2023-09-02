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
numversion = "1.03"
textColor = "blue"
welcomeText = "ELISA VERSION " + numversion + " IS PUTTING ON HER GLASSES"
workingText = "ELISA VERSION " + numversion + " IS ANALYSING THE DATA"
greetingText = "ELISA VERSION " + numversion + " HAS COMPLETED THE ANALYSIS"
dataLocation ='constellations.xlsx' # file name

################################################### CODE

class main:

    ########## start method
    def __init__(self):
        print(colored("--------------------------------------------------------------------------------------",textColor))
        print(colored("--------------------------------------------------------------------------------------",textColor))
        print(colored(welcomeText, textColor))
        print(colored("--------------------------------------------------------------------------------------",textColor))
        print(colored("--------------------------------------------------------------------------------------",textColor))
        try:
            settings = esettings.getSettings() # loading plot settings
            self.survivalAnalysis(settings) # Survival Analysis
            self.sayGreetings() # closing method
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(colored(str(e), 'red'))
            print(colored(str(exc_tb.tb_frame.f_code.co_filename) + " at  line " + str(exc_tb.tb_lineno), 'red'))

    ########## ending method
    def survivalAnalysis(self,settings):
        try:
            print(colored(workingText, textColor))
            #workbook = pd.ExcelFile(dataLocation) # open excel file
            data = load_waltons() # returns a Pandas DataFrame            
            self.plottingFits(settings,data)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(colored(str(e), 'red'))
            print(colored(str(exc_tb.tb_frame.f_code.co_filename) + " at  line " + str(exc_tb.tb_lineno), 'red'))

    ########## plotting 
    def plottingFits(self, settings, data ):
        T = data['T']
        E = data['E']
        groups = data['group']
        ix = (groups == 'miR-137')
        upperX = self.calculateXUpperLimit(data['T'].max(),settings.xbase)
        timeLine = np.linspace(0.0, upperX, settings.tableRowsNumber)
        group2kpfit = {}
        dictionary = settings.functionDictionary
        for function in dictionary:
            plotTitle = self.generatePlotTitle(settings.title, function)
            fig, ax = plt.subplots(1, 1, figsize=(settings.figsize_x, settings.figsize_y))           
            controlGroup = dictionary[function].fit(T[~ix], E[~ix], label='control')
            ax = controlGroup.plot_survival_function(ci_show=True)
            group1 = dictionary[function].fit(T[ix], E[ix], label='miR-137')
            ax = group1.plot_survival_function(ax=ax, ci_show=True)
            
            # if settings.showSummaryTables:
            #     add_at_risk_counts(controlGroup, group1) printing same table twice?

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
            group2kpfit[function + "_control"] = controlGroup
            group2kpfit[function +  "_miR-137"] = group1
        self.generateExcelFile(settings, timeLine, group2kpfit)

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
                    survivaltable.to_excel(writer, sheet_name=group, index=False, header=[settings.timeColumnName,settings.survivalColumnName])
                    table.to_excel(writer, sheet_name=group+'_overview', index=False)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(colored(str(e), 'red'))
            print(colored(str(exc_tb.tb_frame.f_code.co_filename) + " at  line " + str(exc_tb.tb_lineno), 'red'))

    ########## ending method
    def sayGreetings(self):
        print(colored("--------------------------------------------------------------------------------------",textColor))
        print(colored("--------------------------------------------------------------------------------------",textColor))
        print(colored(greetingText, textColor))
        print(colored("--------------------------------------------------------------------------------------",textColor))
        print(colored("--------------------------------------------------------------------------------------",textColor))