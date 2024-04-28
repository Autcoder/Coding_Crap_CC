
arr = [0]
sum = 0

for x in range(5):
    value = input("Value: ")
    arr.append(int(value))

arr.pop(0)

print("Normal Array: " + str(arr))

arr.reverse()
print("Reversed Array: " + str(arr))

arr.sort()
print("Sorted Array: " + str(arr))

min = arr[0]
max = arr[4]
print("Min: " + str(min))
print("Max: " + str(max))

for x in arr:
    sum = sum + int(x)

average = sum / len(arr)
print("Average:", average)

print("What value do you want to search for?")
search = int(input())

if search in arr:
    print("Found")
    print("Index of value: " + str(arr.index(search)))
else:
    print("Not Found")

print("What value do you want to replace?")
replace = int(input())

print("What value do you want to replace it with?")
replaceWith = int(input())

arr[arr.index(replace)] = replaceWith
print("New Array: " + str(arr))