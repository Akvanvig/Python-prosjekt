package com.example.mediekontroll;

import android.os.Handler;
import android.util.Log;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;

public class MottaData extends Thread {
    public Handler mHandler;
    private String ip;
    private int port;
    private static ServerSocket serverSocket;

    public MottaData(String ip, int port) {
        this.ip = ip;
        this.port = port;
    }

    @Override
    public void run() {
        while (true) {
            try {
                serverSocket = new ServerSocket(port);
            } catch (IOException ioe) {
                System.out.println("Kunne ikke lytte på " + port);
                System.exit(-1);
            }
            while (true) {
                String str = "";
                try {
                    Socket socket = serverSocket.accept();
                    BufferedReader br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                    str = br.readLine();
                    socket.close();
                } catch (IOException ioe) {
                    System.out.println(ioe.toString());
                }
                tolkSignal(str);
            }
        }
    }

    private void tolkSignal(String str) {
        String[] kommandoer = str.split("|");
        for (String kommando : kommandoer ) {
            String[] ord = kommando.split(";;");
            if (ord[0].equals("host")) {
                Log.e("Medie_Mottat", "Mottat kommando " + ord[0] + ": '" + ord[1] + "'");
            } else if (ord[0].equals("sangnavn")) {
                Log.e("Medie_Mottat", "Mottat kommando " + ord[0] + ": '" + ord[1] + "'");
            } else {
                Log.e("Medie_Mottat", "Mottat ukjent kommando: '" + kommando + "'");
            }
        }
    }
}
