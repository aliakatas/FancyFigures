import sys
import os
import pandas as pd
import functions as fn
from AppConf import AppConf, PIECHART, BARCHART, WORDCLOUD, HEATMAP

#############################################
def prepare_for_exit(msg, normal=False):
    '''
    Dislpay messages before terminating execution.

    Parameters:
        msg: (str) - Custom message to display
        normal: (bool) - True if the termination is expected, false otherwise.
    '''
    print(msg)
    if not normal:
        print('Aborting!')
    else:
        print('Done.')

###############################################################
def main():
    '''
    The main control!
    '''
    # Initialise the configuration object for this instance
    appConfiguration = AppConf()

    print('')
    if appConfiguration.showHelp():
        prepare_for_exit('', normal=True)
        return

    exeName = os.path.split(sys.argv[0])
    print(f'Running {exeName[1]}...')

    # Get some things out of the way
    if len(sys.argv) == 0:
        prepare_for_exit('ERROR: MS Office Excel file needed as argument...')
        return 

    # Get the xls file    
    appConfiguration.setXLSfile()
    if not os.path.exists(appConfiguration.getXLSfile()):
        prepare_for_exit(f'ERROR: File does not exist :: {appConfiguration.getXLSfile()}')
        return

    # Check if we have interactive mode enabled
    appConfiguration.setInteractiveSession()

    # Check if output location is provided
    appConfiguration.setOutputPath()

    # Get columns from user
    ok = appConfiguration.setWorkingColumns()
    if not ok:
        prepare_for_exit('ERROR: Variables list file does not exist or no column IDs provided...')
        return 

    # # Get figure kind from command line/user
    ok = appConfiguration.setFigureKind()
    if not ok:
        prepare_for_exit('ERROR: No valid input for figure type is provided...')
        return 

    # Check if graphs should be displayed before saving
    appConfiguration.setViewFigure()
    
    # Get the name of the output file (if given)
    appConfiguration.setOutputFileName()

    # Check if there is a need to write to text file as well
    appConfiguration.setSupportFileName()

    # For wordclouds, get the exclusion list (if present)
    appConfiguration.setStopwords()

    # Get the contents of the file
    print(f'Reading {appConfiguration.getXLSfile()}...', end='')
    xlsContents = pd.read_excel(appConfiguration.getXLSfile())
    dfColumns = xlsContents.columns
    print(' OK')
    
    # Check if any user interaction is needed
    appConfiguration.interactWithUser(dfColumns)

    # Make sure that we got something to work with 
    if len(appConfiguration.getWorkingColumns()) == 0:
        prepare_for_exit('ERROR: No valid input is provided...')
        return

    # Show a briefing before doing the work
    print(appConfiguration)

    # Ensure that each graph gets the correct input
    ok = appConfiguration.sanityCheck()
    if not ok:
        prepare_for_exit('')
        return
    
    # Create figures
    print('Saving figure...', end='')
    figKind = appConfiguration.getFigureKind()
    viewFigure = appConfiguration.viewFigure()
    figFilename = appConfiguration.getOutputFileName()
    stopwords_custom = appConfiguration.getStopwords()
    txtFile = appConfiguration.getSupportFileName()
    varList = appConfiguration.getWorkingColumns()
    key = list(varList.keys())[0]

    ok = True
    if figKind == PIECHART:
        # Do the pie chart
        fn.createPieChart(dfColumns[key], xlsContents, figFilename, display=viewFigure)
    elif figKind == WORDCLOUD:
        # Do the wordcloud
        fn.createWordCloud(dfColumns[key], xlsContents, figFilename, max_words=200, ignore=stopwords_custom, display=viewFigure)    
        if len(txtFile) > 0:
            fn.dumpToText(txtFile, dfColumns[key], xlsContents)
    elif figKind == BARCHART:
        # Do the bar chart
        fn.createBarChart(dfColumns[key], xlsContents, figFilename, txtFile, display=viewFigure)
    elif figKind == HEATMAP:
        # Do the heatmap
        colList = [dfColumns[i] for i in varList]
        fn.createHeatmap(colList, xlsContents, figFilename, txtFile, display=viewFigure)
    else: 
        print('\n ** Not yet implemented! **')
        print('WARNING: No figure is produced!')
        ok = False
    
    if ok:
        print('OK')

    #TODO Produce any statistics?
    print('Goodbye.\n')

###############################################################
# The main program
if __name__ == '__main__':
    main()
    