from django.views import generic
from django.shortcuts import render, redirect
from games.forms import UpdateGameDataFormRightWrongMode, UpdateGameDataFormPairsMode
from games.models import GameData, GameDataRightWrongMode, GameDataPairsMode, Game, GameDataStats, GameStats
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
# from django.urls import reverse # django 1.10
# from django.core.urlresolvers import reverse #django 1.9
from django.contrib.auth.mixins import LoginRequiredMixin
# from user_profiles.models import UserProfile
from django.contrib.auth.models import User



from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt






def get_max_score(request, slug_data, slug_game):
    gd = GameData.objects.get(slug= slug_data)
    g = Game.objects.get(slug= slug_game)
    stats = GameDataStats.objects.get_or_create(game_data= gd, game= g)
    return HttpResponse(stats[0].get_max_score())

def get_mark(request, slug_data, slug_game, score):
    gd = GameData.objects.get(slug= slug_data)
    g = Game.objects.get(slug= slug_game)
    stats = GameDataStats.objects.get_or_create(game_data= gd, game= g)
    max_score = stats[0].get_max_score() * 1.0
    if (max_score == 0):
        return HttpResponse(100)
    if (int(score) >= max_score):
        return HttpResponse(100)
    return HttpResponse((int(score)/max_score)*100)

@csrf_exempt
def post_score(request, slug_data, slug_game):
    if request.method == "POST":
        score = request.POST.get("score", "")
        gd = GameData.objects.get(slug= slug_data)
        g = Game.objects.get(slug= slug_game)
        # +1 times_played GameStats
        stats = GameStats.objects.get_or_create(game= g)
        stats[0].played()
        stats[0].save()
        # +1 times_played GameDataStats and add score
        stats = GameDataStats.objects.get_or_create(game_data= gd, game= g)
        stats[0].add_score(score)
        stats[0].save()
        # +1 times_played PlayerStats and add score
    else:
        score = 10
        gd = GameData.objects.get(slug= slug_data)
        g = Game.objects.get(slug= slug_game)
        # +1 times_played GameStats
        stats = GameStats.objects.get_or_create(game= g)
        stats[0].played()
        stats[0].save()
        # # +1 times_played GameDataStats and add score
        stats = GameDataStats.objects.get_or_create(game_data= gd, game= g)
        stats[0].add_score(score)
        stats[0].save()
    return HttpResponse("hi")



class AllGamesListView(generic.ListView):
    template_name = "games/list.html"
    def get_queryset(self):
        return GameData.objects.all()

class MyGamesView(generic.ListView):
    template_name = "games/my_games.html"
    def get_queryset(self):
        return GameData.objects.filter(user= self.request.user)


class CreateGameView(generic.TemplateView):
    template_name = "games/new_game.html"


# class CreateGameRightWrongModeView(LoginRequiredMixin, generic.edit.CreateView):
#     template_name = "games/new_game_rw_mode.html"
#     # model = GameDataRightWrongMode
#     # fields = GameDataRightWrongMode.editable_fields()
#     form_class = UpdateGameDataFormRightWrongMode
#     success_url = "/teach"
#     # LoginRequiredMixin Settings
#     login_url = "/account/login/"
#     redirect_field_name = "redirect_to"
#     # Set user to logged in user
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super(CreateGameRightWrongModeView, self).form_valid(form)
class CreateGameRightWrongModeView(generic.edit.CreateView):
    template_name = "games/new_game_rw_mode.html"
    # model = GameDataRightWrongMode
    # fields = GameDataRightWrongMode.editable_fields()
    form_class = UpdateGameDataFormRightWrongMode
    success_url = "/teach"
    # Set user to logged in user
    def form_valid(self, form):
        form.instance.user = User.objects.get(pk=3)
        return super(CreateGameRightWrongModeView, self).form_valid(form)

# class CreateGamePairsModeView(LoginRequiredMixin, generic.edit.CreateView):
#     template_name = "games/new_game_pairs_mode.html"
#     # model = GameDataPairsMode
#     # fields = GameDataPairsMode.editable_fields()
#     form_class = UpdateGameDataFormPairsMode
#     success_url = "/teach"
#     # LoginRequiredMixin Settings
#     login_url = "/account/login/"
#     redirect_field_name = "redirect_to"
#     # Set user to logged in user
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super(CreateGamePairsModeView, self).form_valid(form)
class CreateGamePairsModeView(generic.edit.CreateView):
    template_name = "games/new_game_pairs_mode.html"
    # model = GameDataPairsMode
    # fields = GameDataPairsMode.editable_fields()
    form_class = UpdateGameDataFormPairsMode
    success_url = "/teach"
    # Set user to logged in user
    def form_valid(self, form):
        form.instance.user = User.objects.get(pk=3)
        return super(CreateGamePairsModeView, self).form_valid(form)

