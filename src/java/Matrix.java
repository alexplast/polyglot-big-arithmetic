public class Matrix {
    public static void main(String[] args) {
        String nEnv = System.getenv("MATRIX_SIZE");
        int N = 256;
        if (nEnv != null) {
            try { N = Integer.parseInt(nEnv); } catch (Exception e) {}
        }

        double[] A = new double[N * N];
        double[] B = new double[N * N];
        double[] C = new double[N * N];

        for (int i = 0; i < N * N; i++) {
            A[i] = 1.0 + (i % 100) * 0.01;
            B[i] = 1.0 - (i % 100) * 0.01;
        }

        long start = System.nanoTime();

        for (int i = 0; i < N; i++) {
            for (int k = 0; k < N; k++) {
                double r = A[i * N + k];
                for (int j = 0; j < N; j++) {
                    C[i * N + j] += r * B[k * N + j];
                }
            }
        }

        long end = System.nanoTime();

        System.out.println("Matrix(" + N + "x" + N + ")");
        System.out.println("Result[0]: " + C[0]);
        System.out.printf("Time: %.3f ms%n", (end - start) / 1_000_000.0);
    }
}
