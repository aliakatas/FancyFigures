NOFIGKIND = ''
VIOLINCHART = 'violin'
SWARMCHART = 'swarm'
BARCHART = 'bar'
JOINTCHART = 'joint'
HEATMAP = 'heat'
PIECHART = 'pie'
WORDCLOUD = 'wcloud'

VALID_FIGURE_KINDS = [NOFIGKIND, VIOLINCHART, SWARMCHART, BARCHART, JOINTCHART, HEATMAP, PIECHART, WORDCLOUD]

YES = 'y'
NO = 'n'

YES_NO = [YES, NO]

OUTFOLDER_F = '-o'
GRAPHKIND_F = '-k'
FILENAME_F = '-q'
COLLIST_F = '-l'
SUPFILE_F = '-t'
STOPWORDS_F = '-s'
VIEWFIGURE_F = '-v'
INTERACTIVE_F = '-i'
HELP_F = '-h'

VALID_FLAGS = {
    OUTFOLDER_F: 'output folder', 
    GRAPHKIND_F: 'kind of graph',
    FILENAME_F: 'filename for the output graph',
    COLLIST_F: 'file with list of column IDs to use',
    SUPFILE_F: 'filename for supporting text file (multiple uses)',
    STOPWORDS_F: 'file with custom stopwords for word cloud',
    VIEWFIGURE_F: 'flag to force viewing of the figure after saving',
    INTERACTIVE_F: 'flag to indicate interactive mode',
    HELP_F: 'show help'
}