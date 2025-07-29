from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, RecruiterProfile, CandidateProgress

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Only superusers can assign admin role
        if not request.user.is_superuser:
            if 'role' in form.base_fields:
                form.base_fields['role'].choices = [
                    choice for choice in form.base_fields['role'].choices 
                    if choice[0] != 'ADMIN'
                ]
        return form

@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'num_candidates')
    search_fields = ('user__username', 'user__email')
    
    def num_candidates(self, obj):
        return obj.candidates.count()
    num_candidates.short_description = 'Assigned Candidates'

@admin.register(CandidateProgress)
class CandidateProgressAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'game_type', 'score', 'timestamp')
    list_filter = ('game_type', 'timestamp')
    search_fields = ('candidate__username', 'game_type')
    ordering = ('-timestamp',)
