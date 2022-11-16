import random


def calc(people):

    uniqueYears = 0
    times = 100000
    for i in range(times): 
        days = []
        for i in range(people):
            days.append(random.randint(1, 365))

        if(len(set(days)) == len(days)):
            uniqueYears += 1
    return 1 - uniqueYears / times

for i in range(365):
    print(str(i) + ": " + str(calc(i)))