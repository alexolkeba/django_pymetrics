from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone

class User(AbstractUser):
    ADMIN = 'ADMIN'
    RECRUITER = 'RECRUITER'
    CANDIDATE = 'CANDIDATE'
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        RECRUITER = 'RECRUITER', 'Recruiter'
        CANDIDATE = 'CANDIDATE', 'Candidate'
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CANDIDATE,
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recruiter_profile')
    candidates = models.ManyToManyField(User, related_name='assigned_recruiters', limit_choices_to={'role': User.Role.CANDIDATE})
    notes = models.TextField(blank=True, help_text='Private notes for this recruiter')

    def __str__(self):
        return f"Recruiter Profile: {self.user.username}"

class CandidateProgress(models.Model):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': User.Role.CANDIDATE})
    game_type = models.CharField(max_length=32)
    score = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.username} - {self.game_type} - {self.score}"

class CandidateProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='candidate_profile')
    position = models.CharField(max_length=128, blank=True)
    experience = models.CharField(max_length=32, blank=True)
    education = models.TextField(blank=True)
    skills = models.JSONField(default=list, blank=True)
    consent_given = models.BooleanField(default=False)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"CandidateProfile: {self.user.username}"
