from django.shortcuts import get_object_or_404, redirect, render
from projects.models import Donation, Project, Rating
from registration.forms import ProjectForm
from registration.models import MyUser
from django.db.models import Q, Avg

# Create your views here.

def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    average_rating = Rating.objects.filter(project=project).aggregate(avg_rating=Avg('value'))['avg_rating']

    return render(
        request,
        "projects/project_detail.html",
        {"project": project, "average_rating": average_rating},
    )

def donate(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        amount = request.POST.get("amount")  
        user_email = request.session.get("user_email")
        user = MyUser.objects.get(email=user_email)
        donation = Donation.objects.create(
            project=project, user=user, amount=amount
        )
        return redirect("project_detail", project_id=project.id)
    return render(request, "projects/donate.html", {"project": project})


def create_project(request):
    if request.method == "POST":
        project_form = ProjectForm(request.POST, request.FILES)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            user_email = request.session.get("user_email")
            if user_email:
                user = MyUser.objects.get(email=user_email)
                project.owner = user
            project.save()
            return redirect("project_detail", project_id=project.id)
        else:
            pass
    else:
        project_form = ProjectForm()
    return render(
        request,
        "projects/create_project.html",
        {"project_form": project_form}
    )

def rate_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        rating_value = request.POST.get('rating')
        
        user_email = request.session.get("user_email")
        user = MyUser.objects.get(email=user_email)
        
        rating = Rating.objects.create(project=project, user=user, value=rating_value)

    return redirect('project_detail', project_id=project.id)

def search_projects(request):
    query = request.GET.get('query')

    if query:
        projects = Project.objects.filter(Q(title__icontains=query) | Q(category__name__icontains=query))
    else:
        projects = Project.objects.all()

    return render(request, 'projects/search_results.html', {'projects': projects})
