package com.example.mediekontroll;

import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;


public class MainActivity extends AppCompatActivity {
    String ip ="192.168.1.3";
    int port = 49433;
    MottaData serverThread;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        FloatingActionButton fab = findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                sendBeskjed("stopp");
                Snackbar.make(view, "Stoppet", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            }
        });

        //Starter å lytte på nettverket på oppgitt port
        serverThread = new MottaData(ip, port);
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
        SendData t = new SendData(ip, port, beskjed);
        t.start();
    }
}
