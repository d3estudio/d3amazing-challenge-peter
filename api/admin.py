from django.contrib import admin
from .models import Role, Score, User

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role', 'data_created')

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'score_technical', 'score_social', 'data_created')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('slack_user_id', 'role', 'active', 'data_created', 'data_updated')
