/*
Anders Kvanvig
Sender beskjeder til oppgitt port/ip
17.01.2019
http://www.avajava.com/tutorials/lessons/how-do-i-make-a-socket-connection-to-a-server.html
*/
import java.net.ServerSocket;
import java.net.Socket;
import java.net.Inet4Address;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.OutputStream;
import java.io.Console;
import static javax.swing.JOptionPane.*;

class Mediakontroll_Testverktoy {
        private static final int port = 49433;
        private static final String ip = "127.0.0.1";
        public static void main(String args[]) throws IOException {
                boolean f = true;
                while (f) {
                        Socket socket = new Socket(ip, port);
                        String kommando = showInputDialog("Hva ønsker du å sende?");
                        OutputStream os = socket.getOutputStream();
                        PrintWriter pw = new PrintWriter(os, true);
                        pw.println(kommando);
                        pw.close();
                        socket.close();
                        String res = showInputDialog("Ønsker du å sende mer? (y/n)");
                        if (res.equals("n") || res.equals("N")) {
                                f = false;
                        }
                }
        }
}
