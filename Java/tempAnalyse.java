import java.util.*;

public class tempAnalyse {
    public static void main(String[] args) {
        try (Scanner temp = new Scanner(System.in)) {
            int[] temps = new int[7];
            int min=temps[0];
            int max=temps[0];
            int u30=0;
            int u4=0;

            for (int i = 0; i < temps.length; i++) {
                System.out.print("Put in the " + (i+1) + " value: ");
                int value = temp.nextInt();
                temps[i] = value;
            }

            int sum = 0;
            for (int i = 0; i < temps.length; i++) {
                sum += temps[i];
            }
            int average = sum / temps.length;
            
            for(int j=0; j<temps.length; j++){

                if (temps[j]>max) {
                    max = temps[j];
                }
                if (temps[j]<min) {
                    min=temps[j];
                }
                if (temps[j]>30) {
                    u30++;                    
                }
                if (temps[j]<4) {
                    u4++;                    
                }
            }
            
            System.out.println("Here is the collected data:");
            System.out.println("The temperatures in the last seven days were " + Arrays.toString(temps) + ".");
            System.out.println("Average temperatur in the last 7 days was " + average + "°C.");
            System.out.println("It was hotter than 30°C on " + u30 + " days.");
            System.out.println("It was colder than 4°C on " + u4 + " days");
        }
    }
}
