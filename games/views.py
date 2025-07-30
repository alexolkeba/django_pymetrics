from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import GameSession, GameResult
from .utils import get_game_list_data

@login_required
def game_list(request):
    """Display the list of available games and progress"""
    GAME_TYPES = [
        ('balloon_risk', 'Adaptive Risk Challenge', 'Test your risk-taking behavior with an adaptive challenge.', 'Risk-Taking', '🎈', 'Pump the balloon to earn money. The more you pump, the more you can earn, but the risk of it bursting also increases. The game adapts to your playstyle. Cash out before it pops!'),
        ('money_exchange_1', 'Money Exchange Game #1', 'Test economic decision-making and trust', 'Economic Decision-Making', '💰', 'You have $10 each round. Decide how much to send to your partner. They will return a portion based on trust. Your goal is to maximize total earnings over multiple rounds.'),
        ('money_exchange_2', 'Money Exchange Game #2', 'Test economic decision-making and trust (variant)', 'Economic Decision-Making', '💵', 'Similar to Game #1, but with different partner behavior patterns. Learn to adapt your strategy based on your partner\'s trustworthiness across rounds.'),
        ('easy_or_hard', 'Easy or Hard Game', 'Choose between easy and hard tasks', 'Effort Allocation', '🎲', 'You\'ll see pairs of options: easy tasks with lower rewards and hard tasks with higher rewards. Choose based on your effort preferences and risk tolerance.'),
        ('cards_game', 'Cards Game (Iowa Gambling)', 'Test risk and reward learning', 'Risk/Reward Learning', '🃏', 'Choose cards from 4 different decks. Some decks have higher immediate rewards but long-term losses, others have lower rewards but better long-term outcomes. Learn which decks are most profitable.'),
        ('arrows_game', 'Arrows Game', 'Test spatial attention', 'Spatial Attention', '➡️', 'Arrows will appear in different directions. Click the corresponding arrow key (left, right, up, down) as quickly and accurately as possible.'),
        ('lengths_game', 'Lengths Game', 'Test visual estimation', 'Visual Estimation', '📏', 'You\'ll see two lines of different lengths. Click on the longer line. The differences may be subtle, so pay close attention to visual details.'),
        ('memory_cards', 'Spatial Working Memory Challenge', 'Test your spatial memory with an adaptive challenge.', 'Memory', '🧠', 'Find all matching pairs. The grid size adapts to your performance, testing the limits of your working memory.'),
        ('keypresses', 'Keypresses Game', 'Test motor speed and accuracy', 'Motor Speed', '⌨️', 'Press the spacebar as quickly as possible when prompted. Your reaction time and consistency will be measured.'),
        ('faces_game', 'Faces Game', 'Test facial recognition', 'Facial Recognition', '🙂', 'You\'ll see a target face, then multiple faces. Click on the face that matches the target. Pay attention to facial features and expressions.'),
        ('letters', 'Letters Game', 'Identify and submit letters', 'Verbal Reasoning', '🔤', 'A letter will appear on screen. Type that exact letter as quickly and accurately as possible. Both speed and accuracy matter.'),
        ('magnitudes', 'Numerical Acuity Challenge', 'Test your ability to distinguish between numerical quantities.', 'Quantitative Reasoning', '🔢', 'Choose the larger of two numbers. The difference between them will adapt based on your performance, measuring the precision of your number sense.'),
        ('reaction_timer', 'Temporal Reflex Challenge', 'Test your reaction speed with precision timing.', 'Reaction Speed', '⚡', 'Wait for the visual cue to change, then respond as quickly as possible. This challenge measures your raw reaction time and consistency under pressure.'),
        ('sorting_task', 'Cognitive Sorting Challenge', 'Test your ability to categorize objects based on changing rules.', 'Cognitive Flexibility', '🔄', 'Sort objects into categories. The sorting rule changes without warning, requiring you to adapt your strategy. This measures cognitive flexibility and rule inference.'),
        ('pattern_completion', 'Inductive Reasoning Challenge', 'Test your ability to identify and complete complex patterns.', 'Inductive Reasoning', '🧩', 'Identify the underlying rule in a sequence of items and predict the next one. The patterns increase in complexity, testing your abstract reasoning skills.'),
        ('stroop_test', 'Cognitive Inhibition Challenge', 'Test your ability to suppress automatic responses.', 'Cognitive Inhibition', '🎨', 'Name the color of the ink a word is printed in, while ignoring the word itself (e.g., the word “RED” printed in blue ink). This measures your ability to inhibit a prepotent response.'),
        ('tower_of_hanoi', 'Progressive Planning Task', 'Test your planning and problem-solving abilities.', 'Planning', '🗼', 'Move a stack of disks from one rod to another, following specific rules. This classic task measures your foresight and ability to break down a problem into smaller steps.'),
        ('emotional_faces', 'Facial Emotion Perception Task', 'Test your ability to recognize emotions in facial expressions.', 'Emotion Perception', '🎭', 'Identify the emotion conveyed by a series of faces. This task measures your accuracy and speed in perceiving social cues.'),
        ('trust_game', 'The Trust Dilemma', 'A multi-round game to assess your trust and reciprocity behavior.', 'Social Decision-Making', '🤝', 'Decide how much to entrust to a partner, who then decides how much to return. This game models trust and cooperation in economic interactions.'),
        ('stop_signal', 'Inhibitory Control Challenge', 'Test your ability to stop a planned action.', 'Inhibitory Control', '🛑', 'Respond quickly to a go signal, but withhold your response if a stop signal appears. This measures your reactive inhibition.'),
        ('digit_span', 'Working Memory Challenge', 'Test your verbal working memory capacity.', 'Working Memory', '🔢', 'Recall and repeat a sequence of digits. The length of the sequence increases, testing the limits of your short-term memory.'),
        ('fairness_game', 'Economic Fairness Challenge', 'Assess your sense of fairness in resource allocation.', 'Fairness & Altruism', '⚖️', 'Decide how to split a sum of money between yourself and another person. This game explores your preferences for equity and fairness.'),
        ('attention_network', 'Attention Control Challenge', 'A comprehensive test of the three attention networks.', 'Attention', '🎯', 'Respond to visual cues that test your alerting, orienting, and executive attention functions. This task provides a detailed profile of your attentional control.')
    ]

    user_results = GameResult.objects.filter(user=request.user)

    games = []
    completed_games_count = 0
    for game_type, name, description, trait, icon, instructions in GAME_TYPES:
        completed_result_qs = user_results.filter(game_type=game_type, completion_status='completed')
        is_completed = completed_result_qs.exists()
        if is_completed:
            completed_games_count += 1

        games.append({
            'type': game_type,
            'name': name,
            'description': description,
            'trait': trait,
            'icon': icon,
            'instructions': instructions,
            'completed': is_completed,
            'score': completed_result_qs.first().score if is_completed else None
        })

    total_games = len(GAME_TYPES)
    progress_percentage = (completed_games_count / total_games) * 100 if total_games > 0 else 0

    context = {
        'games': games,
        'completed_games': completed_games_count,
        'total_games': total_games,
        'progress_percentage': round(progress_percentage),
    }
    return render(request, 'games/game_list.html', context)

