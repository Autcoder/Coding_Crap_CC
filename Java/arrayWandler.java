import java.util.*;

class arrayWandler {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            try (Scanner search = new Scanner(System.in)) {
                int[] array = new int[5];

                // Input
                for (int i = 0; i < array.length; i++) {
                    System.out.print("Put in the " + (i + 1) + " value: ");
                    int value = sc.nextInt();
                    array[i] = value;
                }

                // Output Normal Array
                System.out.println("Normal Array: " + Arrays.toString(array));

                // Reversed Array
                int[] reversedArray = new int[array.length];
                for (int i = 0; i < array.length; i++) {
                    reversedArray[i] = array[array.length - 1 - i];
                }
                System.out.println("Reversed Array: " + Arrays.toString(reversedArray));

                // Sorted Array
                Arrays.sort(array);
                System.out.println("Sorted Array: " + Arrays.toString(array));

                // Min and Max of the Array
                int min = array[0];
                int max = array[array.length - 1];
                System.out.println("Min Value: " + min);
                System.out.println("Max Value: " + max);

                // Average of the Array
                int sum = 0;
                for (int i = 0; i < array.length; i++) {
                    sum += array[i];
                }
                float average = (float) sum / array.length;
                System.out.println("Average: " + average);

                // Look for a value in the Array
                System.out.print("Type the value you want to search for: ");
                int searchValue = search.nextInt();
                boolean found = false;
                int index = 0;
                for (int i = 0; i < array.length; i++) {
                    index++;
                    if (array[i] == searchValue) {
                        found = true;
                        break;
                    }
                }
                if (found == true) {
                    System.out.println("The value " + searchValue + " is present in the array. Its index is: " + index);
                } else {
                    System.out.println("The value " + searchValue + " is not present in the array.");
                }

                // Replace a value in the Array with another value
                System.out.print("Type the value you want to replace: ");
                int replaced = search.nextInt();
                System.out.print("Type the value it should be replaced with: ");
                int newValue = search.nextInt();

                for (int i = 0; i < array.length; i++) {
                    if (array[i] == replaced) {
                        array[i] = newValue;
                    }
                }
                System.out.println("The new array is: " + Arrays.toString(array));
            }
        }
    }
}
