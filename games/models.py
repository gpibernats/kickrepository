from django.db import models

from django.forms import ModelForm
from user_profiles.models import UserProfile
from django.contrib import admin
from django.template.defaultfilters import slugify
import xml.etree.cElementTree as ET
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from django.dispatch import receiver
import datetime



# Create your models here.
# class GameCollection(models.Model):
#     owner = models.OneToOneField(UserProfile)
#     name = models.CharField(max_length=100)


class Game(models.Model):
    RIGHT_WRONG = 'RW'
    PAIRS = 'PR'
    MODE_CHOICES = (
        (RIGHT_WRONG, 'Right-Wrong mode'),
        (PAIRS, 'Pairs mode'),
        # (TEST, 'Test mode'),
    )
    slug = models.SlugField(max_length=140)
    title = models.CharField(max_length=100)
    folder_name =  models.CharField(max_length=100, default="default")
    image_name = models.CharField(max_length=100, default="default.jpg")
    mode = models.CharField(max_length=5, choices=MODE_CHOICES)
    def __str__(self):
        return self.title + '(' + self.mode + ')'
    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     super(Game, self).save()



class GameData(models.Model):
    slug = models.SlugField(max_length=140, unique=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    mode = models.CharField(max_length=5, choices=Game.MODE_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # collection = models.ForeignKey(GameCollection)

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while GameData.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super(GameData, self).save()

    def __str__(self):
        return self.title

    def get_xml(self):
        root = ET.Element('game')
        ET.SubElement(root, 'title').text = self.title
        ET.SubElement(root, 'description').text = self.description
        return root

    @staticmethod
    def get_game(slug):
        object = None
        try:
            object = GameDataRightWrongMode.objects.get(slug=slug)
        except ObjectDoesNotExist:
            object = GameDataPairsMode.objects.get(slug=slug)
        return object



class GameDataRightWrongMode(GameData):
    right_words = models.CharField(max_length=500)
    wrong_words = models.CharField(max_length=500)

    def save(self, *args, **kwargs):
        self.mode = Game.RIGHT_WRONG
        super(GameDataRightWrongMode, self).save()

    @staticmethod
    def editable_fields():
        return ['title', 'description', 'right_words', 'wrong_words']
    def get_xml(self):
        root = GameData.get_xml(self)
        words = ET.SubElement(root, 'right-words')
        data = self.right_words.split('\n')
        for i in range(len(data)):
            ET.SubElement(words, 'word').text = data[i]
        words = ET.SubElement(root, 'wrong-words')
        data = self.wrong_words.split('\n')
        for i in range(len(data)):
            ET.SubElement(words, 'word').text = data[i]
        return ET.tostring(root, encoding="us-ascii", method="xml")



class GameDataPairsMode(GameData):
    pairs = models.CharField(max_length=500)

    def save(self, *args, **kwargs):
        self.mode = Game.PAIRS
        super(GameDataPairsMode, self).save()

    def get_xml(self):
        root = GameData.get_xml(self)
        data = self.pairs.split('\n')
        n_pairs = 0
        max_n_shorts = 0
        for i in range(len(data)):
            data_pair = data[i].split(';')
            pair = ET.SubElement(root, 'pair')
            ET.SubElement(pair, 'long').text = data_pair[0]
            data_pair = data_pair[1].split(',')
            n_shorts = 0
            for i in range(len(data_pair)):
                ET.SubElement(pair, 'short').text = data_pair[i]
                n_shorts += 1
            n_pairs += 1
            if (n_shorts > max_n_shorts):
                max_n_shorts = n_shorts
        meta = ET.SubElement(root, 'meta')
        ET.SubElement(meta, 'n-pairs').text = str(n_pairs)
        ET.SubElement(meta, 'max-n-shorts').text = str(max_n_shorts)
        return ET.tostring(root, encoding="us-ascii", method="xml")

    @staticmethod
    def editable_fields():
        return ['title', 'description', 'pairs']








class Stats(models.Model):
    stats_id = models.AutoField(primary_key=True)
    # game = models.OneToOneField(Game)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    times_played = models.IntegerField(default=0)

    def played(self):
        self.times_played+= 1


class GameStats(Stats):
    jan = models.IntegerField(default=0)
    feb = models.IntegerField(default=0)
    mar = models.IntegerField(default=0)
    apr = models.IntegerField(default=0)
    may = models.IntegerField(default=0)
    jun = models.IntegerField(default=0)
    jul = models.IntegerField(default=0)
    aug = models.IntegerField(default=0)
    sep = models.IntegerField(default=0)
    okt = models.IntegerField(default=0)
    nov = models.IntegerField(default=0)
    dec = models.IntegerField(default=0)

    def played(self):
        super(GameStats, self).played()
        month = datetime.datetime.today().month
        if month == 1:
            self.jan += 1
        elif month == 2:
            self.feb += 1
        elif month == 3:
            self.mar += 1
        elif month == 4:
            self.apr += 1
        elif month == 5:
            self.may += 1
        elif month == 6:
            self.jun += 1
        elif month == 7:
            self.jul += 1
        elif month == 8:
            self.aug += 1
        elif month == 9:
            self.sep += 1
        elif month == 10:
            self.okt += 1
        elif month == 11:
            self.nov += 1
        elif mont == 12:
            self.dec += 1


# @receiver(post_save, sender=Game)
# def create_game_data_stats(sender, instance, created, **kwargs):
#     if created:
#         GameStats.objects.create(game=instance)


class GameDataStats(Stats):
    # game_data = models.OneToOneField(GameData)
    game_data = models.ForeignKey(GameData, on_delete=models.CASCADE)
    max_score = models.IntegerField(default=0)
    average_score = models.FloatField(default=0)

    def add_score(self, score):
        score = int(score)
        if score > self.max_score:
            self.max_score = score
        self.average_score = (score + self.average_score*self.times_played)/(self.times_played+1)
        self.played()

    def get_max_score(self):
        return self.max_score

# @receiver(post_save, sender=GameDataRightWrongMode)
# def create_game_data_stats(sender, instance, created, **kwargs):
#     if created:
#         GameDataStats.objects.create(gameData=instance)
# @receiver(post_save, sender=GameDataPairsMode)
# def create_game_data_stats(sender, instance, created, **kwargs):
#     if created:
#         GameDataStats.objects.create(gameData=instance)