@login_required
def play_game(request, game_type):
    """Route to the appropriate game template"""
    game_templates = {
        'balloon_risk': 'games/balloon_risk.html',
        'memory_cards': 'games/memory_cards.html',
        'reaction_timer': 'games/reaction_timer.html',
        'sorting_task': 'games/sorting_task.html',
        'pattern_completion': 'games/pattern_completion.html',
        'stroop_test': 'games/stroop_test.html',
        'tower_of_hanoi': 'games/tower_of_hanoi.html',
        'emotional_faces': 'games/emotional_faces.html',
        'trust_game': 'games/trust_game.html',
        'stop_signal': 'games/stop_signal.html',
        'digit_span': 'games/digit_span.html',
        'fairness_game': 'games/fairness_game.html',
        'letters': 'games/letters.html',
        'magnitudes': 'games/magnitudes.html',
        'sequences': 'games/sequences.html',
        'money_exchange_1': 'games/money_exchange_1.html',
        'money_exchange_2': 'games/money_exchange_2.html',
        'easy_or_hard': 'games/easy_or_hard.html',
        'cards_game': 'games/cards_game.html',
        'arrows_game': 'games/arrows_game.html',
        'lengths_game': 'games/lengths_game.html',
        'keypresses': 'games/keypresses.html',
        'faces_game': 'games/faces_game.html',
        'attention_network': 'games/attention_network.html',
    }
    
    template_name = game_templates.get(game_type)
    if not template_name:
        return redirect('game_list')
    
    return render(request, template_name)

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def save_score(request):
    """Save game score and detailed event data from an AJAX request."""
    try:
        data = json.loads(request.body)

        # Flexible validation for redesigned games
        required_fields = ['game_name', 'score', 'completion_status', 'events']
        if not all(field in data for field in required_fields):
            return JsonResponse({'success': False, 'error': 'Missing required fields'}, status=400)

        # Create a game session
        session = GameSession.objects.create(
            user=request.user,
            is_completed=(data.get('completion_status') == 'completed')
        )

        # Determine duration from events if not provided directly
        duration_ms = data.get('duration_ms')
        if not duration_ms and data.get('events'):
            events = data['events']
            if len(events) > 1:
                start_time = events[0].get('timestamp')
                end_time = events[-1].get('timestamp')
                if start_time and end_time:
                    duration_ms = end_time - start_time
            if not duration_ms:
                 duration_ms = 0 # Fallback
        elif not duration_ms:
            duration_ms = 0 # Fallback

        # Create the game result
        result = GameResult.objects.create(
            user=request.user,
            session=session,
            game_type=data['game_name'],
            score=data['score'],
            duration=duration_ms,
            completion_status=data['completion_status'],
            decisions=data.get('events', []),
            raw_data=data.get('game_specific_data', data.get('raw_data', {}))
        )

        return JsonResponse({
            'success': True,
            'message': 'Result saved successfully',
            'result_id': result.id
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        # import logging
        # logging.exception(f"Error saving game result for user {request.user.id}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
