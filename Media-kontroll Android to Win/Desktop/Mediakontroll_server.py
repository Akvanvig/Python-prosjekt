'''
Anders Kvanvig
Mottar beskjeder fra nettverket på oppgitt port, og klikker på mediataster når etterspurt
20.01.2019

Krever:
pyAutoGui - https://pyautogui.readthedocs.io/en/latest/install.html
'''

#Nettverkskommunikasjon
import threading
import socket
#Mediakontroll
from pyautogui import press
import os

#Informasjonshenting
import platform

port = 49433
addressList = []

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
    #Oppretter server socket som lytter på gitt på fra alle avsendere
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('', port))
    serverSocket.listen(5)

    while True:
        #Godtar tilkoblinger
        (clientSocket, address) = serverSocket.accept()
        ct = clientThread(clientSocket)
        addressList.append(address)
        #Hvis 6 enheter er koblet til tjeneren, vil første fjernes
        if len(addressList) > 5:
            addressList.pop(0)
        #Mottar kommando fra klient
        ct.start()

'''
class sendDataThread (threading.Thread):
    def __init__(self, ip, port, hostName):
        self.ip = ip
        self.port = port
        self.hostName = hostName

    def run(self):
        print('Kjører send data tråd')
        info = ''
        if self.hostName != '':
            info +='host;;' + self.hostName
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(self.ip, self.port)
        try:
            pass
        except Exception as e:
            raise
        s.send(info)
        s.close()
'''
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
