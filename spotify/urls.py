from django.urls import path

from . import views

urlpatterns = [
    path('/get-auth-url', views.AuthURL.as_view()),
    path('/redirect', views.spotify_callback),
    path('/is-authenticated', views.IsAuthenticated.as_view()),
    path('/current-song', views.CurrentSong.as_view()),
    path('/user-profile', views.UserProfile.as_view()),
    path('/pause', views.PauseSong.as_view()),
    path('/play', views.PlaySong.as_view()),
    path('/skip', views.SkipSong.as_view()),
    path('/playlists', views.Playlist.as_view()),
    path('/play/<playlist_id>', views.PlayPlaylist.as_view()),
]