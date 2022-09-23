from django.contrib import admin
from . models import Voter_Registration, Nomination_list, Nomination_paper, Vote_Shedule, Member_Vote_Data, Chairman_Vote_Data
# Register your models here.
@admin.register(Voter_Registration)
class Voter_Registration_ModelAdmin(admin.ModelAdmin):
    list_display = ['username', 'village', 'zilla']
# Register your models here.
@admin.register(Nomination_list)
class Nomination_list_ModelAdmin(admin.ModelAdmin):
    list_display = ['candidate_name', 'position']
# Register your models here.
@admin.register(Nomination_paper)
class Nomination_paper_ModelAdmin(admin.ModelAdmin):
    list_display = ['id','name']

@admin.register(Vote_Shedule)
class Vote_Shedule_ModelAdmin(admin.ModelAdmin):
    list_display = ['id','vote_date']

@admin.register(Member_Vote_Data)
class Member_Vote_Data_ModelAdmin(admin.ModelAdmin):
    list_display = ['id','voter_name', 'candidate_name']

@admin.register(Chairman_Vote_Data)
class Chairman_Vote_Data_ModelAdmin(admin.ModelAdmin):
    list_display = ['id','voter_name', 'candidate_name']