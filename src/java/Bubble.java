import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.file.Files;
import java.nio.file.Paths;

public class Bubble {
    public static void main(String[] args) {
        String nEnv = System.getenv("SORT_SIZE");
        int N = 10000;
        if (nEnv != null) {
            try { N = Integer.parseInt(nEnv); } catch (Exception e) {}
        }

        double[] arr = new double[N];
        
        try {
            byte[] bytes = Files.readAllBytes(Paths.get("data.bin"));
            // Ensure we don't read past the file or array bounds
            int limit = Math.min(N, bytes.length / 8);
            if (limit < N) {
                System.err.println("Warning: data.bin smaller than SORT_SIZE");
            }

            ByteBuffer buffer = ByteBuffer.wrap(bytes);
            buffer.order(ByteOrder.LITTLE_ENDIAN); // Python struct.pack uses little endian

            for (int i = 0; i < limit; i++) {
                arr[i] = buffer.getDouble();
            }
        } catch (IOException e) {
            System.err.println("Error: 'data.bin' not found. Run 'python3 tests/gen_data.py' first.");
            System.exit(1);
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
        int printLimit = (N < 5) ? N : 5;
        for(int i=0; i<printLimit; i++) System.out.printf("%.4f ", arr[i]);
        System.out.print("... ");
        if (N > 5) {
            for(int i=N-5; i<N; i++) System.out.printf("%.4f ", arr[i]);
        }
        System.out.println();

        System.out.printf("Time: %.3f ms%n", (end - start) / 1_000_000.0);
    }
}
