def getPrimeNumbers(n):
    
    '''
    Parameter: a positive integer n
    
    Checks if are there prime numbers between 2 and n 
    
    Returns all the prime numbers found in the given range as a list
    '''
    
    primeNums = []
    for num in range(2, n + 1):
        if isPrime(num):
            primeNums.append(num)
    return primeNums


def isPrime(number):
    
    '''
    Receives an positive integer number
    
    Checks if the number is divisible by any number
    between 2 and the number
    
    If the number is not divisible, it is a prime number
    Returns True and otherwise False
    ''' 
    
    if number <= 1:
        return False
    for i in range(2, number):
        if number % i == 0:
            return False
    return True
    
    
if __name__ == "__main__":
    print(__name__)
    n = int(input("Enter a number: "))
    print("Prime numbers between 2 and", n, "are:", getPrimeNumbers(n))



