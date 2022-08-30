import bin.cred.cred as cred, spotipy, re, os,subprocess, urllib.request
from pytube import YouTube
from spotipy.oauth2 import SpotifyClientCredentials
from scripts import gui

completed = 0
text = ''

def inst(query,py,screen):
    global completed, text

    text = 'Searching Spotify'
    completed += 10

    client_credentials_manager = SpotifyClientCredentials(client_id=cred.spot()[0], client_secret=cred.spot()[1])
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    artist_name = []
    track_name = []
    popularity = []
    for i in range(1):
        track_results = sp.search(q=query, type='track', limit=10,offset=i)
        for i, t in enumerate(track_results['tracks']['items']):
            artist_name.append(t['artists'][0]['name'])
            track_name.append(t['name'])
            popularity.append(t['popularity'])
    
    ind = 0
    ch = True
    sng_name = ''
    for name in track_name:
        if query == name.lower():
            ch = False
            query = artist_name[ind] + ' ' + name + ' lyrics'
            sng_name = name
            break
        ind +=1

    text = 'Finding link'
    completed +=5

    if ch:
        popularity_ind = popularity.index(max(popularity))
        query = artist_name[popularity_ind] + ' ' + track_name[popularity_ind] + ' lyrics'
        sng_name = track_name[popularity_ind]
    temp = ''
    for i in query:
        if i!=' ':
            temp+=i
        else:
            temp+='+'
    query = temp
    sng_name_temp = ''
    for i in sng_name:
        if i not in "\"\\\'()":
            sng_name_temp+=i
    sng_name = sng_name_temp
    html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={query}")
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    text = 'link found'
    completed +=5

    yt = YouTube(f"https://www.youtube.com/watch?v={video_ids[0]}")

    text = 'installing MP4 file'
    completed +=25

    yt.streams.filter(file_extension='mp4', resolution='360p').first().download(filename=f'bin\\temp\\{sng_name}.mp4')
    DETACHED_PROCESS = 0x00000008

    text = 'converting MP4 to MP3'
    completed +=40

    subprocess.call(f'ffmpeg\\bin\\ffmpeg.exe -i "bin\\temp\\{sng_name}.mp4" "bin\\temp\\{sng_name}.mp3"', creationflags=DETACHED_PROCESS)
    os.remove(f"bin\\temp\\{sng_name}.mp4")

    text='Writing to .rick_roll binary'
    completed +=10

    try:
        f = open(f"bin\\temp\\{sng_name}.mp3", 'rb')
        file = open(f'bin\\{sng_name}.rick_roll', 'wb')
        
        while True:
            b = f.read(1)
            if not b:
                break
            file.write(b)
        f.close()
        file.close()
    except:
        pass

    text = 'cleaning'
    completed +=5

    os.remove(f"bin\\temp\\{sng_name}.mp3")
    text = ''
    completed = 0