# class UpdateGameDataRightWrongModeView(generic.edit.UpdateView):
#     template_name = "games/update_game_rw_mode.html"
#     # model = GameDataRightWrongMode
#     # fields = GameDataRightWrongMode.editable_fields()
#     form_class = UpdateGameDataFormRightWrongMode
#     success_url = "/teach"
#     def get_object(self):
#         return GameDataRightWrongMode.objects.get(slug=self.kwargs["slug"], user= self.request.user)
class UpdateGameDataRightWrongModeView(generic.edit.UpdateView):
    template_name = "games/update_game_rw_mode.html"
    # model = GameDataRightWrongMode
    # fields = GameDataRightWrongMode.editable_fields()
    form_class = UpdateGameDataFormRightWrongMode
    success_url = "/teach"
    def get_object(self):
        return GameDataRightWrongMode.objects.get(slug=self.kwargs["slug"], user= User.objects.get(pk=3))

# class UpdateGameDataPairsModeView(generic.edit.UpdateView):
#     template_name = "games/update_game_pairs_mode.html"
#     # model = GameDataPairsMode
#     # fields = GameDataPairsMode.editable_fields()
#     form_class = UpdateGameDataFormPairsMode
#     success_url = "/teach"
#     def get_object(self):
#         return GameDataPairsMode.objects.get(slug=self.kwargs["slug"], user= self.request.user)
class UpdateGameDataPairsModeView(generic.edit.UpdateView):
    template_name = "games/update_game_pairs_mode.html"
    # model = GameDataPairsMode
    # fields = GameDataPairsMode.editable_fields()
    form_class = UpdateGameDataFormPairsMode
    success_url = "/teach"
    def get_object(self):
        return GameDataPairsMode.objects.get(slug=self.kwargs["slug"], user= User.objects.get(pk=3))

def update_game_data_redirection(request, slug):
    object = GameData.get_game(slug)
    if (object.mode == Game.RIGHT_WRONG):
        return redirect("http://"+request.get_host()+"/games/edit-game/right-wrong-mode/"+slug)
    else:
        return redirect("http://"+request.get_host()+"/games/edit-game/pairs-mode/"+slug)

class DeleteGameView(generic.edit.DeleteView):
    template_name = "games/delete_game.html"
    model = GameData
    success_url = "/teach"
    def get_context_data(self, **kwargs):
            context = super(DeleteGameView, self).get_context_data(**kwargs)
            context["game_data"] = GameData.objects.get(slug=self.kwargs["slug"])
            return context

class PreviewGameView(generic.detail.DetailView):
    template_name = "games/game_preview.html"
    model = GameData
    def get_context_data(self, **kwargs):
            context = super(PreviewGameView, self).get_context_data(**kwargs)
            context["game_data"] = GameData.objects.get(slug=self.kwargs["slug"])
            context["games"] = Game.objects.filter(mode=context["game_data"].mode)
            return context

def play_game_data(request, slug_data, slug_game):
    template = loader.get_template("games/game.html")
    return HttpResponse(template.render())
    # return render_to_response("games/game.html")

class PlayGameView(generic.TemplateView):
    template_name = "games/game.html"
    def get_context_data(self, **kwargs):
            context = super(PlayGameView, self).get_context_data(**kwargs)
            context["game_data"] = GameData.objects.get(slug=self.kwargs["slug_data"])
            context["game"] = Game.objects.get(slug=self.kwargs["slug_game"], mode=context["game_data"].mode)
            return context

def xml_game_data(request, slug):
    # data = serializers.serialize("xml", GameData.objects.all(), fields=("slug"))
    # response = HttpResponse(data)
    # response["Content-Type"] = "application/xml;"
    # return response
    object = GameData.get_game(slug)
    data = object.get_xml()
    response = HttpResponse(data)
    response["Content-Type"] = "application/xml;"
    return response
