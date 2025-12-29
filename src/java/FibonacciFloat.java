public class FibonacciFloat {
    public static void main(String[] args) {
        String countEnv = System.getenv("COUNT");
        int count = 1475;
        if (countEnv != null) {
            try {
                count = Integer.parseInt(countEnv);
            } catch (NumberFormatException e) {}
        }

        double a = 0.0;
        double b = 1.0;

        long start = System.nanoTime();
        for (int i = 0; i < count; i++) {
            double temp = a;
            a = b;
            b = temp + b;
        }
        long end = System.nanoTime();

        System.out.printf("Result(F_%d): %.10e%n", count, a);
        System.out.printf("Time: %.3f ms%n", (end - start) / 1_000_000.0);
    }
}
