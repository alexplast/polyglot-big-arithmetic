import java.math.BigInteger;

public class Factorial {
    public static void main(String[] args) {
        String countEnv = System.getenv("COUNT");
        int count = 200;
        if (countEnv != null) {
            try {
                count = Integer.parseInt(countEnv);
            } catch (NumberFormatException e) {
                // Keep default
            }
        }

        // System.out.println("Calculating Factorial(" + count + ")...");
        
        BigInteger factorial = BigInteger.ONE;

        long start = System.nanoTime();
        for (int i = 1; i <= count; i++) {
            factorial = factorial.multiply(BigInteger.valueOf(i));
        }
        long end = System.nanoTime();
        double durationMs = (end - start) / 1_000_000.0;

        System.out.println("Result(" + count + "!): " + factorial);
        System.out.printf("Time: %.3f ms%n", durationMs);
    }
}
