def wordCount(t):
    
    '''
    Parameter: a string (str) file name t
    
    Creates an empty dictionary and an integer (lineNumber)
    
    Opens the file in read mode
    
    For each line it removes the endline 
    and splits the words by white space
    
    For each word, if the word is not in the dictionary
    then adds the word as key and line number as value
    
    Returns the dictionary
    '''
    
    wordsDict = {}
    lineNum = 1
    with open(t, 'r') as file:
        for line in file:
            words = line.strip().split()
            for word in words :
                if word not in wordsDict:
                    wordsDict[word] = lineNum
            lineNum += 1
    return wordsDict



data = wordCount("data/q3Data.txt")   

for k, v in data.items():
    print(v, ":", k)