public class FactorialFloat {
    public static void main(String[] args) {
        String countEnv = System.getenv("COUNT");
        int count = 170;
        if (countEnv != null) {
            try {
                count = Integer.parseInt(countEnv);
            } catch (NumberFormatException e) {}
        }

        double factorial = 1.0;

        long start = System.nanoTime();
        for (int i = 1; i <= count; i++) {
            factorial *= i;
        }
        long end = System.nanoTime();

        System.out.printf("Result(%d!): %.10e%n", count, factorial);
        System.out.printf("Time: %.3f ms%n", (end - start) / 1_000_000.0);
    }
}
