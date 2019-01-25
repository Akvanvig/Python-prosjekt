/*
Anders Kvanvig
Mottar beskjeder fra nettverket på oppgitt port, og klikker på mediataster når etterspurt
Java kan ikke utføre klikk på mediataster!
17.01.2019
http://www.avajava.com/tutorials/lessons/how-do-i-make-a-socket-connection-to-a-server.html
Krever:
JIntellyType - https://code.google.com/archive/p/jintellitype/downloads
*/
import java.net.ServerSocket;
import java.net.Socket;
import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.awt.Robot;


class MediakontrollServer {
        private static final int port = 49433;
        private static ServerSocket serverSocket;
        private static Robot r;

        public static void main(String[] args) {
                try {
                        serverSocket = new ServerSocket(port);
                } catch (IOException ioe) {
                        System.out.println("Kunne ikke lytte på " + port);
                        System.exit(-1);
                }
                try {
                        r = new Robot();
                } catch (Exception e) {
                        System.out.println(e.toString());
                        System.exit(-1);
                }
                while (true) {
                        String str = "Ikke initialisert";
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

        private static void tolkSignal(String s) {
                switch (s) {
                        case "playPause":
                                System.out.println("Mottat: '" + s + "'");
                                //r.keyPress(179);
                                break;
                        case "forrige":
                                System.out.println("Mottat: '" + s + "'");
                                //r.keyPress(177);
                                break;
                        case "neste":
                                System.out.println("Mottat: '" + s + "'");
                                //r.keyPress(176);
                                break;
                        case "volumOpp":
                                System.out.println("Mottat: '" + s + "'");
                                //r.keyPress(175);
                                break;
                        case "volumNed":
                                System.out.println("Mottat: '" + s + "'");
                                //r.keyPress(174);
                                break;
                        case "mute":
                                System.out.println("Mottat: '" + s + "'");
                                //r.keyPress(173);
                                break;
                        default:
                                System.out.println("Gjenkjente ikke signal '" + s + "'");
                                break;
                }
        }
}
