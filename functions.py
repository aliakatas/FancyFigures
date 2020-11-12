import datetime
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS 
import pandas as pd
import seaborn as sns

###############################################################
def getTimestamp():
    '''
    Get a timestamp of the current time.
    Returns:
        - The timestamp in format %Y%m%dT%H%M%S: (str)
    '''
    dateTimeObj = datetime.datetime.now()
    return dateTimeObj.strftime("%Y%m%dT%H%M%S")

###############################################################
def getInputArgs(flag, args):
    '''
    Get the input arguments based on specific flag.
    Parameters:
        - flag: (str) The flag to look for with the hyphen
        - args: (list, str) The list of arguments provided from command line
    Returns:
        The requested argument (str), None otherwise.
    '''
    if len(flag) == 0:
        return args[1]

    for arg in args:
        if arg.startswith(flag):
            return arg[len(flag):]
    return None

###############################################################
def getColumnIDInteractive(cols, msg):
    '''
    Get the column ID interactively from the user.
    Parameters:
        - cols: (list, str) Columns headers in the dataframe
        - msg: (str) Helping message to show to the user
    Returns:
        The ID (int) of the column selected from the user, None otherwise.
    '''
    for ind, item in zip(range(len(cols)), cols):
        print(f'{ind} :: {item}')

    choice = input(f'Provide ID of column to process #{msg}:: ')
    if not choice.isnumeric():
        return None

    choice = int(choice)
    if choice >= 0 and choice < len(cols):
        return choice
    else:
        return None

###############################################################
def getDictionariesFromColEntries(entries):
    out = {}
    out_rev = {}
    for it, entry in zip(range(len(entries)), entries):
        out[entry] = it
        out_rev[it] = entry
    return out, out_rev

###############################################################
def createPieChart(y, data, name, display=False):
    minidf = data.groupby(y)[y].count()
    
    minidf.plot.pie(y=y, figsize=(8, 8), autopct='%1.1f%%')
    plt.savefig(name, dpi=200)
    if display:
        plt.show()

###############################################################
def createWordCloud(y, data, name, max_words=200, ignore=[], display=False):
    comment_words = '' 
    stopwords = set(STOPWORDS)
    stopwords.update(ignore)
    stopwords.update(['none'])
    
    # iterate through the csv file 
    for val in data[y]: 
        # typecaste each val to string 
        val = str(val) 
    
        # split the value 
        tokens = val.split() 

        # Converts each token into lowercase 
        for i in range(len(tokens)): 
            tokens[i] = tokens[i].lower() 
        
        comment_words += " ".join(tokens)+" "

    wordcloud = WordCloud(width = 750, height = 750,        # was 800x800
            background_color ='white', 
            stopwords = stopwords, 
            min_font_size = 10, max_words=max_words).generate(comment_words) 

    # plot the WordCloud image                        
    plt.figure(figsize = (7, 7), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    plt.savefig(name , dpi=200)
    if display:
        plt.show()

###############################################################
def readVarList(fname):
    with open(fname, 'r') as f:
        lines = f.readlines()

    out = {}
    for line in lines:
        words = line.split()
        if len(words) > 1:
            out[int(words[0])] = ' '.join(line.split()[1:])
        else:
            out[int(words[0])] = ''
    return out

###############################################################
def readExcludedWords(fname):
    with open(fname, 'r') as f:
        lines = f.readlines()

    out = []
    for line in lines:
        out.append(line.split()[0].strip())
    return out

###############################################################
def dumpToText(fname, x, data, min_len=5):
    with open(fname, 'w') as w:
        for item in data[x]:
            if len(str(item)) >= min_len:
                w.write(f'{item.strip()} \n')

###############################################################
def createBarChart(x, data, name, legend, dislpay=False):
    uniqueAnswers = {}
    for row in data[x]:
        item = str(row)
        rowEntries = item.strip().split(';')
        for entryIn in rowEntries:
            entry = entryIn.strip()
            if len(entry) > 0:
                if entry in uniqueAnswers:
                    uniqueAnswers[entry] += 1
                else:
                    uniqueAnswers[entry] = 1

    significantAnswers = {}
    otherList = []
    for key in uniqueAnswers.keys():
        if uniqueAnswers[key] > 2:
            significantAnswers[key] = uniqueAnswers[key]
        else:
            otherList.append(key)
            if 'Other' in significantAnswers:
                significantAnswers['Other'] += uniqueAnswers[key]
            else:
                significantAnswers['Other'] = uniqueAnswers[key]   
    
    ans_dict, rev_ans_dict = getDictionariesFromColEntries(list(significantAnswers.keys()))
    d = {'Answers': [ans_dict[key] for key in ans_dict.keys()], 
        'Count': [significantAnswers[key] for key in significantAnswers.keys()]}
    
    newdf = pd.DataFrame(data = d)
    
    ax = newdf.plot.bar(x='Answers', y='Count', rot=0)

    myLabels = ax.get_xticklabels()
    ax.set_xticklabels(myLabels, rotation=20, fontsize='x-small') 
    ax.set_xlabel('')

    plt.savefig(name, dpi=200)
    if dislpay:
        plt.show()
    
    with open(legend + '_legend.txt', 'w') as w:
        for key in rev_ans_dict.keys():
            w.write(f'{key} :: {rev_ans_dict[key]} \n')
    with open(legend +'_other.txt', 'w') as w:
        for item in otherList:
            w.write(f'{item} \n')

###############################################################
def createHeatmap(var_list, data, name, legend, dislpay=False):
    ylist = var_list
    optionsMix = data[ylist[0]].unique()
    
    zeroList = [0] * len(ylist)

    options = []
    for item in optionsMix:
        if isinstance(item, str):
            options.append(str(item))
    
    d = {}
    for item in options:
        d[item] = zeroList
    
    ans_dict, rev_ans_dict = getDictionariesFromColEntries(ylist)
    df = pd.DataFrame(data = d, index=[ans_dict[key] for key in ans_dict.keys()])
    
    for col in rev_ans_dict:
        temp = data.groupby(rev_ans_dict[col])[rev_ans_dict[col]].count()
        for option in options:
            if option in temp.index:
                df[option][col] = temp[option]

    ax = sns.heatmap(df, annot=True, fmt="d")

    ax.set_xticklabels(ax.get_xticklabels(), rotation=20, fontsize='x-small') 

    myYlabels = ax.get_yticklabels()
    
    ax.set_yticklabels(myYlabels, fontsize='x-small', rotation=55)

    plt.savefig(name, dpi=200)
    if dislpay:
        plt.show()

    with open(legend, 'w') as w:
        for key in rev_ans_dict.keys():
            w.write(f'{key} :: {rev_ans_dict[key]} \n')


