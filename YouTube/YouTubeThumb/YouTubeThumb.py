from pythumb import Thumbnail

while True:
    try:
        print("Youtube Downloader".center(40, "_"))
        url = input("Enter youtube url:  ")
        t = Thumbnail(url)
        t.fetch()
        t.save('.')
    except Exception:
        print("Couldn't download the thumb.")
    finally:
        option = int(input("\n1.download again \n2.Exit\n\nOption here :"))
    if option != 1:
        break

