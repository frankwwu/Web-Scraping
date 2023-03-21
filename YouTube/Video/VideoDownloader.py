from pytube import YouTube

while True:
    try:
        print("Youtube Downloader".center(40, "_"))
        url = input("Enter youtube url:  ")
        yt = YouTube(url)
        yd = yt.streams.get_highest_resolution()
        yd.download()
    except Exception:
        print("Couldn't download the video.")
    finally:
        option = int(input("\n1.download again \n2.Exit\n\nOption here :"))
    if option != 1:
        break
