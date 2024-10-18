import random
import sys

def get_difficulty_range():
    print("Wählen Sie einen Schwierigkeitsgrad:")
    print("1. Einfach (1-100)")
    print("2. Mittel (1-1000)")
    print("3. Schwer (1-10000)")
    print("4. Extrem (1-1000000)")

    while True:
        choice = input("Ihre Wahl (1-4): ")

        if choice == "1":
            return 1, 100
        elif choice == "2":
            return 1, 1000
        elif choice == "3":
            return 1, 10000
        elif choice == "4":
            return 1, 1000000
        else:
            print("Bitte wählen Sie eine gültige Option (1-4).")

def main():
    min_num, max_num = get_difficulty_range()
    number_to_guess = random.randint(min_num, max_num)
    attempts = 0

    print(f"Willkommen bei Zahlenraten! Erraten Sie die Zahl zwischen {min_num} und {max_num}!")
    print("Sie können jederzeit \"exit\" eingeben, um das Programm zu beenden!")

    while True:
        guess = input(f"Rate eine Zahl von {min_num}-{max_num}: ")

        if guess.lower() == "exit":
            sys.exit(0)

        try:
            guess = int(guess)
            if not min_num <= guess <= max_num:
                print(f"Die Zahl muss zwischen {min_num} und {max_num} liegen.")
                continue

            attempts += 1

            if guess < number_to_guess:
                print("Die gesuchte Zahl ist höher.")
            elif guess > number_to_guess:
                print("Die gesuchte Zahl ist niedriger.")
            else:
                print(f"\nGlückwunsch! Sie haben die Zahl erraten!")
                print(f"Sie haben {attempts} Versuche gebraucht!")
                break

        except ValueError:
            print("Bitte geben Sie eine gültige Zahl ein!")

if __name__ == "__main__":
    main()
