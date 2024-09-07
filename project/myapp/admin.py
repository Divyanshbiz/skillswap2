from django.contrib import admin
from .models.Member import Member
from .models.VideoConference import VideoConference

class MemberAdmin(admin.ModelAdmin):
    list_display = ("username", "firstname", "lastname", "email", "password")

class VideoConferenceAdmin(admin.ModelAdmin):
    list_display = ('title', 'host', 'category', 'created_at', 'is_active')  # Ensure created_at is a field in the model
    search_fields = ('title', 'host__username', 'category')
    list_filter = ('is_active', 'created_at')  # Ensure created_at is a field in the model


admin.site.register(Member, MemberAdmin)
admin.site.register(VideoConference, VideoConferenceAdmin)

