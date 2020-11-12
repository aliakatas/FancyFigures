import sys
import os
import functions as fn
from AppData import * 

#############################################
def print_flags():
    for key in VALID_FLAGS.keys():
        print(f'   {key} :: {VALID_FLAGS[key]}')

#############################################
def simple_user_dialogue(msg, options):
    '''
    Provides a simple interface for user dialogue.

    Parameters:
        msg: (str) - Custom message to display
        options: (list, str) - List of acceptable options
    Returns:
        The options selected by the user in lowercase.
    '''
    choice = input(msg + '(' + '/'.join(options) + ')  ')

    while not (choice.lower() in options):
        choice = input('Please type ' + '/'.join(options) + '  ')
    return choice.lower()

#############################################
class AppConf:
    def __init__(self):
        self.xlsFile = ''
        self.dataPath = ''
        self.interactive_session = False
        self.outputPath = ''
        self.xcol = None
        self.ycol = None
        self.zcol = None
        self.figureKind = ''
        self.view = False
        self.outFileName = ''
        self.columns = {}
        self.supportFileName = ''
        self.stopwords_custom = []

    #~~~~~~~~~~~~~~~~~~~~
    def showHelp(self):
        show = fn.getInputArgs(HELP_F, sys.argv)
        if not (show is None):
            print('Application usage: ')
            print(f'    {os.path.split(sys.argv[0])[1]} data_file (flags)')
            print('where flags are optional and they are:')
            print_flags()
            return True
        return False

    #~~~~~~~~~~~~~~~~~~~~
    def setXLSfile(self):
        # Get the xls file    
        xlsFile = fn.getInputArgs('', sys.argv)
        self.xlsFile = os.path.abspath(xlsFile)
        self.dataPath = os.path.split(xlsFile)[0]
    
    def getXLSfile(self):
        return self.xlsFile

    #~~~~~~~~~~~~~~~~~~~~
    def getXLSfilePath(self):
        return self.dataPath

    #~~~~~~~~~~~~~~~~~~~~
    def setInteractiveSession(self):
        # Check if we have interactive mode enabled
        if not (fn.getInputArgs(INTERACTIVE_F, sys.argv) is None):
            self.interactive_session = True

    def isInteractiveSession(self):
        return self.interactive_session

    #~~~~~~~~~~~~~~~~~~~~
    def setOutputPath(self):
        outputPath = fn.getInputArgs(OUTFOLDER_F, sys.argv)
        if outputPath:
            self.outputPath = os.path.abspath(outputPath)
        else:
            self.outputPath = os.path.join(self.dataPath, 'figures_' + fn.getTimestamp())
        
        # Create the output folder if it's not there
        if not os.path.exists(self.outputPath):
            print(f'Creating output folder :: {self.outputPath}')
            os.makedirs(self.outputPath)

    def getOutputPath(self):
        return self.outputPath

    #~~~~~~~~~~~~~~~~~~~~
    def setWorkingColumns(self):
        # Get column ID to be viewed on x-axis
        for var in ['-x', '-y', '-z']:
            x = fn.getInputArgs(var, sys.argv)
            if not (x is None):
                self.columns[int(x)] = ''

        n = len(self.columns)
        if n > 0:
            return True

        # Check and read (if present) the list of vars to be used in heatmap
        varFile = fn.getInputArgs(COLLIST_F, sys.argv)
        
        if not (varFile is None):
            varFile = os.path.abspath(varFile)
            if not os.path.exists(varFile):
                return False
                
            self.columns = fn.readVarList(varFile)
            return True
        
        return self.interactive_session

    def getWorkingColumns(self):
        return self.columns

    #~~~~~~~~~~~~~~~~~~~~
    def setFigureKind(self):
        # Get the type of figure needed
        figKind = fn.getInputArgs(GRAPHKIND_F, sys.argv)
        if not (figKind is None):
            self.figureKind = figKind.lower()
        
        # Ensure there is a valid figure type (kind)
        if not (self.figureKind in VALID_FIGURE_KINDS):
            return False
        
        return self.interactive_session

    def getFigureKind(self):
        return self.figureKind

    #~~~~~~~~~~~~~~~~~~~~
    def setViewFigure(self):
        # Check if graphs should be displayed before saving
        if not (fn.getInputArgs(VIEWFIGURE_F, sys.argv) is None):
            self.view = True
    
    def viewFigure(self):
        return self.view

    #~~~~~~~~~~~~~~~~~~~~
    def setOutputFileName(self):
        # Get the name of the output file (if given)
        outFileName = fn.getInputArgs(FILENAME_F, sys.argv)
        if not (outFileName is None):
            self.outFileName = os.path.join(self.outputPath, f'{outFileName}.png')
        else:
            self.outFileName = os.path.join(self.outputPath, 'result.png')

    def getOutputFileName(self):
        return self.outFileName
    
    #~~~~~~~~~~~~~~~~~~~~
    def setSupportFileName(self):
        # Check if there is a need to write to text file as well
        txtFile = fn.getInputArgs(SUPFILE_F, sys.argv)
        if not (txtFile is None):
            self.supportFileName = os.path.abspath(os.path.join(self.outputPath, txtFile))

    def getSupportFileName(self):
        return self.supportFileName

    #~~~~~~~~~~~~~~~~~~~~
    def setStopwords(self):
        # For wordclouds, get the exclusion list (if present)
        stopwords_file = fn.getInputArgs(STOPWORDS_F, sys.argv)
        if not (stopwords_file is None):
            stopwords_file = os.path.abspath(stopwords_file)
            if not os.path.exists(stopwords_file):
                print('WARNING: Exluded words list file does not exist...')
                print('Continuing with defaults.')
            else:
                self.stopwords_custom = fn.readExcludedWords(stopwords_file)
    
    def getStopwords(self):
        return self.stopwords_custom

    #~~~~~~~~~~~~~~~~~~~~
    def getChoices(self, dfColumns):
        choice = YES
        it = 1
        while choice == YES:
            var_x = fn.getColumnIDInteractive(dfColumns, f'{it}')
            if not (var_x is None):
                self.columns[var_x] = dfColumns[var_x]
            
            choice = simple_user_dialogue('Wish to add another column?', YES_NO)
            it += 1

    def interactWithUser(self, dfColumns):
        if self.interactive_session:
            if len(self.columns) > 0:
                print('Column IDs are already provided.')

                choice = simple_user_dialogue('Wish to override?', YES_NO)
                
                if choice == NO:
                    print('Continuing with current choices...')
                else:
                    # Manual entry...
                    self.getChoices(dfColumns)                    
            else:
                self.getChoices(dfColumns)

            if len(self.figureKind) > 0:
                print('Figure type is already provided.')

                choice = simple_user_dialogue('Wish to override?', YES_NO)
                
                if choice == NO:
                    print('Continuing with current choice...')
                else:
                    self.figureKind = simple_user_dialogue('Please choose the type: ', VALID_FIGURE_KINDS)
            else:
                self.figureKind = simple_user_dialogue('Please choose the type: ', VALID_FIGURE_KINDS)

    #~~~~~~~~~~~~~~~~~~~~
    def __str__(self):
        out = '\n-----------------------\n'
        out += 'Current configuration\n'
        for key in self.columns.keys():
            out += f'-> Column :: {key}, {self.columns[key]} \n'

        out += f'Figure will be saved in :: {self.outputPath}\n'
        out += f'As :: {os.path.split(self.getOutputFileName())[1]}\n'
        out += f'Type of figure :: {self.figureKind}\n'
        
        if self.view:
            out += 'Figure will be displayed after saving\n'
        else:
            out += 'Figure will NOT be displayed, just saved\n'
        
        if len(self.supportFileName) > 0:
            out += f'Support file produced as :: {self.supportFileName}\n'
        out += '-----------------------\n'
        return out
    
    #~~~~~~~~~~~~~~~~~~~~
    def sanityCheck(self):
        n = len(self.columns)
        if self.figureKind == PIECHART or self.figureKind == WORDCLOUD or self.figureKind == BARCHART or self.figureKind == HEATMAP:
            if n < 1:
                print(f'ERROR: No valid input is provided for {self.figureKind}...')
                print('Consider defining -x or -y flags or pass a list-file of column IDs')
                return False
            
        if self.figureKind == HEATMAP:
            if n < 3:
                print(f'NOTE: Consider another type of graph for {n} columns')
        
        return True