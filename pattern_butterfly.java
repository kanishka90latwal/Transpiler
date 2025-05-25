public class ButterflyPattern {
    public static void main(String[] args) {
        // Number of rows
        int N = 5;

        // Variables to store number of spaces and stars
        int spaces = 2 * N - 1;
        int stars = 0;

        // The outer loop will run for (2 * N - 1) times
        for (int i = 1; i <= 2 * N - 1; i++) {
            // Upper half of the butterfly
            if (i <= N) {
                spaces = spaces - 2;
                stars++;
            }
            // Lower half of the butterfly
            else {
                spaces = spaces + 2;
                stars--;
            }
            // Print stars
            for (int j = 1; j <= stars; j++) {
                System.out.print("*");
            }
            // Print spaces
            for (int j = 1; j <= spaces; j++) {
                System.out.print(" ");
            }
            // Print stars
            for (int j = 1; j <= stars; j++) {
                if (j != N) {
                    System.out.print("*");
                }
            }
            System.out.println();
        }
    }
}
//this code is contributed by Adarsh
