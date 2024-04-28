import java.util.Scanner;

class würfelRaten {
    public static void main(String[] args) {
        try (Scanner scanner = new Scanner(System.in)) {
            int value = ((int) (Math.random()*(7 - 1))) + 1;

            // Guess the number
            System.out.println("Guess a number betweeen 1 and 6!");
            int guess = scanner.nextInt();

            // Check if the guess is correct
            while (guess != value) {
                if (guess > 0 && guess < 7) System.out.println("Wrong! Try again!");
                if (guess < 1 || guess > 6) System.out.println("Systemoutofboundsexception");
                guess = scanner.nextInt();
            }

            // The Player won
            System.out.println("Correct!");
        }
    }
}