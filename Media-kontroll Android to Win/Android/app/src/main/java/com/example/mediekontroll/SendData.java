package com.example.mediekontroll;

import android.util.Log;

import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;

public class SendData extends Thread{
    int port;
    String ip;
    String beskjed;
    public SendData(String ip, int port, String beskjed) {
        this.ip = ip;
        this.port = port;
        this.beskjed = beskjed;
    }

    @Override
    public void run() {
        try {
            Socket socket = new Socket(ip, port);
            OutputStream os = socket.getOutputStream();
            PrintWriter pw = new PrintWriter(os, true);
            pw.println(beskjed);
            pw.close();
            socket.close();
            Log.v("Medie_Annet", "Sendt beskjed: " + ip + ":" + port + " - " + beskjed);
        } catch (IOException ioe) {
            Log.e("Medie_IO", ioe.toString());
        } catch (Exception ex) {
            Log.e("Medie_Annet", ex.toString());
        } finally {

        }
    }
}
