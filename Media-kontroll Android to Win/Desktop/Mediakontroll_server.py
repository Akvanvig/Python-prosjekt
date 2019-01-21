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
#Mediakontroll
from pyautogui import press
import os

#Informasjonshenting
import platform

#Port for kommunikasjon, brukes for kommunikasjon i begge retninger
mPort = 49433
sPort = 49434
maksTilkoblinger = 3

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
    sdt = sendDataThread(q, sPort, maksTilkoblinger)
    sdt.start()
    while True:
        #Godtar tilkoblinger
        (clientSocket, address) = serverSocket.accept()
        ct = clientThread(clientSocket)
        q.put(address)
        #Mottar kommando fra klient
        ct.start()


class sendDataThread (threading.Thread):
    def __init__(self, q, port, maksTilkoblinger):
        threading.Thread.__init__(self)
        self.q = q
        self.port = port
        self.maksTilkoblinger = maksTilkoblinger
        self.addressList = []
        self.fortsett = True

    def run(self):
        print('Kjører send data tråd')
        while self.fortsett:
            if self.q:
                self.addressList = self.leggTilIP( self.addressList, self.q.get() )
            self.hentData()
            data = self.pakkData()
            for ip in self.addressList:
                self.sendData(ip, data)
            time.sleep(2)

    #Sjekker om IP som akkurat kontaktet program er lagt inn i
    def leggTilIP(self, liste, ip):
        #IP kommer inn som "('192.168.1.6', 35024)" (Henter ut bare IP)
        ip_str = str(ip).split("'")[1]
        if ip_str not in liste:
            liste.append(ip_str)
            if len(liste) > self.maksTilkoblinger:
                liste.pop(0)
            print(liste)
        return liste

    #Setter sammen data til en enkelt streng for overføring
    def pakkData(self):
        info = ''
        info +='host;;' + self.hostName
        return info

    #Sender data på port sPort til alle registrerte klienter (opptil fem)
    def sendData(self, ip, data):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, self.port))
            byt = data.encode()
            s.send(byt)
        except Exception as e:
            print('Kunne ikke sende melding til "' + ip + '"')
            print(e)
        s.close()

    #Henter inn data til overføring (Kan kobles sammen med API fra forskjellige medieavspillingsprogram som Google Play Music Desktop Player, eller Spotify)
    def hentData(self):
        self.hostName = platform.node()
        return



class clientThread (threading.Thread):
    def __init__(self, clientSocket):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket

    def run(self):
        #Leser meldingen (int = antall bytes)
        res = self.clientSocket.recv(16)
        self.clientSocket.close()
        #Gjør om til string (Fra byte)
        data = repr(res)
        #Fjerner ekstra tegn lagt til (b'stopp\n' --> stopp)
        data = data.replace('\\n','')
        data = data[2:-1]
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
