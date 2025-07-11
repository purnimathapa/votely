from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count
from django.utils import timezone
from .models import Election, Candidate, Vote
from .forms import ElectionForm, CandidateForm, VoteForm

def is_admin(user):
    return user.is_staff

@login_required
def election_list(request):
    elections = Election.objects.all()
    return render(request, 'elections/election_list.html', {'elections': elections})

@login_required
@user_passes_test(is_admin)
def election_create(request):
    if request.method == 'POST':
        form = ElectionForm(request.POST)
        if form.is_valid():
            election = form.save(commit=False)
            election.created_by = request.user
            election.save()
            messages.success(request, 'Election created successfully.')
            return redirect('election_detail', pk=election.pk)
    else:
        form = ElectionForm()
    return render(request, 'elections/election_form.html', {'form': form, 'title': 'Create Election'})

@login_required
def election_detail(request, pk):
    election = get_object_or_404(Election, pk=pk)
    candidates = election.candidates.all()
    user_has_voted = Vote.objects.filter(voter=request.user, election=election).exists()
    
    if request.method == 'POST' and not user_has_voted and election.is_active:
        print('DEBUG: election =', election)
        form = VoteForm(request.POST, election=election, voter=request.user)
        if form.is_valid():
            vote = form.save(commit=False)
            print('DEBUG: vote.election after form.save =', vote.election)
            print('DEBUG: vote.voter after form.save =', vote.voter)
            vote.full_clean()
            vote.save()
            messages.success(request, 'Your vote has been recorded.')
            return redirect('election_detail', pk=pk)
        else:
            print('DEBUG: form.errors =', form.errors)
    else:
        form = VoteForm(election=election, voter=request.user) if election.is_active else None
    
    context = {
        'election': election,
        'candidates': candidates,
        'form': form,
        'user_has_voted': user_has_voted,
    }
    return render(request, 'elections/election_detail.html', context)

@login_required
@user_passes_test(is_admin)
def election_edit(request, pk):
    election = get_object_or_404(Election, pk=pk)
    if request.method == 'POST':
        form = ElectionForm(request.POST, instance=election)
        if form.is_valid():
            form.save()
            messages.success(request, 'Election updated successfully.')
            return redirect('election_detail', pk=pk)
    else:
        form = ElectionForm(instance=election)
    return render(request, 'elections/election_form.html', {'form': form, 'title': 'Edit Election'})

@login_required
@user_passes_test(is_admin)
def election_delete(request, pk):
    election = get_object_or_404(Election, pk=pk)
    if request.method == 'POST':
        election.delete()
        messages.success(request, 'Election deleted successfully.')
        return redirect('dashboard')
    return render(request, 'elections/election_confirm_delete.html', {'election': election})

@login_required
@user_passes_test(is_admin)
def candidate_create(request, election_pk):
    election = get_object_or_404(Election, pk=election_pk)
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.election = election
            candidate.save()
            messages.success(request, 'Candidate added successfully.')
            return redirect('election_detail', pk=election_pk)
    else:
        form = CandidateForm()
    return render(request, 'elections/candidate_form.html', {
        'form': form,
        'election': election,
        'title': 'Add Candidate'
    })

@login_required
@user_passes_test(is_admin)
def candidate_edit(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES, instance=candidate)
        if form.is_valid():
            form.save()
            messages.success(request, 'Candidate updated successfully.')
            return redirect('election_detail', pk=candidate.election.pk)
    else:
        form = CandidateForm(instance=candidate)
    return render(request, 'elections/candidate_form.html', {
        'form': form,
        'election': candidate.election,
        'title': 'Edit Candidate'
    })

@login_required
@user_passes_test(is_admin)
def candidate_delete(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    election_pk = candidate.election.pk
    if request.method == 'POST':
        candidate.delete()
        messages.success(request, 'Candidate deleted successfully.')
        return redirect('election_detail', pk=election_pk)
    return render(request, 'elections/candidate_confirm_delete.html', {'candidate': candidate})

@login_required
def election_results(request, pk):
    try:
        election = get_object_or_404(Election, pk=pk)
        candidates = election.candidates.all()
        total_votes = sum(c.vote_count for c in candidates)
        
        # Debug logging
        print(f"Election: {election.title}")
        print(f"Total votes: {total_votes}")
        print(f"Candidates: {[c.name for c in candidates]}")
        print(f"Vote counts: {[c.vote_count for c in candidates]}")
        
        # Debugging the is_ajax query parameter
        print(f"is_ajax query parameter: {request.GET.get('is_ajax')}")

        if request.GET.get('is_ajax') == 'true':
            data = {
                'labels': [c.name for c in candidates],
                'votes': [c.vote_count for c in candidates]
            }
            print(f"AJAX response data: {data}")
            return JsonResponse(data)
        
        return render(request, 'elections/election_results.html', {
            'election': election,
            'candidates': candidates,
            'total_votes': total_votes
        })
    except Exception as e:
        print(f"Error in election_results view: {str(e)}")
        if request.GET.get('is_ajax') == 'true':
            return JsonResponse({'error': str(e)}, status=500)
        messages.error(request, f"Error loading results: {str(e)}")
        return redirect('dashboard')

@login_required
def dashboard(request):
    if request.user.is_staff:
        # Admin sees all elections
        elections = Election.objects.all().order_by('-start_date')
    else:
        # Regular users see all active elections
        now = timezone.now()
        elections = Election.objects.filter(
            start_date__lte=now,
            end_date__gte=now
        ).order_by('-start_date')
        
        # Get the user's votes to show voting status
        user_votes = Vote.objects.filter(voter=request.user).values_list('election_id', flat=True)
        
    context = {
        'elections': elections,
        'user_votes': user_votes if not request.user.is_staff else None
    }
    return render(request, 'elections/dashboard.html', context) 