from random import random

value = int(random() * 6) + 1

print("Guess a number between 1 and 6!")

guess = int(input())

if guess > 0 and guess < 7:
    if guess == value:
        print("You guessed right!")
    else:
        print("You guessed wrong!")
        guess = int(input())

print("You won!")
