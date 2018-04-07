from django.contrib import admin
from .models import Game, GameData, GameDataRightWrongMode, GameDataPairsMode, Stats, GameDataStats, GameStats
# from django.contrib.auth.models import User


admin.site.register(Game)
class GameDataAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'mode')
admin.site.register(GameData, GameDataAdmin)
admin.site.register(GameDataRightWrongMode)
admin.site.register(GameDataPairsMode)
# class StatsAdmin(admin.ModelAdmin):
#     list_display = ('stats_id', 'total')
admin.site.register(Stats)
admin.site.register(GameStats)
# class GameDataStatsAdmin(admin.ModelAdmin):
#     list_display = ('stats_id', 'total')
admin.site.register(GameDataStats)
