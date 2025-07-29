from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .forms import UserRegistrationForm, CandidateProfileForm
from .models import User, RecruiterProfile, CandidateProgress, CandidateProfile
from games.models import GameSession, GameResult
from ai_model.models import TraitProfile
import json
from django.utils import timezone
import csv

@login_required
def admin_dashboard(request):
    if request.user.role != User.ADMIN:
        return redirect('home')
    # You can add admin-specific context here
    context = {
        'user': request.user,
    }
    return render(request, 'accounts/admin_dashboard.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .forms import UserRegistrationForm, CandidateProfileForm
from .models import User, RecruiterProfile, CandidateProgress, CandidateProfile
from games.models import GameSession, GameResult
from ai_model.models import TraitProfile
import json
from django.utils import timezone
import csv
from django.http import StreamingHttpResponse, HttpResponseForbidden

def home(request):
    if request.user.is_authenticated:
        if request.user.role == User.ADMIN:
            return redirect('admin_dashboard')
        elif request.user.role == User.RECRUITER:
            return redirect('recruiter_dashboard')
        else:
            return redirect('candidate_dashboard')
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.role == User.ADMIN:
                return redirect('admin_dashboard')
            elif user.role == User.RECRUITER:
                return redirect('recruiter_dashboard')
            else:
                return redirect('candidate_dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
    
    return render(request, 'accounts/login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.CANDIDATE  # Default role for new registrations
            user.save()
            login(request, user)
            return redirect('candidate_dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@csrf_exempt
@require_http_methods(["GET", "POST"])
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def candidate_dashboard(request):
    user = request.user
    user_results = GameResult.objects.filter(user=user)
    
    # List of all 20 games
    GAME_TYPES = [
        'balloon_risk', 'money_exchange_1', 'money_exchange_2', 'easy_or_hard', 'cards_game',
        'arrows_game', 'lengths_game', 'keypresses', 'faces_game', 'letters', 'magnitudes', 
        'sequences', 'memory_cards', 'reaction_timer', 'sorting_task', 'pattern_completion', 
        'stroop_test', 'tower_of_hanoi', 'emotional_faces', 'trust_game', 'stop_signal', 
        'digit_span', 'fairness_game', 'attention_network'
    ]
    total_games = len(GAME_TYPES)
    completed_games = user_results.filter(game_type__in=GAME_TYPES).count()
    progress_percentage = (completed_games / total_games) * 100 if total_games > 0 else 0

    # Calculate average score
    average_score = 0
    if user_results.exists():
        total_score = sum(result.score for result in user_results if result.game_type in GAME_TYPES)
        count = user_results.filter(game_type__in=GAME_TYPES).count()
        average_score = round(total_score / count) if count > 0 else 0

    # Calculate total time in minutes
    total_time = 0
    if user_results.exists():
        total_duration = sum(result.duration for result in user_results if result.game_type in GAME_TYPES)
        total_time = round(total_duration / 60) if total_duration > 0 else 0
    


    # Get recent games (last 3)
    recent_games = []
    for result in user_results.filter(game_type__in=GAME_TYPES).order_by('-completed_at')[:3]:
        recent_games.append({
            'game': {
                'name': result.get_game_name(),
                'trait': result.get_game_trait(),
                'icon': result.get_game_icon()
            },
            'score': result.score,
            'duration_minutes': round(result.duration / 60)
        })

    # Get AI profile if exists
    ai_profile = None
    try:
        trait_profile = TraitProfile.objects.get(session__user=user)
        ai_profile = {
            'overall_score': trait_profile.overall_score if hasattr(trait_profile, 'overall_score') else None,
            'overall_score_percentage': round(trait_profile.overall_score * 100) if hasattr(trait_profile, 'overall_score') else None,
            'recommendation': trait_profile.recommendation,
            'recommendation_display': getattr(trait_profile, 'get_recommendation_display', lambda: trait_profile.recommendation)(),
            'confidence': getattr(trait_profile, 'confidence', None),
            'confidence_percentage': round(trait_profile.confidence * 100) if hasattr(trait_profile, 'confidence') else None,
            'generated_at': trait_profile.created_at,
            'strengths': getattr(trait_profile, 'strengths', '').split(', ') if hasattr(trait_profile, 'strengths') and trait_profile.strengths else [],
            'weaknesses': getattr(trait_profile, 'weaknesses', '').split(', ') if hasattr(trait_profile, 'weaknesses') and trait_profile.weaknesses else [],
            'traits': []
        }
        # Parse traits from JSON
        if trait_profile.trait_scores:
            try:
                traits_data = json.loads(trait_profile.trait_scores)
                for trait_name, trait_data in traits_data.items():
                    ai_profile['traits'].append({
                        'name': trait_name.replace('_', ' ').title(),
                        'score': trait_data.get('score', 0),
                        'score_percentage': round(trait_data.get('score', 0) * 100),
                        'percentile': trait_data.get('percentile', 50),
                        'benchmark': trait_data.get('benchmark', 'average')
                    })
            except json.JSONDecodeError:
                pass
    except TraitProfile.DoesNotExist:
        pass

    context = {
        'user': user,
        'completed_games': completed_games,
        'total_games': total_games,
        'progress_percentage': round(progress_percentage),
        'average_score': average_score,
        'total_time': total_time,
        'recent_games': recent_games,
        'ai_profile': ai_profile,
        'game_types': GAME_TYPES
    }

    return render(request, 'accounts/candidate_dashboard.html', context)

@login_required
def recruiter_dashboard(request):
    if request.user.role != User.RECRUITER:
        return redirect('candidate_dashboard')

    try:
        recruiter_profile = RecruiterProfile.objects.get(user=request.user)
        assigned_candidates = recruiter_profile.candidates.all()
    except RecruiterProfile.DoesNotExist:
        assigned_candidates = []

    selected_candidate_id = request.GET.get('candidate_id')
    selected_candidate = None
    if selected_candidate_id:
        try:
            candidate = assigned_candidates.get(id=selected_candidate_id)
            try:
                profile = candidate.candidate_profile
            except CandidateProfile.DoesNotExist:
                profile = None
            from games.models import GameResult
            game_results = GameResult.objects.filter(user=candidate)
            game_results_list = [
                {
                    'game_id': gr.game_type,
                    'score': gr.score,
                    'duration_seconds': int(gr.timestamp.timestamp()),
                    'avg_reaction_time': getattr(gr, 'avg_reaction_time', 0),
                } for gr in game_results
            ]
            notes = ''
            if recruiter_profile.notes:
                notes = recruiter_profile.notes
            selected_candidate = {
                'id': candidate.id,
                'first_name': candidate.first_name,
                'last_name': candidate.last_name,
                'email': candidate.email,
                'profile': profile,
                'game_results': game_results_list,
                'notes': notes,
            }
        except User.DoesNotExist:
            selected_candidate = None

    # Handle notes saving
    if request.method == 'POST' and selected_candidate_id:
        notes = request.POST.get('notes', '')
        recruiter_profile.notes = notes
        recruiter_profile.save()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return redirect(f'?candidate_id={selected_candidate_id}')

    context = {
        'assigned_candidates': assigned_candidates,
        'selected_candidate': selected_candidate,
        'selected_candidate_id': selected_candidate_id,
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and selected_candidate_id:
        # Return only the candidateDetails partial for AJAX
        return render(request, 'accounts/recruiter_dashboard.html', context, content_type='text/html')
    return render(request, 'accounts/recruiter_dashboard.html', context)

@login_required
def candidate_profile(request):
    user = request.user
    try:
        profile = user.candidate_profile
    except CandidateProfile.DoesNotExist:
        profile = CandidateProfile.objects.create(user=user)

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = CandidateProfileForm(request.POST, request.FILES, instance=profile)
        # Parse skills JSON if present
        skills_json = request.POST.get('skills')
        if skills_json:
            try:
                form.data = form.data.copy()
                form.data['skills'] = json.loads(skills_json)
            except Exception:
                pass
        if form.is_valid():
            profile = form.save(commit=False)
            if profile.consent_given:
                profile.completed_at = timezone.now()
            profile.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': form.errors.as_json()})

    # GET: render profile page
    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'accounts/candidate_profile.html', context)

@login_required
def admin_export_csv(request):
    if request.user.role != User.ADMIN:
        return HttpResponseForbidden('Not authorized')
    
    # Prepare CSV header
    header = [
        'User ID', 'Email', 'First Name', 'Last Name', 'Position', 'Experience', 'Education', 'Skills', 'Consent', 'Resume', 'Video',
        'Games Completed', 'Game Results', 'AI Overall Score', 'AI Recommendation', 'AI Strengths', 'AI Weaknesses'
    ]
    
    def row_generator():
        yield header
        from .models import CandidateProfile
        from games.models import GameResult
        from ai_model.models import TraitProfile
        users = User.objects.filter(role=User.CANDIDATE)
        for user in users:
            try:
                profile = user.candidate_profile
            except CandidateProfile.DoesNotExist:
                profile = None
            try:
                ai = TraitProfile.objects.get(user=user)
            except TraitProfile.DoesNotExist:
                ai = None
            game_results = GameResult.objects.filter(user=user)
            games_completed = game_results.count()
            game_results_str = '; '.join([
                f"{gr.game_type}:{gr.score}" for gr in game_results
            ])
            row = [
                user.id, user.email, user.first_name, user.last_name,
                getattr(profile, 'position', ''),
                getattr(profile, 'experience', ''),
                getattr(profile, 'education', ''),
                ', '.join(getattr(profile, 'skills', [])) if profile else '',
                getattr(profile, 'consent_given', False),
                getattr(profile, 'resume', ''),
                getattr(profile, 'video', ''),
                games_completed,
                game_results_str,
                getattr(ai, 'overall_score', ''),
                getattr(ai, 'recommendation', ''),
                getattr(ai, 'strengths', ''),
                getattr(ai, 'weaknesses', ''),
            ]
            yield row
    
    pseudo_buffer = (','.join(map(str, row)) + '\n' for row in row_generator())
    response = StreamingHttpResponse(pseudo_buffer, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="candidates_export.csv"'
    return response
