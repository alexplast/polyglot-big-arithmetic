import java.math.BigInteger;

public class Power {
    public static void main(String[] args) {
        String baseEnv = System.getenv("BASE");
        String expEnv = System.getenv("EXP");
        
        int base = 2;
        int exp = 1000;
        
        if (baseEnv != null) {
            try {
                base = Integer.parseInt(baseEnv);
            } catch (NumberFormatException e) {
                // Keep default
            }
        }
        
        if (expEnv != null) {
            try {
                exp = Integer.parseInt(expEnv);
            } catch (NumberFormatException e) {
                // Keep default
            }
        }

        BigInteger bigBase = BigInteger.valueOf(base);

        long start = System.nanoTime();
        BigInteger result = bigBase.pow(exp);
        long end = System.nanoTime();
        double durationMs = (end - start) / 1_000_000.0;

        System.out.println("Result(" + base + "^" + exp + "): " + result);
        System.out.printf("Time: %.3f ms%n", durationMs);
    }
}
