from django.urls import path
from .views import (
    register_view, login_view, logout_view,
    candidate_dashboard, admin_dashboard, recruiter_dashboard,
    candidate_profile, admin_export_csv
)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/candidate/', candidate_dashboard, name='candidate_dashboard'),
    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/recruiter/', recruiter_dashboard, name='recruiter_dashboard'),
    path('profile/', candidate_profile, name='candidate_profile'),
    path('admin/export_csv/', admin_export_csv, name='admin_export_csv'),
] 