from abc import get_cache_token
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json


# Create your views here.


def index(request):
    scope = 'user-read-currently-playing playlist-modify-private user-library-read playlist-read-collaborative playlist-read-private'

    cache_handler = spotipy.cache_handler.DjangoSessionCacheHandler(
        request=request)

    auth_manager = spotipy.oauth2.SpotifyOAuth(
        client_id="123", client_secret="123", redirect_uri="http://localhost:8000/guess_song_1/", scope=scope, cache_handler=cache_handler)

    # code is the return verified authentication from spotify server!!! you're getting this from the url and then erasing it by doing redirect(index)
    # so that the end user does not see the token.
    if request.GET.get("code"):
        auth_manager.get_access_token(request.GET.get("code"))
        return redirect("index")

    # cache_handler is manipulated, Also auth_manager does not redirect YET
    if not auth_manager.validate_token(cache_handler.get_cached_token()):

        auth_url = auth_manager.get_authorize_url()
        return render(request, "guess_song_1/index.html", {
            "auth_url": auth_url
        })

    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return render(request, "guess_song_1/login.html", {
        "name": spotify.me()["display_name"]
    })


def logged_in(request):

    sp = request.session['sp']

    request.session.pop('results', None)
    request.session.modified = True

    results = sp.current_user_saved_tracks()

    for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " – ", track['name'])

    return render(request, "guess_song_1/login.html",  {
        "results": results['items']['track']['name']
    })


def sign_out(request):

    del request.session['token_info']

    return redirect("index")


def playlist_page(request):

    cache_handler = spotipy.cache_handler.DjangoSessionCacheHandler(
        request=request)
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        client_id="b4500f1dc0064d498aeabc56c140ead0", client_secret="c3b0d3f0e2864dce93deeb5def7f4e9c", redirect_uri="http://localhost:8000/guess_song_1", cache_handler=cache_handler)

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    spotify = spotipy.Spotify(auth_manager=auth_manager)

    spotify_playlists = spotify.current_user_playlists()

    # [items][n][name] to get all the names!
    # pretty = json.dumps(
    #    spotify_playlists['items'][10]['name'], skipkeys=False, indent=0)
    dataJSON = json.dumps(spotify_playlists['items'])

    return render(request, "guess_song_1/playlists.html", {
        "playlists": spotify_playlists,
        "playlistsJSON": dataJSON
    })


def game(request):
    if request.method == 'POST':
        playlistNumber = int(request.POST['playlist'])
        cache_handler = spotipy.cache_handler.DjangoSessionCacheHandler(
            request=request)
        auth_manager = spotipy.oauth2.SpotifyOAuth(
            client_id="b4500f1dc0064d498aeabc56c140ead0", client_secret="c3b0d3f0e2864dce93deeb5def7f4e9c", redirect_uri="http://localhost:8000/guess_song_1", cache_handler=cache_handler)

        if not auth_manager.validate_token(cache_handler.get_cached_token()):
            return redirect('/')

        spotify = spotipy.Spotify(auth_manager=auth_manager)

        spotify_playlists = spotify.current_user_playlists()

        return render(request, "guess_song_1/game.html", {
            "playlist": spotify_playlists['items'][playlistNumber],
            "token": cache_handler.get_cached_token()

        })
