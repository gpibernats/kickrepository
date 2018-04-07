from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

app_name="games"
urlpatterns = [



    url(r"^games/$", views.AllGamesListView.as_view(), name="all_games"),
    # url(r"^my-games/$", views.MyGamesView.as_view(), name="my_games"),
    url(r"^new-game/$", views.CreateGameView.as_view(), name="create_game"),
    url(r"^new-game/right-wrong-mode/$", views.CreateGameRightWrongModeView.as_view(), name="create_game_rwmode"),
    url(r"^new-game/pairs-mode/$", views.CreateGamePairsModeView.as_view(), name="create_game_pairsmode"),
    url(r"^edit-game/(?P<slug>[-\w]+)/$", views.update_game_data_redirection, name="update_game"),
    url(r"^edit-game/right-wrong-mode/(?P<slug>[-\w]+)/$", views.UpdateGameDataRightWrongModeView.as_view(), name="update_game_rwmode"), # url hardcoded in UpdateGameDataRedirection!!
    url(r"^edit-game/pairs-mode/(?P<slug>[-\w]+)/$", views.UpdateGameDataPairsModeView.as_view(), name="update_game_pairsmode"), # url hardcoded in UpdateGameDataRedirection!!
    url(r"^delete-game/(?P<slug>[-\w]+)/$", views.DeleteGameView.as_view(), name="delete_game"),
    #
    #
    #
    url(r"^(?P<slug>[-\w]+)/$", views.PreviewGameView.as_view(), name="game"), #conflict with all_games, game_request, etc!!!!!
    url(r"^(?P<slug_data>[-\w]+)/play/(?P<slug_game>[-\w]+)/$", views.PlayGameView.as_view(), name="play_game"),
    url(r"^(?P<slug>[-\w]+)/xml/$", views.xml_game_data, name="xml_game"),
    url(r"^(?P<slug_data>[-\w]+)/play/(?P<slug_game>[-\w]+)/get-max-score/$", views.get_max_score, name="get_max_score"),
    url(r"^(?P<slug_data>[-\w]+)/play/(?P<slug_game>[-\w]+)/get-mark/(?P<score>[0-9]+)/$", views.get_mark, name="get_mark"),
    url(r"^(?P<slug_data>[-\w]+)/play/(?P<slug_game>[-\w]+)/post-score/$", views.post_score, name="post_score"),






    # url(r"^testgame/", TemplateView.as_view(template_name="games/game.html"), name="testgame"),
]
