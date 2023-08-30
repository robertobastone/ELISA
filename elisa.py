################################################### LIBRARIES
import matplotlib.pyplot as plt
import numpy as np
from lifelines.datasets import load_waltons
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
greetingText = "ELISA VERSION " + numversion + " HAS COMPLETED THE ANALYSIS"
workingText = "ELISA VERSION " + numversion + " IS ANALYSING THE DATA"
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
            self.survivalAnalysis(settings) # Kaplan-Meier Analysis
            self.sayGreetings() # ending quote
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(colored(str(e), 'red'))
            print(colored(str(exc_tb.tb_frame.f_code.co_filename) + " at  line " + str(exc_tb.tb_lineno), 'red'))

    ########## ending method
    def survivalAnalysis(self,settings):
        try:
            print(colored(workingText, textColor))
            #workbook = pd.ExcelFile(dataLocation) # open excel file
            fig, ax = plt.subplots(1, 1, figsize=(settings.figsize_x, settings.figsize_y))

            df = load_waltons() # returns a Pandas DataFrame
            T = df['T']
            E = df['E']
            groups = df['group']
            ix = (groups == 'miR-137')
            upperX = self.calculateXUpperLimit(df['T'].max(),settings.xbase)

            controlGroup = KaplanMeierFitter().fit(T[~ix], E[~ix], label='control')
            ax = controlGroup.plot(ci_show=True)
            group1 = KaplanMeierFitter().fit(T[ix], E[ix], label='miR-137')
            #print(T[ix])
            ax = group1.plot_survival_function(ax=ax, ci_show=True)
            
            ax.set_title(settings.title,fontsize=settings.titleFontSize)
            ########## x axis settings
            ax.set_xlim(settings.xlim[0],upperX)
            ax.set_xlabel(settings.xlabel,fontsize=settings.axisLabelFontSize)
            ########## y axis settings
            ax.set_ylim(settings.ylim[0],settings.ylim[1])
            ax.set_ylabel(settings.ylabel,fontsize=settings.axisLabelFontSize)
            if settings.changeScale:
                ax.set_yticks(settings.yticks)
                ax.set_yticklabels(settings.yticksLabel)

            plt.legend(fontsize=settings.LabelFontSize) # using a size in points
            fig.tight_layout()
            
            plt.savefig(settings.plotName, dpi=settings.dpi)

            group2kpfit = {
                "control": controlGroup,
                "miR-137": group1,                
            }

            self.generateExcelFile(settings,np.linspace(0.0, upperX, settings.tableRowsNumber),group2kpfit)

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

    ########## save results in an excel file
    def generateExcelFile(self, settings, timeline, group2kpfit):
        try:
            with pd.ExcelWriter(settings.excelFile) as writer:  
                for group in group2kpfit:
                    survivalFunction = group2kpfit[group].survival_function_at_times(timeline) # get survival function (panda series)
                    survivaltable =  survivalFunction.reset_index() # get results in table format
                    confidenceInterval = group2kpfit[group].confidence_interval_
                    events = group2kpfit[group].event_table
                    confidenceInterval.rename(columns={'': 'event_at'})
                    table = pd.concat([events, confidenceInterval], axis=1).reset_index()
                    # print(survivaltable.sort_values(by=['index'],ignore_index=True))
                    print(table)
                    # print(colored("--------------------------------------------------------------------------------------",textColor))
                    survivaltable.to_excel(writer, sheet_name=group, index=False, header=[settings.timeColumnName,settings.survivalColumnName])
                    table.to_excel(writer, sheet_name=group+' all data', index=False)
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