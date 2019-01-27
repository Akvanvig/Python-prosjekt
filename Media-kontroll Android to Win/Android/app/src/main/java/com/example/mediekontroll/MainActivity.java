package com.example.mediekontroll;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.net.URL;
import java.util.Timer;
import java.util.TimerTask;


public class MainActivity extends AppCompatActivity {
    String ip ="192.168.1.3";
    int sPort = 49433;
    int mPort = 49434;
    MottaData serverThread;

    //Gui-elementer
    TextView artistView;
    TextView sangView;
    Button playPauseView;
    ImageView albumView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        //Henter referanser til Gui-elementer
        artistView = (TextView) findViewById(R.id.txtArtist);
        sangView = (TextView) findViewById(R.id.txtSang);
        playPauseView = (Button) findViewById(R.id.btn_play_pause);
        albumView = (ImageView) findViewById(R.id.imgImageView);
        albumView.setAdjustViewBounds(true);
        albumView.setScaleType(ImageView.ScaleType.CENTER_CROP);

        //Starter å lytte på nettverket på oppgitt port
        serverThread = new MottaData(ip, mPort);
        serverThread.start();

        //Setter opp jevnlige oppdateringer av gui
        Timer myTimer = new Timer();
        myTimer.schedule(new TimerTask() {
            @Override
            public void run() {updateGui();}
        }, 0, 500);
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
        final String hostNavn = serverThread.getHostnavn();
        final Sang sang = serverThread.getSang();
        final SangTid tid = serverThread.getSangTid();
        final boolean spiller = serverThread.getSpiller();
        Bitmap bmpTemp =BitmapFactory.decodeResource(getResources(), R.drawable.yt_music_logo);
        try {
            String bilde = sang.getAlbumBilde().replace("=w60-h60", "=w800-h800"); //Endrer bildelink til å gi bedre oppløsning :)
            URL url = new URL(bilde);
            bmpTemp = BitmapFactory.decodeStream(url.openConnection().getInputStream());
        } catch (Exception ex) {
            Log.v("Medie_Albumbilde", ex.getMessage());
        }
        final Bitmap bmp = bmpTemp;


        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                //Alle oppdateringer til Gui-et må skje her
                setTitle(hostNavn);
                sangView.setText(sang.getTittel());
                artistView.setText(sang.getArtist());
                if (spiller && (playPauseView.getBackground() != getDrawable(R.drawable.ic_play_arrow_black_24dp))) {
                    playPauseView.setBackground(getDrawable(R.drawable.ic_pause_circle_filled_black_24dp));
                } else if (!spiller && (playPauseView.getBackground() != getDrawable(R.drawable.ic_pause_circle_filled_black_24dp))) {
                    playPauseView.setBackground(getDrawable(R.drawable.ic_play_arrow_black_24dp));
                }
                albumView.setImageBitmap(bmp);
            }
        });
    }

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
    public String getTittel() {
        return this.tittel;
    }
    public String getArtist() {
        return this.artist;
    }
    public String getAlbum() {
        return this.album;
    }
    public String getAlbumBilde() {
        return  this.albumBilde;
    }
}

class SangTid {
    private int current;
    private int total;

    public SangTid(int current, int total) {
        this.current = current;
        this.total = total;
    }
    public void setCurrent(int tid) {
        this.current = tid;
    }
    public void setTotal(int tid) {
        this.total = tid;
    }
    public int getCurrent() {
        return this.current;
    }
    public int getTotal() {
        return this.total;
    }
}