
results = [0]
results.pop(0)
i = 0
answer = "y"

while answer == "y":
    i = i + 1
    print("Please enter a number")
    value = int(input())
    print("What convertion do you want to do?")
    print("Type help for more information")
    convertion = input()
    if convertion == "help":
        print("c-k = Celsius to Kelvin")
        print("k-c = Kelvin to Celsius")
        print("c-f = Celsius to Fahrenheit")
        print("f-c = Fahrenheit to Celsius")
        print("m-ml = Meile to Meter")
        print("ml-m = Meter to Meile")
        print("i-f = Inch to Foot")
        print("f-i = Foot to Inch")
        print("Type the two letters without the ""-"".")
        print("For example: ck")
        continue
    elif convertion == "ck":
        print(value, "Celsius is", value + 273.15, "Kelvin")
        results.append(int(value + 273.15))
    elif convertion == "kc":
        print(value, "Kelvin is", value - 273.15, "Celsius")
        results.append(int(value - 273.15))
    elif convertion == "cf":
        print(value, "Celsius is", value * 1.8 + 32, "Fahrenheit")
        results.append(int(value * 1.8 + 32))
    elif convertion == "fc":
        print(value, "Fahrenheit is", (value - 32) / 1.8, "Celsius")
        results.append(int((value - 32) / 1.8))
    elif convertion == "mml":
        print(value, "Meter is", value * 1000, "Millimeter")
        results.append(int(value * 1000))
    elif convertion == "mlm":
        print(value, "Millimeter is", value / 1000, "Meter")
        results.append(int(value / 1000))
    elif convertion == "if":
        print(value, "Inch is", value * 12, "Foot")
        results.append(int(value * 12))
    elif convertion == "fi":
        print(value, "Foot is", value / 12, "Inch")
        results.append(int(value / 12))
    else:
        print("Error")
    print("Do you want to do another convertion?")
    print("y = yes")
    print("n = no")
    answer = input()
    if answer == "y":
        continue
    elif answer == "n":
        break

print("The results are:")
print(results)