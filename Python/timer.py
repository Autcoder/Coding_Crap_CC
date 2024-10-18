import time

timerstring = input("Enter the timer in format [HH:MM:SS]:  ")
timer = timerstring.split(":")

hours = int(timer[0])
minutes = int(timer[1])
seconds = int(timer[2])

allSeconds = hours * 3600 + minutes * 60 + seconds

endTime = time.strftime("%H:%M:%S", time.localtime(time.time() + allSeconds))
print("\n" + f"Timer will end at {endTime}" + "\n")

while True:
    allSeconds = allSeconds - 1
    hours = allSeconds // 3600
    minutes = (allSeconds % 3600) // 60
    seconds = (allSeconds % 3600) % 60
    
    if hours > 0:
        print(f"\r{hours:02d}:{minutes:02d}:{seconds:02d}", end="")
    elif minutes > 0:
        print(f"\r{minutes:02d}:{seconds:02d}", end="")
    else:
        print(f"\r{seconds:02d}", end="")
        
    if hours == 0 and minutes == 0 and seconds == 0:
        print("\rTime is up!")
        break
    time.sleep(1)