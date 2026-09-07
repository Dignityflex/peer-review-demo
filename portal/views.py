from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Paper, Review


def paper_list(request):
    query = request.GET.get('q', '').strip()
    if query:
        papers = Paper.objects.filter(title__icontains=query).order_by('-created_at')
    else:
        papers = Paper.objects.all().order_by('-created_at')
    return render(request, 'portal/paper_list.html', {'papers': papers, 'query': query})


def paper_detail(request, pk):
    paper = get_object_or_404(Paper, pk=pk)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        score = int(request.POST.get('score', 5))
        feedback = request.POST.get('feedback', '').strip()
        if feedback:
            Review.objects.update_or_create(
                paper=paper,
                reviewer=request.user,
                defaults={'score': score, 'feedback': feedback}
            )
            return redirect('paper_detail', pk=pk)

    return render(request, 'portal/paper_detail.html', {'paper': paper})


@login_required
def submit_paper(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        abstract = request.POST.get('abstract', '').strip()
        category = request.POST.get('category', 'General')
        pdf_url = request.POST.get('pdf_url', '').strip()

        if not title or not abstract:
            return render(request, 'portal/submit_paper.html', {
                'error': 'Title and abstract are required.'
            })

        Paper.objects.create(
            title=title,
            abstract=abstract,
            category=category,
            pdf_url=pdf_url if pdf_url else None,
            author=request.user
        )
        return redirect('paper_list')

    return render(request, 'portal/submit_paper.html')


@login_required
def delete_paper(request, pk):
    paper = get_object_or_404(Paper, pk=pk)
    # Strictly allow only staff or superusers
    if not (request.user.is_staff or request.user.is_superuser):
        raise PermissionDenied

    if request.method == 'POST':
        paper.delete()
        return redirect('paper_list')

    return redirect('paper_detail', pk=pk)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('paper_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})