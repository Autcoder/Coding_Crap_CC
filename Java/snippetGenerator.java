import java.util.*;
import java.math.*;
import java.io.*;

class Snippetgenerator {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            int sum = 0;
            int index = 0;

            for (int i = 0; i < 10; i++) {
                sum = sum + 4;
            }

            for (int i = 0; i < 10; i++) {
                if (sum > 10) {
                    index = i;
                }
            }

            System.out.println("Sum: " + sum + "\nIndex: " + index);

            String[] array = { "1", "2", "3", "4", "5" };
        }
    }
}