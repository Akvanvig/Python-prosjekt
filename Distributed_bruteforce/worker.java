/*
Sender jevnlig en forespørsel til kontroller og etterspør område å søke gjennom.

Venter x antall sekund om ingen oppgaver

Tested with java 13.0.2
Set classpath: $env:CLASSPATH = '<PATH_TO_JAR_FILES>\*;.'
*/
import java.net.*;
import java.io.*;
import java.util.*;
import java.lang.Thread;

import com.google.gson.*; //https://github.com/google/gson/blob/master/UserGuide.md
import com.google.gson.JsonObject;

class worker {
  //private static String url = "http://127.0.0.1";
  private static String url = "http://controller.controller-deployment.svc"
  private static int port = 80;
  private static int retryTime = 10; //Seconds

  public static void main(String[] args) {
    while (true) {
      JsonObject job = getJob();
      if ( ! (job.get("finished")).getAsBoolean()) {

      } else {
        try {
          Thread.sleep(retryTime * 1000);
        } catch (Exception e) {
          System.out.println("Sleep failed: " + e);
        }
      }
    }
  }

  private static JsonObject getJob() {
    //Sends request for new task
    JsonObject request = new JsonObject();
    request.addProperty("type","get");
    request.addProperty("subtype","job");
    String responseStr = sendPostRequest(request.toString());
    JsonObject response = new Gson().fromJson(responseStr, JsonObject.class);
    //Interprets response
    if ((response.get("status_code")).getAsInt() == 1) {
      System.out.println(response.get("job"));
      return new Gson().fromJson(response.get("job").toString(), JsonObject.class);//new JsonObject(response.get("job").toString());
    } else {
      System.out.println(response.get("status") + "\n" + response.get("error-message"));
      return new Gson().fromJson("{\"finished\":True,\"free_block\":False,\"keyword\":\"\",\"chars\":\"\",\"algorithm\":\"\",\"start_point\":\"\",\"end_point\":\"\"}", JsonObject.class);
    }
  }

  private static String sendPostRequest(String message) {
    //https://www.baeldung.com/httpurlconnection-post
    try {
      URL link = new URL(url + ":" + String.valueOf(port));
      HttpURLConnection connection = (HttpURLConnection) link.openConnection();
      connection.setRequestMethod("POST");
      connection.setRequestProperty("Content-Type", "application/json; utf-8");
      connection.setRequestProperty("Accept", "application/json");
      connection.setDoOutput(true);

      //writing message
      OutputStream os = connection.getOutputStream();
      byte[] input = message.getBytes("utf-8");
      os.write(input, 0, input.length);

      //Reading message
      BufferedReader br = new BufferedReader(new InputStreamReader(connection.getInputStream(), "utf-8"));
      StringBuilder response = new StringBuilder();
      String responseLine = null;
      while ((responseLine = br.readLine()) != null) {
        response.append(responseLine.trim());
      }
      return response.toString();

    } catch (Exception e) {
      //System.out.println("ERROR SPR - " + e);
      return "{\"status_code\":2, \"status\": \"Request Failed\", \"error-message\": \"" + e + "\" }";
    }
  }

  private Runnable pwdCrack(final JsonObject job) {
    Runnable runnable = new Runnable() {
      //Collecting info needed to make search
      int taskID = (job.get("task_id")).getAsInt();
      String algorithm = (job.get("algorithm")).getAsString();
      String startPoint = (job.get("start_point")).getAsString();
      String endPoint = (job.get("end_point")).getAsString();
      String keyword = (job.get("keyword")).getAsString();
      String chars = (job.get("chars")).getAsString();
      String currentWord = startPoint;

      //variables needed to check result
      String algCurrentWord = "";
      byte status = 0; //0 = keep serching, 1 = word found, 2 = reached end of searcharea, 3 = unknown algorithm

      public void run() {
        while (status == 0) {
          genAlgCurrentWord();
          if (algCurrentWord.equals(keyword)) {
            status = 1;
          } else if (currentWord.equals(endPoint)) {
            status = 2;
          } else {
            currentWord = increaseVal(currentWord, ((currentWord.length()) - 1), chars.length());
          }
        }
        genResultJson();
      }

      private void genAlgCurrentWord() {
        //transforms string using algorithm specified
        //algorithm && currentWord
        switch (algorithm) {
          case "none":
            algCurrentWord = currentWord;
            break;
          case "lettershift":
            algCurrentWord = Encrypt.lettershift(currentWord, 5, chars);
            break;
          default:
            status = 3;
        }
      }

      private String increaseVal(String word, int pos, int countChars) {
        //Increases value of string by one according to characters available

        int x = chars.indexOf(word.charAt(pos));
        String newWord = "";
        //if this char is highest value char
        if (x == countChars) {
          //if length of word has to be increased
          if (pos == 0) {
            //newWord = ((Character) chars.charAt(0)).toString().repeat(word.length() + 1);
            char[] array = new char[word.length() + 1];
            Arrays.fill(array, chars.charAt(0));
            newWord = new String(array);
          } else {
            x = 0;
            StringBuilder tempWord = new StringBuilder(increaseVal(word, pos -1, countChars));
            tempWord.setCharAt(pos, chars.charAt(x));
            newWord = tempWord.toString();
          }
          return newWord;
        } else {
          StringBuilder tempWord = new StringBuilder(word);
          tempWord.setCharAt(pos, chars.charAt(x + 1));
          newWord = tempWord.toString();
          return newWord;
        }
      }

      private String genResultJson() {
        //packs all info needed for reply to controller into one Json string
        boolean foundKeywordBool = ((status == 1) ? false : true);
        String errorMessage = ((status == 3) ? "" : "Algorithm is not supported in this version");
        JsonObject result = new JsonObject();
        result.addProperty("start_point",startPoint);
        result.addProperty("end_point",endPoint);
        result.addProperty("keyword",keyword);
        result.addProperty("found_keyword_bool", foundKeywordBool);
        result.addProperty("keyword_found", currentWord);
        result.addProperty("task_id", taskID);
        result.addProperty("error_message", errorMessage);

        return result.toString();
      }
    };
    return runnable;
  }
}

class Encrypt {
  public static String lettershift(String word, int shift, String chars) {
    char[] chrArr = word.toCharArray();
    for (int i = 0; i < chrArr.length; i++) {
      int j = (chars.indexOf(chrArr[i]) + shift) % chars.length();
      j = (j < 0) ? (j + chars.length()) : j;
      chrArr[i] = chars.charAt(j);
    }
    return new String(chrArr);
  }
}
