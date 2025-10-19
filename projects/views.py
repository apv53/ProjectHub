from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Project, Comments, Votes
from .forms import ProjectForm, CommentForm
from django.http import HttpResponseForbidden
from django.http import JsonResponse

def project_home(request):
    return render(request, 'home.html')

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    # Votes
    upvotes = project.votes.filter(values=1)
    downvotes = project.votes.filter(values=-1)

    # Comments
    comments = project.comments.all().order_by("-created_at")

    # Handle comment form submission
    if request.method == "POST" and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            comment.user = request.user
            comment.save()
            form = CommentForm()  # clear form after saving
    else:
        form = CommentForm()

    context = {
        "project": project,
        "upvotes": upvotes,
        "downvotes": downvotes,
        "comments": comments,
        "form": form,
    }
    return render(request, "projects/project_detail.html", context)

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('project_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    # Only the owner can delete
    if project.owner != request.user:
        return HttpResponseForbidden("You are not allowed to delete this project.")
    
    if request.method == "POST":
        project.delete()
        return redirect('project_list')
    
    return render(request, 'projects/project_confirm_delete.html', {'project': project})

@login_required
@require_POST
def project_vote(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    # Validate vote
    try:
        vote_value = int(request.POST.get('values'))
        if vote_value not in [1, -1]:
            return JsonResponse({'status': 'error', 'message': 'Invalid vote value'})
    except (ValueError, TypeError):
        return JsonResponse({'status': 'error', 'message': 'Invalid vote value'})

    # Create or update vote
    vote, created = Votes.objects.get_or_create(
        user=request.user, 
        project=project, 
        defaults={'values': vote_value}
    )

    if not created:
        if vote.values == vote_value:
            # Remove existing vote if clicked again
            vote.delete()
        else:
            # Update opposite vote
            vote.values = vote_value
            vote.save()

    # Return updated counts
    return JsonResponse({
        'status': 'ok',
        'upvotes': project.upvotes,
        'downvotes': project.downvotes
    })

@login_required
def add_comment(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        comment_text = request.POST.get("comment")
        if comment_text:
            Comments.objects.create(project=project, user=request.user, comment=comment_text)
        return redirect("project_detail", pk=project.pk)


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comments, pk=pk)
    project = get_object_or_404(Project, pk=pk)
    if comment.owner != request.owner:
        raise HttpResponseForbidden("You are not allowed to delete this comment!")
    
    if request.method == "POST":
        comment.delete()
        return redirect("project_detail", pk=project.pk)
    

