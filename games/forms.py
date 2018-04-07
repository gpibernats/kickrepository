from django import forms
from games import models
from games.models import GameData, GameDataRightWrongMode, GameDataPairsMode


# class CreateGameDataForm(forms.ModelForm):
#     title = forms.CharField(label='Title', max_length=100)
#     description = forms.CharField(label='Description', max_length=200)
#     model = GameData
    # def create_game_data(self):
    #     game = GameData.objects.create(title='thetitle', description='thedescription')
    #     # game.save()



class UpdateGameDataFormRightWrongMode(forms.ModelForm):
    class Meta:
        model = GameDataRightWrongMode
        fields = GameDataRightWrongMode.editable_fields()
        widgets = {
            'right_words': forms.Textarea(attrs={'rows': 10, 'cols': 60}),
            'wrong_words': forms.Textarea(),
        }
        help_texts = {
            'title': 'What is the topic of your game?',
            'description': 'Short indication for players',
        }

class UpdateGameDataFormPairsMode(forms.ModelForm):
    class Meta:
        model = GameDataPairsMode
        fields = GameDataPairsMode.editable_fields()
        widgets = {
            'pairs': forms.Textarea(),
        }
        help_texts = {
            'title': 'What is the topic of your game?',
            'description': 'Short indication for players',
        }
