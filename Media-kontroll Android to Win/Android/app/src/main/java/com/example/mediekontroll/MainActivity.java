package com.example.mediekontroll;

import android.os.Bundle;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.util.Timer;
import java.util.TimerTask;


public class MainActivity extends AppCompatActivity {
    String ip ="192.168.1.3";
    int sPort = 49433;
    int mPort = 49434;
    MottaData serverThread;
    final Handler myHandler = new Handler();

    //Variabler brukt for å vise sanginfo
    private String hostnavn = "";
    private boolean endretHostnavn = false;
    private Sang sang = new Sang("", "", "", "");
    private boolean endretSangnavn = false;
    private boolean spiller = false;
    private boolean endretSpiller = false;
    private SangTid tid = new SangTid(0,0);
    private boolean endretTid = false;

    //Gui-elementer
    TextView hostView;
    Button playPauseView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        synchronized(SharedData_Motta_Main.globalInstance) {
            hostnavn = SharedData_Motta_Main.globalInstance.hostnavn;
            endretHostnavn = SharedData_Motta_Main.globalInstance.endretHostnavn;
            sang = SharedData_Motta_Main.globalInstance.sang;
            endretSangnavn = SharedData_Motta_Main.globalInstance.endretSangnavn;
            spiller = SharedData_Motta_Main.globalInstance.spiller;
            endretSpiller = SharedData_Motta_Main.globalInstance.endretSpiller;
            tid = SharedData_Motta_Main.globalInstance.tid;
            endretTid = SharedData_Motta_Main.globalInstance.endretTid;
        }

        //Henter referanser til Gui-elementer
        hostView = (TextView) findViewById(R.id.txtHostnavn);
        playPauseView = (Button) findViewById(R.id.btn_play_pause);

        //Setter opp jevnlige oppdateringer av gui
        Timer myTimer = new Timer();
        myTimer.schedule(new TimerTask() {
            @Override
            public void run() {updateGui();}
        }, 0, 1000);

        //Starter å lytte på nettverket på oppgitt port
        serverThread = new MottaData(ip, mPort);
        serverThread.start();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        } else if (id == R.id.action_avslutt_server) {
            sendBeskjed("stopp");
            Toast.makeText(this, getString(R.string.server_avsluttet), Toast.LENGTH_SHORT).show();
        }

        return super.onOptionsItemSelected(item);
    }

    public void onBtnClick(View view) {
        if (view.getId() == R.id.btn_play_pause) {
            sendBeskjed("playPause");
        } else if (view.getId() == R.id.btn_forrige) {
            sendBeskjed("forrige");
        } else if (view.getId() == R.id.btn_neste) {
            sendBeskjed("neste");
        } else if (view.getId() == R.id.btn_volum_ned) {
            sendBeskjed("volumNed");
        } else if (view.getId() == R.id.btn_volum_opp) {
            sendBeskjed("volumOpp");
        }
    }

    private void sendBeskjed(String beskjed) {
        SendData t = new SendData(ip, sPort, beskjed);
        t.start();
    }

    private void updateGui() {
        myHandler.post(myRunnable);
    }

    final Runnable myRunnable = new Runnable() {
        public void run() {
            hostView.setText(hostnavn);
        }
    };
}

class Sang {
    private String tittel;
    private String artist;
    private String album;
    private String albumBilde;

    public Sang(String tittel, String artist, String album, String albumBilde) {
        this.tittel = tittel;
        this.artist = artist;
        this.album = album;
        this.albumBilde = albumBilde;
    }

    public void setTittel(String str) {
        this.tittel = str;
    }
    public void setArtist(String str) {
        this.artist = str;
    }
    public void setAlbum(String str) {
        this.album = str;
    }
    public void setAlbumBilde(String str) {
        this.albumBilde = str;
    }
}

class SangTid {
    private int current;
    private int total;

    public SangTid(int current, int total) {
        this.current = current;
        this.total = total;
    }
}