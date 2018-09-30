from django.shortcuts import render
import pytube
import os
import pathlib
# Create your views here.

def index (request):
    return render(request, 'index.html')

def download (request):
    if request.method == "POST":
        vurl = request.POST['url']
        vaudiovideo = request.POST['audio-video']
        if vaudiovideo == 'A':
            vext = request.POST['audio-ext']
        elif vaudiovideo == 'V':
            vext = request.POST['video-ext']

        def progress_Check(stream=None, chunk=None, file_handle=None, remaining=None):
            percent = (100 * (file_size - remaining)) / file_size
            print("{:00.0f}% downloaded".format(percent))

        def start():
            global file_size
            home = os.path.expanduser('~')
            print(home)
            download_path = pathlib.Path(home)
            #os.path.join(home, 'Downloads')
            print("Your video will be saved to: {}".format(download_path))

            try:
                yt = pytube.YouTube(vurl)
                #, on_progress_callback=progress_Check
                if vaudiovideo == 'A':
                    files = yt.streams.filter(only_audio=True).order_by('bitrate').desc().first()
                elif vaudiovideo == 'V':
                    files = yt.streams.filter().first()
                title = yt.title
                itag = files.itag
                ext  = files.mime_type.split('/')[-1]
                dfullname = itag + '.' + ext
                cfullname = itag +  vext
                dpath = download_path / dfullname
                cpath = download_path / cfullname
                print("Fetching: {}...".format(title))
                file_size = files.filesize
                print('Starting Download....')
                files.download(download_path,filename=itag)
                print('Download Completed')
                print('Starting Video Convertion...')
                os.rename(dpath, cpath)
                print('Video Convertion Finished')
            except:
                print("ERROR. Check your: -connectio! Try again.")

        begin = start()
        return render(request, 'index.html')

