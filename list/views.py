from .models import Playlist, Video
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import DetailView
import requests

def index(request):
    if request.method == 'POST':
        list_url = 'https://www.googleapis.com/youtube/v3/playlists'
        listItems_url = 'https://www.googleapis.com/youtube/v3/playlistItems'
        link = request.POST['link']
        pl = Playlist(url=link)

        list_id = link.replace('https://youtube.com/playlist?list=', '')
        list_id = list_id.replace('https://www.youtube.com/playlist?list=', '')

        list_params = {
            'part': 'snippet',
            'id' : list_id,
            'key' : settings.YOUTUBE_DATA_API_KEY,
        }
        r = requests.get(list_url, params=list_params)
        pl.title = r.json()['items'][0]['snippet']['title']

        listItems_params = {
            'part': 'snippet',
            'playlistId' : list_id,
            'key' : settings.YOUTUBE_DATA_API_KEY,
        }
        r = requests.get(listItems_url, params=listItems_params)
        nums = r.json()['pageInfo']['totalResults']

        listItems_params = {
            'part': 'snippet',
            'playlistId' : list_id,
            'maxResults' : nums,
            'key' : settings.YOUTUBE_DATA_API_KEY,
        }
        
        r = requests.get(listItems_url, params=listItems_params)
        results = r.json()['items']
        
        pl.save()
        for result in results:
            video = Video(title=result['snippet']['title'], channel=result['snippet']['videoOwnerChannelTitle'], playlist=pl)
            video.save()
        
        return redirect('list:index')

    playlists = Playlist.objects.all()    

    return render(request, 'list/index.html', {'playlists': playlists})

class Detail(DetailView):
    model = Playlist
    template_name = 'list/detail.html'   