from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import redirect, render

from main.forms import ProjectForm
from main.models import Experience, Project


def show_main(request):
    context = {
        "name": "Muhammad Eshan Bobby Bhaskara",
        "npm": "2506546333",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Information Systems student at Fasilkom UI with a growing "
            "interest in technology and its impact on society. Working "
            "collaboratively, thinking critically, and approaching problems "
            "with attention to detail."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Muhammad Eshan Bobby Bhaskara",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.order_by("display_order", "title")

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")


def show_projects(request):
    json_response = get_projects_json(request)
    serialized_projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [serialized_project.object for serialized_project in serialized_projects]

    context = {
        "name": "Muhammad Eshan Bobby Bhaskara",
        "project_list": projects,
        "title_query": request.GET.get("title", "").strip(),
    }
    return render(request, "projects.html", context)


def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Project added successfully!")
        return redirect("main:show_projects")

    context = {
        "name": "Muhammad Eshan Bobby Bhaskara",
        "form": form,
    }
    return render(request, "projects_form.html", context)
