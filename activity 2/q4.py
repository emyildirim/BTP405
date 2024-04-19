def printStats(t):
    
    '''
    Parameter: a string (str) file name
    
    Opens the file t in read mode
    
    For each line it calls print_stats after removing the endline
    '''
    
    with open(t, "r") as file:
        for line in file:
            print_stats(line.strip())


def statsDecorator(func):
    
    '''
    Parameter: a function
    
    Calls the inner function:
        splits the numbers from the line into a list
        counts how many numbers in the list
        gets the sum, average amd max number.
        
    Displays all the info
    '''
    
    def printer(numbers):
        numList = list(map(int, numbers.split(',')))
        count = len(numList)
        total = sum(numList)
        average = total / count
        maximum = max(numList)

        print("Numbers read:", numList)
        print("Count:", count)
        print("Average:", average)
        print("Maximum:", maximum)
        
    return printer  


@statsDecorator
def print_stats(numbers):
    '''
    executes:
    print_stats = stats_decorator(print_stats)
    
    since empty body not allowed, placeholder 'pass' used
    
    '''
    pass
                
            
            
printStats("data/q4Nums.txt")