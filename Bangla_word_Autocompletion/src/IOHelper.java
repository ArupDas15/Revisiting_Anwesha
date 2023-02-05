import java.io.*;

public class IOHelper {
    public static BufferedReader getBufferedReader(String file, int bufferSize) throws IOException {
        FileInputStream fis = new FileInputStream(file);
        InputStreamReader isr = new InputStreamReader(fis, "utf-8");
        BufferedReader br = new BufferedReader(isr, bufferSize);
        return br;
    }
    public static BufferedWriter getBufferedWriter(String file, int bufferSize) throws IOException {
        FileOutputStream fos = new FileOutputStream(file);
        OutputStreamWriter osw = new OutputStreamWriter(fos, "utf-8");
        BufferedWriter bw = new BufferedWriter(osw, bufferSize);
        return bw;
    }
    public static BufferedReader getBufferedReader(String file) throws IOException {
        FileInputStream fis = new FileInputStream(file);
        InputStreamReader isr = new InputStreamReader(fis, "utf-8");
        BufferedReader br = new BufferedReader(isr);
        return br;
    }
    public static BufferedWriter getBufferedWriter(String file) throws IOException {
        FileOutputStream fos = new FileOutputStream(file);
        OutputStreamWriter osw = new OutputStreamWriter(fos, "utf-8");
        BufferedWriter bw = new BufferedWriter(osw);
        return bw;
    }
}
