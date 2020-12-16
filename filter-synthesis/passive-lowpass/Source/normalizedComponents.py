from math import pi, sin

""" Simple Python program to calculate the normalized values for capacitors and inductors given the 
minimum order of a Butterworth approximation. Used during Circuit Synthesis at Universidade Federal da Bahia """

def extractK(n):
    # Generating the list to extract the odd and even numbers
    k = []
    for i in range(n+1):
        k.append(i)
    # Leaving 0 from the list
    k = k[1:n+1]

    even = []
    odd = []
    for num in k:
        if num % 2:
            odd.append(num)
        else:
            even.append(num)
    print("Even: ", even)
    print("Odd: ", odd)
    return odd, even

def calculateComponent(n, epslon, k_list):
    normalizedComponents = []
    for k in k_list:
        normalizedComponent = 2*epslon**(1/n)*sin((2*k-1)*pi/2*n)
        normalizedComponents.append(normalizedComponent)
    return normalizedComponents

def main():
    # TODO: Function to calculate epslon and n
    epslon = 0.1526
    n = 5
    odd, even = extractK(n)

    # For the capacitors
    capacitors = calculateComponent(n, epslon, odd)
    # For the inductors
    inductors = calculateComponent(n, epslon, even)

    print("Capacitors: C1, C3, C5...")
    print(capacitors)
    print("Inductors: L2, L4...")
    print(inductors)


main()
