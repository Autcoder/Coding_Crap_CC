import math

def addition():
    print("Addition")
    a = int(input("Zahl 1: "))
    b = int(input("Zahl 2: "))
    final = a + b
    print(a, "+", b, "=", a + b)
    return int(final)


def subtraktion():
    print("Subtraktion")
    a = int(input("Zahl 1: "))
    b = int(input("Zahl 2: "))
    final = a - b
    print(a, "-", b, "=", a - b)
    return int(final)


def multiplikation():
    print("Multiplikation")
    a = int(input("Zahl 1: "))
    b = int(input("Zahl 2: "))
    final = a * b
    print(a, "*", b, "=", a * b)
    return int(final)


def division():
    print("Division")
    a = int(input("Zahl 1: "))
    b = int(input("Zahl 2: "))
    final = a / b
    print(a, "/", b, "=", a / b)
    return int(final)


def quadratwurzel():
    print("Quadratwurzel")
    a = int(input("Zahl: "))
    final = a**0.5
    print("Wurzel von", a, "=", a**0.5)
    return int(final)


def quadrat():
    print("Quadrat")
    a = int(input("Zahl: "))
    final = a**2
    print("Quadrat von", a, "=", a**2)
    return int(final)


def potenz():
    print("Potenz")
    a = int(input("Zahl: "))
    b = int(input("Potenz: "))
    final = a**b
    print(a, "^", b, "=", a**b)
    return int(final)


def logarithmus():
    print("Logarithmus")
    a = int(input("Zahl: "))
    final = math.log(a)
    print("Logarithmus von", a, "=", math.log(a))
    return int(final)


def sinus():
    print("Sinus")
    a = int(input("Zahl: "))
    final = math.sin(a)
    print("Sinus von", a, "=", math.sin(a))
    return int(final)


def cosinus():
    print("Cosinus")
    a = int(input("Zahl: "))
    final = math.cos(a)
    print("Cosinus von", a, "=", math.cos(a))
    return int(final)


def tangens():
    print("Tangens")
    a = int(input("Zahl: "))
    final = math.tan(a)
    print("Tangens von", a, "=", math.tan(a))
    return int(final)


def main():
    while True:
        print()
        print("Type help for more information")
        method = input()

        if method == "a":
            addition()
        elif method == "s":
            subtraktion()
        elif method == "m":
            multiplikation()
        elif method == "d":
            division()
        elif method == "qw":
            quadratwurzel()
        elif method == "q":
            quadrat()
        elif method == "p":
            potenz()
        elif method == "log":
            logarithmus()
        elif method == "sin":
            sinus()
        elif method == "cos":
            cosinus()
        elif method == "tan":
            tangens()
        elif method == "help":
            help()
        elif method == "exit":
            break
    results.append(int(final))

def help():
    print("a = Addition")
    print("s = Subtraktion")
    print("m = Multiplikation")
    print("d = Division")
    print("qw = Quadratwurzel")
    print("q = Quadrat")
    print("p = Potenz")
    print("log = Logarithmus")
    print("sin = Sinus")
    print("cos = Cosinus")
    print("tan = Tangens")
    print("exit = Exit")
    print("To execute an operation, type the letter of the operation standing in front of it.")
    print("For example: ")
    print("To execute Addition type -a-")


results = [0]
results.pop(0)
final = 0

print("This is a simple calculator")
print("Type help for more information")
print("Press Enter to start")
start = input()

if start == "help":
    help()
else:
    pass

if __name__ == "__main__":
    main()

print("The results are:")
print(results)