################################################### LIBRARIES
import matplotlib.pyplot as plt
import numpy as np
from lifelines.datasets import load_waltons
from lifelines import *
import os # info about file
import sys # better management of the exceptions
import pandas as pd # open excel file
from termcolor import colored # customize ui
import elisa_plotSettings as plotsettings

################################################### CONSTANTS
numversion = "1.01"
textColor = "blue"
welcomeText = "ELISA VERSION " + numversion + " IS PUTTING ON HER GLASSES"
greetingText = "ELISA VERSION " + numversion + " HAS COMPLETED THE ANALYSIS"
workingText = "ELISA VERSION " + numversion + " IS ANALYSING THE DATA"
dataLocation ='constellations.xlsx' # file name

################################################### CODE

class main:

    def __init__(self):
        print(colored("--------------------------------------------------------------------------------------",textColor))
        print(colored("--------------------------------------------------------------------------------------",textColor))
        print(colored(welcomeText, textColor))
        print(colored("--------------------------------------------------------------------------------------",textColor))
        print(colored("--------------------------------------------------------------------------------------",textColor))
        try:
            ### generating mocha_plottersettings object with plot settings
            settings = plotsettings.getPlotSetting()
            self.survivalAnalysis(settings)
            self.sayGreetings()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(colored(str(e), 'red'))
            print(colored(str(exc_tb.tb_frame.f_code.co_filename) + " at  line " + str(exc_tb.tb_lineno), 'red'))

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

            controlGroup = KaplanMeierFitter().fit(T[~ix], E[~ix], label='control')
            ax = controlGroup.plot(ci_show=False)
            group1 = KaplanMeierFitter().fit(T[ix], E[ix], label='miR-137')
            ax = group1.plot_survival_function(ax=ax, ci_show=False)
            
            ax.set_title(settings.title,fontsize=settings.titleFontSize)
            ########## x axis settings
            ax.set_xlim(settings.xlim[0], df['T'].max()*1.1)
            ax.set_xlabel(settings.xlabel,fontsize=settings.axisLabelFontSize)
            ########## y axis settings
            ax.set_ylim(settings.ylim[0],settings.ylim[1])
            ax.set_ylabel(settings.ylabel,fontsize=settings.axisLabelFontSize)
            ax.set_yticks(settings.yticks)
            ax.set_yticklabels(settings.yticksLabel)

            plt.legend(fontsize=settings.LabelFontSize) # using a size in points
            fig.tight_layout()
            
            plt.savefig(settings.plotName, dpi=settings.dpi)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(colored(str(e), 'red'))
            print(colored(str(exc_tb.tb_frame.f_code.co_filename) + " at  line " + str(exc_tb.tb_lineno), 'red'))

    def sayGreetings(self):
        print(colored("--------------------------------------------------------------------------------------",textColor))
        print(colored("--------------------------------------------------------------------------------------",textColor))
        print(colored(greetingText, textColor))
        print(colored("--------------------------------------------------------------------------------------",textColor))
        print(colored("--------------------------------------------------------------------------------------",textColor))