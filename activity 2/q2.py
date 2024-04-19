import matplotlib.pyplot as plt

def graphSnowfall(t):
    
    '''
    Parameter: a string (str) file name t
    
    Initializes a dictionary: snowfall for each range
    
    Opens the file name t in read mode
    
    For each line read, it removes the endline and casts it into
    an integer to count snowfall range.
    
    Extracts keys and values from dictionary as ranges and counts
    
    Creates the bar chart

    Changes the labels and the title
    
    Displays the bar chart
    '''
    snowfallRanges = {
        '0-10': 0,
        '11-20': 0,
        '21-30': 0,
        '31-40': 0,
        '41-50': 0
    }

    with open(t, 'r') as file:
        for line in file:
            snowfall = int(line.strip())
            if snowfall >= 0 and snowfall <= 10:
                snowfallRanges['0-10'] += 1
            elif snowfall >= 11 and snowfall <= 20:
                snowfallRanges['11-20'] += 1
            elif snowfall >= 21 and snowfall <= 30:
                snowfallRanges['21-30'] += 1
            elif snowfall >= 31 and snowfall <= 40:
                snowfallRanges['31-40'] += 1
            elif snowfall >= 41 and snowfall <= 50:
                snowfallRanges['41-50'] += 1

    ranges = list(snowfallRanges.keys())
    counts = list(snowfallRanges.values())

    plt.bar(ranges, counts, color='skyblue')

    plt.xlabel('Snowfall Ranges (in cm)')
    plt.ylabel('Number of Occurrences')
    plt.title('Snowfall Accumulation For A Day')

    plt.show()

# given example
graphSnowfall('data/snowfallData.txt')

