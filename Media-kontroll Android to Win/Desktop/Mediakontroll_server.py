'''
Anders Kvanvig
Mottar beskjeder fra nettverket på oppgitt port, og klikker på mediataster når etterspurt
20.01.2019

Krever:
pyAutoGui - https://pyautogui.readthedocs.io/en/latest/install.html
'''

#Nettverkskommunikasjon
import threading
import queue
import socket
import time
import json
#Mediakontroll
from pyautogui import press
import os

#Informasjonshenting
import platform

#Port for kommunikasjon, brukes for kommunikasjon i begge retninger
mPort = 49433
sPort = 49434
maksTilkoblinger = 3
addresseliste = []

hostName = platform.node()
dataChanged = True
'''
#GPMDP-info https://github.com/MarshallOfSound/Google-Play-Music-Desktop-Player-UNOFFICIAL-/blob/master/docs/PlaybackAPI.md
playing = False #Forteller om sangen spilles av nå
rating = [] #Rating object, [bool liked, bool disliked]
repeat = '' #'LIST_REPEAT', 'SINGLE_REPEAT' eller 'NO_REPEAT'
shuffle = '' #'ALL_SHUFFLE', 'NO_SHUFFLE'
song = [] #Song object, ['tittel', 'artist', 'albumtittel', 'albumbilde (url)']
time = [] #Time object, [current time in ms, total time in ms]
'''
def main():
    print(hostName)
    #Oppretter Queue for kommunikasjon mellom Tråder (Brukes for å sende klient-adresser mellom tråder)
    q = queue.Queue()

    #Oppretter server socket som lytter på gitt på fra alle avsendere
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('', mPort))
    serverSocket.listen(5)

    #Oppretter Tråd for å sende data
    sdt = sendDataThread(sPort)
    sdt.daemon = True
    sdt.start()
    ml = mainLoop(serverSocket)
    ml.daemon = True
    ml.start()
    while True:
        time.sleep(5)


class mainLoop (threading.Thread):
    def __init__(self, serverSocket):
        threading.Thread.__init__(self)
        self.serverSocket = serverSocket

    def run(self):
        global addresseliste
        while True:
            #Godtar tilkoblinger
            (clientSocket, address) = self.serverSocket.accept()
            ct = clientThread(clientSocket)
            addresseliste = self.leggTilIP(addresseliste, address)
            #Mottar kommando fra klient
            ct.start()

    #Sjekker om IP som akkurat kontaktet program er lagt inn i
    def leggTilIP(self, liste, ip):
        global maksTilkoblinger
        #IP kommer inn som "('192.168.1.6', 35024)" (Henter ut bare IP)
        ip_str = str(ip).split("'")[1]
        if ip_str not in liste:
            liste.append(ip_str)
            if len(liste) > maksTilkoblinger:
                liste.pop(0)
            print(liste)
        return liste


class sendDataThread (threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port

    def run(self):
        global addresseliste

        print('Kjører send data tråd')
        while True:
            playing, repeat, shuffle, song, times = self.hentData()
            data = self.pakkData(playing, repeat, shuffle, song, times)
            for i in range(len(addresseliste)):
                try:
                    self.sendData(addresseliste[i], data)
                except Exception as e:
                    print(e)

            #print('Sendt Oppdatering til: ' + str(addresseliste))
            time.sleep(2)


    #Setter sammen data til en enkelt streng for overføring
    def pakkData(self, playing, repeat, shuffle, song, time):
        info = ''
        info +='host;;' + self.hostName
        if playing:
            info +='|playing;;1'
        else:
            info +='|playing;;0'

        info +='|repeat;;' + repeat + ' '
        info +='|shuffle;;' + shuffle + ' '
        if (song[0] is not None):
            info +='|song;;' + song[0] + ';' + song[1] + ';' + song[2] + ';' + song[3] + ''
        else:
            info += '|song;; ; ; ; '


        info +='|time;;' + str(time[0]) + ';' + str(time[1])
        return info

    #Sender data på port sPort til alle registrerte klienter (opptil fem)
    def sendData(self, ip, data):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, self.port))
            byt = data.encode('utf8')
            s.send(byt)
        except Exception as e:
            print('Kunne ikke sende melding til "' + ip + '"')
            print(e)
        s.close()

    #Henter inn data til overføring (Kan kobles sammen med API fra forskjellige medieavspillingsprogram som Google Play Music Desktop Player, eller Spotify)
    def hentData(self):
        self.hostName = platform.node()

        playing = False
        repeat = ''
        shuffle = ''
        song = ['','','','']
        times = [0,0]
        #GPMDP
        filsti = os.getenv('APPDATA') + '\\Google Play Music Desktop Player\\json_store\\playback.json'
        with open(filsti, 'r', encoding="utf8") as read_file:
            data = json.load(read_file)
            playing = data['playing']
            repeat = data['repeat']
            shuffle = data['shuffle']
            songData = data['song']
            song = [songData['title'], songData['artist'], songData['album'], songData['albumArt']]
            timeData = data['time']
            time = [timeData['current'], timeData['total']]

        return playing, repeat, shuffle, song, times


class clientThread (threading.Thread):
    def __init__(self, clientSocket):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket

    def run(self):
        #Leser meldingen (int = antall bytes)
        data = self.clientSocket.recv(16)
        self.clientSocket.close()

        #Dekoder fra bytekode til utf-8 og fjerner 'ny linje'-tegn sist
        data = data.decode("utf-8", "replace")[0:-1]


        if data == 'playPause':
            print ('Mottat: "' + data + '"')
            press('playpause')
        elif data == 'forrige':
            print ('Mottat: "' + data + '"')
            press('prevtrack')
        elif data == 'neste':
            print ('Mottat: "' + data + '"')
            press('nexttrack')
        elif data == 'volumOpp':
            print ('Mottat: "' + data + '"')
            press('volumeup')
        elif data == 'volumNed':
            print ('Mottat: "' + data + '"')
            press('volumedown')
        elif data == 'mute':
            print ('Mottat: "' + data + '"')
            press('volumemute')
        elif data == 'stopp':
            print ('Mottat: "' + data + '"')
            os._exit(1)
        else:
            print ('Kunne ikke gjenkjenne kommando: "' + data + '"')

main()
