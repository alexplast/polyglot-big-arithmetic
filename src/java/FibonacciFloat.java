public class FibonacciFloat {
    public static void main(String[] args) {
        String countEnv = System.getenv("COUNT");
        int count = 1475;
        if (countEnv != null) {
            try { count = Integer.parseInt(countEnv); } catch (Exception e) {}
        }

        double a = 0.0, b = 1.0;

        long start = System.nanoTime();
        for(int k=0; k<200000; k++) {
            a = 0.0; b = 1.0;
            for (int i = 0; i < count; i++) {
                double temp = a;
                a = b;
                b = temp + b;
            }
        }
        long end = System.nanoTime();

        System.out.println("Result: " + a);
        System.out.printf("Time: %.3f ms%n", (end - start) / 1_000_000.0);
    }
}
