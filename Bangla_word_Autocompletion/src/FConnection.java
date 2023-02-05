import java.io.*;
import java.net.URL;
import java.awt.*;
import java.util.*;  


public class FConnection{

    public FConnection()
    {
        System.out.print("");
    }
    public String task(String st){
        try {
                Driver driver = new Driver();
                return driver.display_values(st);
        }
        catch (IOException e) {
                e.printStackTrace();
                return "";
        }
    }
}