public class Bubble {
    public static void main(String[] args) {
        String nEnv = System.getenv("SORT_SIZE");
        int N = 10000;
        if (nEnv != null) {
            try { N = Integer.parseInt(nEnv); } catch (Exception e) {}
        }

        double[] arr = new double[N];
        // Use long to simulate unsigned 32-bit math correctly
        long seed = 42; 
        
        for (int i = 0; i < N; i++) {
            seed = (seed * 1664525 + 1013904223) & 0xFFFFFFFFL;
            arr[i] = (double)seed / 4294967296.0;
        }

        long start = System.nanoTime();
        for (int i = 0; i < N - 1; i++) {
            for (int j = 0; j < N - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    double temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
        long end = System.nanoTime();

        System.out.printf("Sort(%d): ", N);
        for(int i=0; i<5; i++) System.out.printf("%.4f ", arr[i]);
        System.out.print("... ");
        for(int i=N-5; i<N; i++) System.out.printf("%.4f ", arr[i]);
        System.out.println();

        System.out.printf("Time: %.3f ms%n", (end - start) / 1_000_000.0);
    }
}
