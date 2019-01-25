package com.example.mediekontroll;

import android.content.Context;
import android.util.Log;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;

public class MottaData extends Thread {
    private String ip;
    private int port;
    private static ServerSocket serverSocket;
    private Context main;

    //Variabler brukt for å vise sanginfo
    private String hostnavn = "";
    private Sang sang = new Sang("", "", "", "");
    private boolean spiller = false;
    private String repeat = "";
    private String shuffle = "";
    private SangTid tid = new SangTid(0,0);

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
        Log.v("Medie_Mottat_Full", "Mottat melding: " + str);
        String[] kommandoer = str.split("\\|");
        for (String kommando : kommandoer ) {
            String[] ord = kommando.split(";;");
            if (ord[0].equals("host")) {
                hostnavn = ord[1];
                Log.v("Medie_Mottat", "Mottat kommando " + ord[0] + ": '" + ord[1] + "'");
            } else if (ord[0].equals("playing")) {
                spiller = ((Integer.parseInt(ord[1])) == 1);
                Log.v("Medie_Mottat", "Mottat kommando " + ord[0] + ": '" + ord[1] + "'");
            } else if (ord[0].equals("repeat")) {
                repeat = ord[1];
                Log.v("Medie_Mottat", "Mottat kommando " + ord[0] + ": '" + ord[1] + "'");
            } else if (ord[0].equals("shuffle")) {
                shuffle = ord[1];
                Log.v("Medie_Mottat", "Mottat kommando " + ord[0] + ": '" + ord[1] + "'");
            } else if (ord[0].equals("song")) {
                String[] sangVar = ord[1].split(";");
                sang.setTittel(sangVar[0]);
                sang.setArtist(sangVar[1]);
                sang.setAlbum(sangVar[2]);
                sang.setAlbumBilde(sangVar[3]);
                Log.v("Medie_Mottat", "Mottat kommando " + ord[0] + ": '" + ord[1] + "'");
            } else if (ord[0].equals("time")) {
                String[] tidVar = ord[1].split(";");
                tid.setCurrent(Integer.parseInt(tidVar[0]));
                tid.setTotal(Integer.parseInt(tidVar[1]));
                Log.v("Medie_Mottat", "Mottat kommando " + ord[0] + ": '" + ord[1] + "'");
            } else {
                Log.e("Medie_Mottat", "Mottat ukjent kommando: '" + kommando + "'");
            }
        }
    }

    //https://medium.com/google-developer-experts/on-properly-using-volatile-and-synchronized-702fc05faac2
    synchronized String getHostnavn() {
        return hostnavn;
    }
    synchronized Sang getSang() {
        return sang;
    }
    synchronized boolean getSpiller() {
        return spiller;
    }
    synchronized SangTid getSangTid() {
        return tid;
    }
}