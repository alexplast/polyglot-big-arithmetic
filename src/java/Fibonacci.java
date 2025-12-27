import java.math.BigInteger;

public class Fibonacci {
    public static void main(String[] args) {
        int n = 10; // Default value
        String countStr = System.getenv("COUNT");
        if (countStr != null) {
            try {
                n = Integer.parseInt(countStr);
            } catch (NumberFormatException e) {
                System.err.println("Error converting COUNT environment variable: " + e.getMessage());
            }
        }

        System.out.println("Fibonacci Sequence (first " + n + " numbers):");

        BigInteger a = BigInteger.ZERO;
        BigInteger b = BigInteger.ONE;
        for (int i = 0; i < n; i++) {
            System.out.print(a + " ");
            BigInteger temp = a;
            a = b;
            b = temp.add(b);
        }
        System.out.println();
    }
}
