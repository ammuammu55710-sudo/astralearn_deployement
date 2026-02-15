from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from doubt_ai.models import DoubtHistory
from notes.models import Note
from groups.models import UserGroupProgress

@login_required
def dashboard(request):
    user = request.user
    # Simplified groups list to prevent potential attribute errors during refactoring
    groups = user.study_groups.all()
    
    # Analytics
    doubts_count = DoubtHistory.objects.filter(user=user).count()
    total_notes = Note.objects.filter(author=user).count()
    
    # Calculate group completion average
    total_completion = 0
    group_progress = UserGroupProgress.objects.filter(user=user)
    
    for p in group_progress:
        if p.group and p.group.ai_schedule:
            try:
                total_days = len(p.group.ai_schedule)
                if total_days > 0:
                    completed = len(p.completed_days)
                    total_completion += (completed / total_days) * 100
            except:
                continue
    
    avg_completion = int(total_completion / group_progress.count()) if group_progress.count() > 0 else 0
    
    context = {
        'user': user,
        'groups': groups,
        'doubts_count': doubts_count,
        'total_notes': total_notes,
        'avg_completion': avg_completion,
        'recent_groups': groups[:3]
    }
    return render(request, 'dashboard/dashboard.html', context)
