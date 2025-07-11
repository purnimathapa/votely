from django.contrib import admin
from .models import Election, Candidate, Vote

@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'created_by')
    list_filter = ('start_date', 'end_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'start_date'

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'election', 'vote_count')
    list_filter = ('election',)
    search_fields = ('name', 'bio')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'candidate', 'election', 'timestamp')
    list_filter = ('election', 'timestamp')
    search_fields = ('voter__username', 'candidate__name', 'election__title')
    date_hierarchy = 'timestamp' 