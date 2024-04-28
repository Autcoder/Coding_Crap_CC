import java.util.*;

class listenAuswertung {
    public static void main(String[] args) {
        int[] liste = new int[20];
        int max = 0;
        int min = 0;
        double average = 0;
        int minDist = 0;

        for (int index = 0; index < liste.length; index++) {
            int randomNumber = (int) (Math.random() * 202) - 101;
            liste[index] = randomNumber;
        }

        System.out.println("Liste: " + Arrays.toString(liste));

        max = maximum(liste);
        min = minimum(liste);
        average = mittelwert(liste);
        minDist = minDist(liste);

        System.out.println("Max: " + max);
        System.out.println("Min: " + min);
        System.out.println("Mittelwert: " + average);
        System.out.println("Mindestabstand: " + minDist);

    }

    private static int minDist(int[] liste) {
        int minDist = Integer.MAX_VALUE;
        for (int i = 0; i < liste.length; i++) {
            for (int j = i + 1; j < liste.length; j++) {
                int difference = Math.abs(liste[i] - liste[j]);
                minDist = Math.min(minDist, difference);
            }
        }
        return minDist;
    }

    private static double mittelwert(int[] liste) {
        double average = 0;
        for (int i = 0; i < liste.length; i++) {
            average += liste[i];
        }
        average = average / liste.length;
        return average;
    }

    private static int minimum(int[] liste) {
        int minimum = liste[0];
        for (int i = 0; i < liste.length; i++) {
            if (liste[i] < minimum) {
                minimum = liste[i];
            }
        }
        return minimum;
    }

    private static int maximum(int[] liste) {
        int maximum = liste[0];
        for (int i = 0; i < liste.length; i++) {
            if (liste[i] > maximum) {
                maximum = liste[i];
            }
        }
        return maximum;
    }
}