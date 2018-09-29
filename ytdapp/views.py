from django.shortcuts import render
import pytube
import os
import subprocess
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
            download_path = 'app/downloads'
            #os.path.join(home, 'Downloads')
            print("Your video will be saved to: {}".format(download_path))

            #try:
            yt = pytube.YouTube(vurl, on_progress_callback=progress_Check)

            if vaudiovideo == 'A':
                files = yt.streams.filter(only_audio=True).order_by('bitrate').desc().first()
            elif vaudiovideo == 'V':
                files = yt.streams.filter().first()
            print(files.filesize)
            title = yt.title
            itag = files.itag
            ext  = files.mime_type.split('/')[-1]
            dfullname = itag + '.' + ext
            cfullname = itag +  vext
            print("Fetching: {}...".format(title))
            file_size = files.filesize
            print("filesize: " + str(file_size))
            print('path: '+ download_path + '\\' + dfullname + '---' + download_path + '\\' + cfullname)
            files.download(download_path, filename=itag)
            print("itage: "  + itag)

            os.rename(download_path+'\\'+dfullname, download_path+'\\'+cfullname)
            print("rename done")
            #subprocess.call(['ffmpeg', '-i',  os.path.join(download_path, dfullname), os.path.join(download_path, cfullname)])
            print('done')
            #except:
            print("ERROR. Check your: -connectio! Try again.")

        begin = start()
        return render(request, 'index.html')
