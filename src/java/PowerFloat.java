public class PowerFloat {
    public static void main(String[] args) {
        String baseEnv = System.getenv("BASE");
        String expEnv = System.getenv("EXP");
        
        double base = 2.0;
        int exp = 1023;
        
        if (baseEnv != null) base = Double.parseDouble(baseEnv);
        if (expEnv != null) exp = Integer.parseInt(expEnv);

        long start = System.nanoTime();
        double result = Math.pow(base, exp);
        long end = System.nanoTime();

        System.out.printf("Result(%.2f^%d): %.10e%n", base, exp, result);
        System.out.printf("Time: %.3f ms%n", (end - start) / 1_000_000.0);
    }
}
