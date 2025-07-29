from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import GameSession, GameResult

@login_required
def game_list(request):
    """Display the list of available games"""
    GAME_TYPES = [
        ('balloon_risk', 'Balloon Risk Game', 'Test your risk tolerance by inflating balloons', 'Risk Tolerance', '🎈', 'Inflate balloons to earn points, but be careful not to pop them! Each pump increases your score, but also the risk of popping. Find the right balance between risk and reward.'),
        ('money_exchange_1', 'Money Exchange Game #1', 'Test economic decision-making and trust', 'Economic Decision-Making', '💰', 'You have $10 each round. Decide how much to send to your partner. They will return a portion based on trust. Your goal is to maximize total earnings over multiple rounds.'),
        ('money_exchange_2', 'Money Exchange Game #2', 'Test economic decision-making and trust (variant)', 'Economic Decision-Making', '💵', 'Similar to Game #1, but with different partner behavior patterns. Learn to adapt your strategy based on your partner\'s trustworthiness across rounds.'),
        ('easy_or_hard', 'Easy or Hard Game', 'Choose between easy and hard tasks', 'Effort Allocation', '🎲', 'You\'ll see pairs of options: easy tasks with lower rewards and hard tasks with higher rewards. Choose based on your effort preferences and risk tolerance.'),
        ('cards_game', 'Cards Game (Iowa Gambling)', 'Test risk and reward learning', 'Risk/Reward Learning', '🃏', 'Choose cards from 4 different decks. Some decks have higher immediate rewards but long-term losses, others have lower rewards but better long-term outcomes. Learn which decks are most profitable.'),
        ('arrows_game', 'Arrows Game', 'Test spatial attention', 'Spatial Attention', '➡️', 'Arrows will appear pointing in different directions. Click the corresponding arrow key (left, right, up, down) as quickly and accurately as possible.'),
        ('lengths_game', 'Lengths Game', 'Test visual estimation', 'Visual Estimation', '📏', 'You\'ll see two lines of different lengths. Click on the longer line. The differences may be subtle, so pay close attention to visual details.'),
        ('keypresses', 'Keypresses Game', 'Test motor speed and accuracy', 'Motor Speed', '⌨️', 'Press the spacebar as quickly as possible when prompted. Your reaction time and consistency will be measured.'),
        ('faces_game', 'Faces Game', 'Test facial recognition', 'Facial Recognition', '🙂', 'You\'ll see a target face, then multiple faces. Click on the face that matches the target. Pay attention to facial features and expressions.'),
        ('letters', 'Letters Game', 'Identify and submit letters', 'Verbal Reasoning', '🔤', 'A letter will appear on screen. Type that exact letter as quickly and accurately as possible. Both speed and accuracy matter.'),
        ('magnitudes', 'Magnitudes Game', 'Estimate and submit magnitudes', 'Quantitative Reasoning', '📏', 'You\'ll be shown numerical values or quantities. Estimate and enter the correct magnitude. This tests your numerical reasoning and estimation skills.'),
        ('sequences', 'Sequences Game', 'Complete and submit sequences', 'Sequential Reasoning', '🔗', 'You\'ll see a sequence of numbers, letters, or patterns with one missing element. Identify the pattern and enter the missing item to complete the sequence.'),
        ('memory_cards', 'Memory Cards Game', 'Find matching pairs of cards', 'Working Memory', '🃏', 'Cards are placed face down. Click two cards to reveal them. If they match, they stay face up. Find all matching pairs to complete the game.'),
        ('reaction_timer', 'Reaction Timer Game', 'Test your reaction speed', 'Reaction Speed', '⚡', 'Wait for the screen to turn green, then click as quickly as possible. Don\'t click before it turns green, as this will count as an error.'),
        ('sorting_task', 'Sorting Task Game', 'Sort objects into categories quickly', 'Cognitive Flexibility', '📦', 'Objects will fall from the top. Sort them into the correct categories by clicking the appropriate bins. Categories may change during the game.'),
        ('pattern_completion', 'Pattern Completion Game', 'Complete number patterns', 'Pattern Recognition', '🔢', 'You\'ll see a sequence of numbers with one missing. Identify the mathematical pattern (addition, subtraction, multiplication, etc.) and choose the correct next number.'),
        ('stroop_test', 'Stroop Test Game', 'Test cognitive control and attention', 'Cognitive Control', '🎨', 'Words will appear in different colors. Click the color of the text, NOT what the word says. For example, if you see "RED" written in blue, click the blue button.'),
        ('tower_of_hanoi', 'Tower of Hanoi Game', 'Solve the classic puzzle', 'Planning & Problem Solving', '🗼', 'Move all disks from the left tower to the right tower. You can only move one disk at a time, and you cannot place a larger disk on top of a smaller one. Plan your moves carefully.'),
        ('emotional_faces', 'Emotional Faces Game', 'Identify facial expressions', 'Emotional Intelligence', '😊', 'You\'ll see faces showing different emotions. Choose the emotion that best matches the facial expression from the options provided.'),
        ('trust_game', 'Trust Game', 'Test trust and cooperation', 'Trust & Cooperation', '🤝', 'You\'ll be paired with different partners. Decide how much money to invest with each partner. Some partners are more trustworthy than others. Learn to identify and work with trustworthy partners.'),
        ('stop_signal', 'Stop Signal Game', 'Test impulse control', 'Impulse Control', '🛑', 'Press arrow keys to respond to directional cues. However, if you see a stop signal, you must stop pressing keys immediately. This tests your ability to control impulsive responses.'),
        ('digit_span', 'Digit Span Game', 'Test working memory capacity', 'Working Memory', '🔢', 'A sequence of numbers will be shown briefly. Remember the numbers and enter them in the correct order. Sequences get longer as you progress.'),
        ('fairness_game', 'Fairness Game', 'Test fairness perception', 'Fairness Perception', '⚖️', 'You\'ll see two people who have completed a task. Distribute money between them fairly based on their performance. Consider effort, outcome, and fairness principles.'),
        ('attention_network', 'Attention Network Game', 'Test your attention and focus', 'Attention Network', '🧠', 'You\'ll see cues and targets on screen. Respond to targets as quickly and accurately as possible. The cues may help or distract you - focus on the targets.'),
    ]

    games = []
    for gt in GAME_TYPES:
        game_type, name, description, trait, icon, instructions = gt
        result_qs = GameResult.objects.filter(user=request.user, game_type=game_type)
        games.append({
            'type': game_type,
            'name': name,
            'description': description,
            'trait': trait,
            'icon': icon,
            'instructions': instructions,
            'completed': result_qs.exists(),
            'score': result_qs.first().score if result_qs.exists() else None
        })
    
    context = {
        'games': games
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
def save_game_result(request):
    """Save game result from AJAX request"""
    try:
        data = json.loads(request.body)
        
        # Create game session
        session = GameSession.objects.create(
            user=request.user,
            is_completed=True
        )
        
        # Create game result
        result = GameResult.objects.create(
            user=request.user,
            session=session,
            game_type=data['game_type'],
            score=data['score'],
            duration=data['duration'],
            decisions=data.get('decisions', []),
            reaction_times=data.get('reaction_times', []),
            raw_data=data.get('raw_data', {})
        )
        
        return JsonResponse({
            'success': True,
            'result_id': result.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
