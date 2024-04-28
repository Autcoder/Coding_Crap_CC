import java.util.Random;

public class random {
    public static void main(String[] args) {
        // Create a Random object
        Random random = new Random();

        // Generate a random number between -100 and 100
        int randomNumber = random.nextInt(201) - 100;

        // Print the random number
        System.out.println("Random number between -100 and 100: " + randomNumber);
    }
}