import youtube_dl, json
from youtube_dl.postprocessor.ffmpeg import FFmpegMetadataPP
#from mutagen.easyid3 import EasyID3

#Variabler brukt til å lagre metadata
filnavn = ""

#Konfigurasjonsvariabler
video = False

#Brukes til å loggføre feil, aktivere debugging
class ytdlLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass
        #print("warn: " + msg)

    def error(self, msg):
        print("err: " + msg)

#Brukes til å legge til metadata
#https://github.com/ytdl-org/youtube-dl/issues/12225#issuecomment-285922882
class FFmpegMP3MetadataPP(FFmpegMetadataPP):

    def __init__(self, downloader=None, metadata=None):
        self.metadata = metadata or {}
        super(FFmpegMP3MetadataPP, self).__init__(downloader)

    def run(self, information):
        information = self.purge_metadata(information)
        information.update(self.metadata)
        return super(FFmpegMP3MetadataPP, self).run(information)

    def purge_metadata(self, info):
        info.pop('title', None)
        info.pop('track', None)
        info.pop('upload_date', None)
        info.pop('description', None)
        info.pop('webpage_url', None)
        info.pop('track_number', None)
        info.pop('artist', None)
        info.pop('creator', None)
        info.pop('uploader', None)
        info.pop('uploader_id', None)
        info.pop('genre', None)
        info.pop('album', None)
        info.pop('album_artist', None)
        info.pop('disc_number', None)
        return info

#Gir beskjed når nedlasting av videoer er fullført
def myHook(d):
    if d["status"] == "finished":
        print('Fullført nedlasting av {}, konvertering gjennomføres'.format(d["filename"]))
    filnavn = d["filename"]

#Nedlastingsalternativer tilgjengelige (Første krever ffmpeg)
#https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312
# 0 = Beste tilgjengelige lyd i mp3-format
# 1 = Beste tilgjengelige video i mp4-format eller annet om ikke mp4 er tilgjengelig (Maks 1080p)
ytdl_opts = [{
    "format": "bestaudio/best",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
    "outtmpl": ".\\Musikk\\%(artist)s - %(track)s #%(id)s.%(ext)s",
    "logger": ytdlLogger(),
    "progress_hooks": [myHook]
},{
    "format": "best[height<=1080]",
    "logger": ytdlLogger(),
    "progress_hooks": [myHook],
    "outtmpl": ".\\Videoer\\%(title)s.%(ext)s",
}]

#Mottar en lenke til en youtube video og Nedlastingsalternativer
#Denne videoen lastes så ned ved bruk av youtube-dl
def lastNedVideo(lenke, nedlastingstype, metadata):
    with youtube_dl.YoutubeDL(nedlastingstype) as ytdl:
        if metadata[0]:
            ffmpeg_mp3_metadata_pp = FFmpegMP3MetadataPP(ytdl, metadata[1])
            ytdl.add_post_processor(ffmpeg_mp3_metadata_pp)
        ytdl.download([lenke])


#Leser ut sanger fa fil, og laster ned disse
def sangerFraFil(filnavn):
    f = open(filnavn, "r").readlines()
    for l in f:
        #Sjekker om linjen skal kommenteres ut
        if l.strip().startswith('#'):
            continue
        #Variabler for sang
        ytdlArgs = ytdl_opts[0]
        tittel = ""
        artist = ""
        erMp3 = True

        #Finner argumenter
        l = l.replace("\n","")
        args = l.split(" -")
        lenke = args[0].strip()
        args = args[1:]

        #Tolker argumenter
        for i in range(0,len(args)):
            kommando = args[i]
            kommando = kommando.split(" ")
            kommando[0] = kommando[0].lower()
            if kommando[0] == "a" or kommando[0] == "artist":
                artist = " ".join(kommando[1:])
            elif kommando[0] == "t" or kommando[0] == "tittel":
                tittel = " ".join(kommando[1:])
            elif kommando[0] == "v" or kommando[0] == "video":
                ytdlArgs = ytdl_opts[1]
                erMp3 = False
            elif kommando[0] == "l" or kommando[0] == "lyd":
                ytdlArgs = ytdl_opts[0]
                erMp3 = True
        metadata = [erMp3, {"title":tittel, "artist":artist}]
        lastNedVideo(lenke,ytdlArgs, metadata)

if __name__ == "__main__":
    sangerFraFil(".\\musikkfil.txt")
