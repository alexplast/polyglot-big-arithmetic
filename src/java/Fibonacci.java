import java.math.BigInteger;

public class Fibonacci {
    public static void main(String[] args) {
        String countEnv = System.getenv("COUNT");
        int count = 10;
        if (countEnv != null) {
            try {
                count = Integer.parseInt(countEnv);
            } catch (NumberFormatException e) {
            }
        }

        BigInteger a = BigInteger.ZERO;
        BigInteger b = BigInteger.ONE;

        long start = System.nanoTime();
        for (int i = 0; i < count; i++) {
            BigInteger temp = a;
            a = b;
            b = b.add(temp);
        }
        long end = System.nanoTime();
        double durationMs = (end - start) / 1_000_000.0;

        System.out.println("Result(F_" + count + "): " + a);
        System.out.printf("Time: %.3f ms%n", durationMs);
    }
}
