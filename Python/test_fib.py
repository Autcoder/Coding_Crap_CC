import time

def fibonacci_generator():
    current, previous = 0, 1
    while True:
        yield current
        current, previous = previous, current + previous

def measure_time(numbers: int) -> tuple[float, float]:
    times = []
    for _ in range(100):
        start_time = time.time_ns()
        generator = fibonacci_generator()
        for _ in range(numbers):
            try:
                next(generator)
            except ValueError:
                break
            except StopIteration:
                break
        end_time = time.time_ns()
        times.append(end_time - start_time)
    times.sort()
    avg_time = sum(times) / len(times)
    median_time = times[len(times) // 2]
    return avg_time, median_time

if __name__ == "__main__":
    while True:
        numbers = input("\nHow many numbers: ")
        if numbers.lower() in ['exit', 'quit']:
            break
        try:
            numbers = int(numbers)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if numbers <= 0:
            print("Invalid input. Please enter a positive number.")
        else:
            avg_time, median_time = measure_time(numbers)
            print(f"Average time taken: {avg_time} nanoseconds")
            print(f"Median time taken: {median_time} nanoseconds")