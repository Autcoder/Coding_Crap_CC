
temps = [0]
sum = 0
u30 = 0
u4 = 0
middletemps = 0

print("Please enter the temperatures one by one!")

for x in range(7):
    value = input("Temperature: ")
    temps.append(value)

temps.pop(0)

for x in temps:
    sum = sum + int(x)

average = sum / len(temps)

for x in temps:
    if int(x) > 30:
        u30 = u30 + 1
    if int(x) < 4:
        u4 = u4 + 1
    else:
        middletemps = middletemps + 1
        

print("Here is the collected data:")
print("The temperatures in the past week were: " + str(temps))
print("The average temperature was: " + str(average))
print("The number of temperatures above 30 was: " + str(u30))
print("The number of temperatures under 4 was: " + str(u4))
print("The number of temperatures between 4 and 30 was: " + str(middletemps))