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

        for (int i = 0; i < count; i++) {
            BigInteger temp = a;
            a = b;
            b = b.add(temp);
        }
        System.out.println("Result(F_" + count + "): " + a);
    }
}
