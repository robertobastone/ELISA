################################################### LIBRARIES
import matplotlib.pyplot as plt
import numpy as np
import itertools
#from lifelines.datasets import load_waltons
from lifelines.plotting import add_at_risk_counts
from lifelines import *
from lifelines.statistics import *
import os # info about file
import sys # better management of the exceptions
import pandas as pd # open excel file
from termcolor import colored # customize ui
import elisa_settings as esettings

################################################### CODE

######### defining wrapper class for SurvivalFit Object
class SurvivalFit(object):
    groupname = ""
    color = ""
    time = []
    events = []
    survivalFit = ()

    def __init__(self, groupname, color, time, events, survivalFit):
        self.groupname = groupname
        self.color = color
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
            self.raiseGenericException(e, settings.exceptionColor)

    ########## generate UI message method
    def generateUImessage(self, message, textColor):
        print(colored("--------------------------------------------------------------------------------------",textColor))
        print(colored("--------------------------------------------------------------------------------------",textColor))
        print(colored(message, textColor))
        print(colored("--------------------------------------------------------------------------------------",textColor))
        print(colored("--------------------------------------------------------------------------------------",textColor))

    ########## generate UI message method
    def raiseGenericException(self, exception, textColor):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(colored(str(exception), textColor))
        print(colored(str(exc_tb.tb_frame.f_code.co_filename) + " at  line " + str(exc_tb.tb_lineno), textColor))

    ########## ending method
    def survivalAnalysis(self,settings):
        try:
            print(colored(settings.workingText, settings.textColor))
            data = pd.ExcelFile('walton.xlsx') # open excel file
            self.plottingFits(settings,data)
        except Exception as e:
            self.raiseGenericException(e, settings.exceptionColor)

    ########## plotting
    def plottingFits(self, settings, data ):
        try:
            dataControl = data.parse(settings.controlSheet)
            dataGroup = data.parse(settings.groupSheet)
            #dataThird = data.parse(settings.thirdGroupSheet)
            upperX = self.calculateXUpperLimit(dataControl['T'].max(),settings.xbase)
            timeLine = np.linspace(0.0, upperX, settings.tableRowsNumber)
            group2kpfit = {}
            dictionary = settings.functionDictionary      
            sfList = [SurvivalFit(settings.controlSheet, settings.controlSheetColor, dataControl['T'], dataControl['E'], None),
                        SurvivalFit(settings.groupSheet, settings.groupSheetColor, dataGroup['T'], dataGroup['E'], None)]
                        #SurvivalFit('3rd', settings.thirdGroupSheetColor, dataThird['T'], dataThird['E'], None)]
            for function in dictionary:
                fitList = []
                plotTitle = self.generatePlotTitle(settings.title, function)
                fig, ax = plt.subplots(1, 1, figsize=(settings.figsize_x, settings.figsize_y))
                for sf in sfList:
                    fit = dictionary[function]().fit(sf.time, sf.events, label=sf.groupname)
                    ax = fit.plot_survival_function(color=sf.color, ci_show=settings.showCI, show_censors=settings.showCensors, censor_styles={'ms': 6, 'marker': 's'})
                    sf.survivalFit = fit
                    fitList.append(fit)
                    #group2kpfit[function +  "_" + sf.groupname] = fit
                    group2kpfit[sf.groupname] = fit 
                if settings.showSummaryTables:
                    add_at_risk_counts(*fitList)
                if settings.runStatisticTests:
                    resultDictionary = self.generateTestResults(settings, sfList)  
                    ax2 = ax.twinx()
                    customHandles = [ax2.plot([],[], ms=0, label = 'p-value ' + result + ' = {0:.9f}'.format(resultDictionary[result].p_value), ls="") for result in resultDictionary]
                    ax2.legend(handles=customHandles, labels='', loc=4, title="", fontsize=settings.LabelFontSize, handlelength=0, handletextpad=0)
                    ax2.get_yaxis().set_visible(False)
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
                ax.legend(loc=3, fontsize=settings.LabelFontSize)
                if settings.hideLegend:
                    ax.get_legend().remove()
                plt.tight_layout()
                plt.savefig((function + settings.plotName).replace(' ', ''), dpi=settings.dpi)  
            self.generateSurvivalFunctionExcelFile(settings, timeLine, group2kpfit)
        except Exception as e:
            self.raiseGenericException(e, settings.exceptionColor)

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
    def generateTestResults(self, settings, sfList):
        try:
            resultDictionary = {}
            testDictionary = settings.testDictionary
            with pd.ExcelWriter(settings.excelPValuesFile) as writer:  
                for test in testDictionary:
                    if test == 'survivalDiff':
                        if(len(sfList)==2):
                            resultDictionary['(Survival Difference)'] = testDictionary[test](settings.pointIntime, sfList[1].survivalFit, sfList[0].survivalFit)
                        else:
                            continue
                    elif test == 'logRank':
                        if(len(sfList)>=2):
                            allPossibleCouples = list(itertools.combinations(range(len(sfList)), 2))
                            for couple in allPossibleCouples:
                                resultDictionary['('+sfList[couple[0]].groupname+' vs '+sfList[couple[1]].groupname+')'] = testDictionary[test](sfList[couple[0]].time, sfList[couple[1]].time, event_observed_A=sfList[couple[0]].events, event_observed_B=sfList[couple[1]].events)
                        else:
                            continue
                    elif test == 'multiLogRank':
                        if(len(sfList)>=2):
                            totalTimes = []
                            totalEvents = []
                            totalGroups = []
                            for i in range(len(sfList)):
                                totalTimes.extend(sfList[i].time)
                                totalEvents.extend(sfList[i].events)
                                totalGroups.extend(np.full(len(sfList[i].time), i))
                            dataFrame = pd.DataFrame({
                                'time': totalTimes,
                                'events': totalEvents,
                                'groups': totalGroups
                            })
                            resultDictionary['(MultiLog Rank)'] = testDictionary[test](dataFrame['time'], dataFrame['groups'], dataFrame['events'])
                        else:
                            continue
                    for result in resultDictionary:
                        pvalue =  resultDictionary[result].p_value
                        testStats = resultDictionary[result].test_statistic   
                        df = pd.DataFrame([[pvalue, testStats]], columns=['p_value', 'test Stats'])        
                        df.to_excel(writer, sheet_name=(result+test+'results').replace(' ', '')[:settings.truncate], index=False)
                return resultDictionary
        except Exception as e:
            self.raiseGenericException(e, settings.exceptionColor)

    ########## save results in an excel file
    def generateSurvivalFunctionExcelFile(self, settings, timeline, group2kpfit):
        try:
            with pd.ExcelWriter(settings.excelFile) as writer:  
                for group in group2kpfit:
                    # first we generate the survival table
                    survivalFunction = group2kpfit[group].survival_function_at_times(timeline) # get survival function (panda series)
                    survivaltable =  survivalFunction.reset_index() # get results in table format
                    survivaltable.to_excel(writer, sheet_name=group[:settings.truncate], index=False, header=[settings.timeColumnName,settings.survivalColumnName])
                    # secondly we generate the event table
                    confidenceInterval = group2kpfit[group].confidence_interval_
                    events = group2kpfit[group].event_table
                    eventtable = pd.concat([events, confidenceInterval], axis=1).reset_index()
                    eventtable.rename(columns={ eventtable.columns[0]: settings.timeColumnName}, inplace=True) # inplace attribute prevents from creating a copy 
                    eventtable.to_excel(writer, sheet_name=(group+'_overview')[:settings.truncate], index=False)
        except Exception as e:
            self.raiseGenericException(e, settings.exceptionColor)