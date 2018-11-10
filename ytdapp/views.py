from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
import pytube
import os
import pathlib

# Create your views here.

def index (request):
    headlines = "Convert Youtube Video to MP3 or any other format"
    return render(request, 'index.html', {'headlines': headlines})

def convert (request):
    if request.method == "POST":
        vurl = request.POST['url']
        vaudiovideo = request.POST['audio-video']

        if vaudiovideo == 'A':
            vext = request.POST['audio-ext']
        elif vaudiovideo == 'V':
            vext = request.POST['video-ext']

        home = os.path.expanduser('~')
        download_path = pathlib.Path('media')
        print("Your video will be saved to: {}".format(download_path))

        #try:
        yt = pytube.YouTube(vurl)

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
        abscpath = "\\" + str(cpath)
        print('Fetching video....')
        files.download(download_path,filename=itag)
        print('Starting Video conversion...')
        os.rename(dpath, cpath)
        print('Video conversion completed!')
        return render(request, 'download.html', {'abscpath': abscpath})
        #except:
        #   print("ERROR. Check your: -connection! Try again.")
        #   return render(request, 'index.html')

    def download(request, path):
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="audio/mpeg")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404

    #return render(request,'index.html')


