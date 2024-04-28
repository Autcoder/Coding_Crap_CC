import java.util.Scanner;

class umwandler {

    public static void main(String[] args) {
        try (Scanner input = new Scanner(System.in)) {
            try (Scanner answer = new Scanner(System.in);) {
                boolean done = false;
                float[] Results = new float[50];
                int i = 0;
                float result = 0.0f;

                do {
                    System.out.print("Put in a value: ");
                    float value = input.nextFloat();

                    System.out.println("What convertion do you want to do?");
                    System.out.println("c-k = Celsius to Kelvin");
                    System.out.println("k-c = Kelvin to Celsius");
                    System.out.println("c-f = Celsius to Fahrenheit");
                    System.out.println("f-c = Fahrenheit to Celsius");
                    System.out.println("m-ml = Meter to Meile");
                    System.out.println("ml-m = Meile to Meter");
                    System.out.println("i-f = Inch to Foot");
                    System.out.println("f-i = Foot to Inch");
                    System.out.println("Just type in the two letters of the convertion (for example ck).");
                    String convertion = input.next();

                    switch (convertion) {
                        case "ck":
                            System.out.println("Celsius to Kelvin: " + (value + 273.15));
                            result = (float) (value + 273.15);
                            break;
                        case "kc":
                            System.out.println("Kelvin to Celsius: " + (value - 273.15));
                            result = (float) (value - 273.15);
                            break;
                        case "cf":
                            System.out.println("Celsius to Fahrenheit: " + ((value * 1.8) + 32));
                            result = (float) ((value * 1.8) + 32);
                            break;
                        case "fc":
                            System.out.println("Fahrenheit to Celsius: " + ((value - 32) / 1.8));
                            result = (float) ((value - 32) / 1.8);
                            break;
                        case "mml":
                            System.out.println("Meter to Meile: " + (value / 1609.344));
                            result = (float) (value / 1609.344);
                            break;
                        case "mlm":
                            System.out.println("Meile to Meter: " + (value * 1609.344));
                            result = (float) (value / 1609.344);
                            break;
                        case "if":
                            System.out.println("Inch to Foot: " + (value / 12));
                            result = (float) (value / 12);
                            break;
                        case "fi":
                            System.out.println("Foot to Inch: " + (value * 12));
                            result = (float) (value * 12);
                            break;
                    }

                    Results[i] = result;
                    i++;

                    System.out.println("Do you want to do another convertion?");
                    System.out.println("Yes or No?");
                    String answerString = answer.nextLine();
                    if (answerString.equals("No") || answerString.equals("no")) {
                        done = true;
                    }
                } while (done == false);

                System.out.println("Here are your Results: ");
                for (int j = 0; j < i; j++) {
                    System.out.println(Results[j]);
                }
            }
        }
    }
}
