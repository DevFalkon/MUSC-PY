import data.cred.cred as cred, spotipy, re, os,subprocess, urllib.request
from pytube import YouTube
from spotipy.oauth2 import SpotifyClientCredentials

update = True

def spot_search(query):
    client_credentials_manager = SpotifyClientCredentials(client_id=cred.spot()[0], client_secret=cred.spot()[1])
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    artist_name = []
    track_name = []
    popularity = []
    duration = []
    track_art = []
    for i in range(1):
        track_results = sp.search(q=query, type='track', limit=10,offset=i)
        for i, t in enumerate(track_results['tracks']['items']):
            if t['name'].lower() == query.lower():
                artist_name = t['artists'][0]['name']
                track_name = t['name']
                duration = t['duration_ms']
                track_art = t['album']['images'][0]['url']
                return artist_name, track_name, duration, track_art
            else:
                artist_name.append(t['artists'][0]['name'])
                track_name.append(t['name'])
                duration.append(t['duration_ms'])
                popularity.append(t['popularity'])
                track_art.append(t['album']['images'][0]['url'])
    ind = popularity.index(max(popularity))
    return artist_name[ind], track_name[ind], duration[ind], track_art[ind]


def find_result(duration, video_ids, err):
    dur = duration//1000
    for yt in video_ids:
        if dur-err<= yt.length<=dur+err:
            return yt
    return None

def update_info(track_name, artist_name,duration):
    with open("data\\track_data.txt", 'a') as file:
        sng_info = {
            'name':track_name,
            'artist': artist_name,
            'duration':duration
        }
        file.write(f"{sng_info}\n")

def inst(query, sng_type = 'lyrics'):
    global update
    
    try:
        artist_name, track_name, duration, track_art = spot_search(query)
        temp = ''
        for i in track_name:
            if i not in '()\\\"\'[}]{':
                temp+=i
        track_name = temp
        temp  = ''
        for i in track_name.split():
            if i.lower() == 'from':
                break
            else:
                temp+=i+ ' '
        track_name = temp

        while track_name[-1] in ' -\'({)}[]':
            track_name = track_name[:-1]
            
        with open("data\\track_data.txt", 'r') as file:
            ls = [eval(i) for i in file.read().split('\n') if i]
        if track_name in [i['name'] for i in ls]:
            pass
        else:

            urllib.request.urlretrieve(track_art, f"data\\track_art\\{track_name}.jpg")

            query = track_name+'+'+artist_name+'+'+sng_type
            search = ''
            for i in query:
                if i != ' ':
                    search+=i
                else: search+='+'
    
            html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={search}")
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

            id_ls = []
            cnt = 0
            for vid_id in video_ids:
                if cnt>5:
                    break
                vid = YouTube(f"https://www.youtube.com/watch?v={vid_id}")
                vid_t = ''
                for i in vid.title.lower():
                    if i.isalnum() or i == ' ':
                        vid_t+=i
                t_name = ''
                for i in track_name.lower():
                    if i.isalnum() or i == ' ':
                        t_name+=i
                if t_name in vid_t:
                    yt = id_ls.append(vid)
                    cnt+=1
            
            if len(id_ls) == 0:
                os.remove(f'data\\track_art\\{track_name}.jpg')
                print('no result')
                return
                
            yt = None
            err = 0
            while not yt:
                yt = find_result(duration, id_ls, err)
                err+=2
                if err >15:
                    os.remove(f'data\\track_art\\{track_name}.jpg')
                    print('no accurate res')
                    return
            id_ls = None
            yt.streams.filter().get_lowest_resolution().download(filename=f'data\\temp\\{track_name}.mp4')
            
            DETACHED_PROCESS = 0x00000008
            subprocess.call(f'ffmpeg\\ffmpeg.exe -i "data\\temp\\{track_name}.mp4" "data\\temp\\{track_name}.mp3"', creationflags=DETACHED_PROCESS)
            os.remove(f"data\\temp\\{track_name}.mp4")
            try:
                os.rename(f"data\\temp\\{track_name}.mp3", f"data\\tracks\\{track_name}.rick_roll")
            except:
                os.remove(f"data\\tracks\\{track_name}.rick_roll")
                os.rename(f"data\\temp\\{track_name}.mp3", f"data\\tracks\\{track_name}.rick_roll")

            #Saving song info in a json file
            update_info(track_name, artist_name,yt.length)
            
            update = True
    except:
        pass