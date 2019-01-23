package com.example.mediekontroll;

//https://github.com/MarshallOfSound/Google-Play-Music-Desktop-Player-UNOFFICIAL-/blob/master/docs/PlaybackAPI.md
class SharedData_Motta_Main {
    public String hostnavn = "";
    public boolean endretHostnavn = false;
    public Sang sang = new Sang("", "", "", "");
    public boolean endretSangnavn = false;
    public boolean spiller = false;
    public boolean endretSpiller = false;
    public SangTid tid = new SangTid(0,0);
    public boolean endretTid = false;

    public static SharedData_Motta_Main globalInstance = new SharedData_Motta_Main();
}
