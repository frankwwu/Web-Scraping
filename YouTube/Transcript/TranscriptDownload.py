
from youtube_transcript_api import YouTubeTranscriptApi
import json

while True:
    try:
        print("Youtube Downloader".center(40, "_"))
        # Example: yt_id = 'VmCDvQecjA8'
        yt_id = input("Enter youtube id:  ")     
        t = YouTubeTranscriptApi.get_transcript(yt_id)       
        j = json.dumps(t, indent = 4)
        print(j)
        try:
            with open(yt_id + '.json', 'w') as f:
                f.write(j)               
        except Exception:
            print("Couldn't save the transcript.")
    except Exception:
        print("Couldn't download the transcript.")
    finally:
        option = int(input("\n1.download again \n2.Exit\n\nOption here :"))
    if option != 1:
        break
