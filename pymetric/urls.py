"""
URL configuration for pymetric project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render, redirect
from django.conf import settings
from django.conf.urls.static import static
from games import views as game_views
from behavioral_data.api_views import MetricExtractionAPIView
from ai_model.api_views import ReportGenerationAPIView

def home(request):
    if request.user.is_authenticated:
        role = getattr(request.user, 'role', None)
        if role == 'ADMIN':
            return redirect('admin_dashboard')
        elif role == 'RECRUITER':
            return redirect('recruiter_dashboard')
        elif role == 'CANDIDATE':
            return redirect('candidate_dashboard')
    return render(request, 'home.html')

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/behavioral/', include('behavioral_data.urls')),
    path('accounts/', include('accounts.urls')),
    path('games/', include('games.urls')),
    # Alias for global reverse lookup if needed
    path('game-list/', game_views.game_list, name='game_list'),
    path('api/metrics/extract/', MetricExtractionAPIView.as_view(), name='metric_extraction'),
    path('api/reports/generate/', ReportGenerationAPIView.as_view(), name='report_generation'),
    path('api/traits/', include('ai_model.urls')),
    path('api/', include('api.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
