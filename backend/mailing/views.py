from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import SelectTemplateForm, AddTagsForm


def select_template(request):
    if request.method == "POST":
        form = SelectTemplateForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("/thanks/")
    else:
        form = SelectTemplateForm()

    return render(request, "mailing/select-template.html", {"form": form})

def add_tags(request):
    if request.method == "POST":
        form = AddTagsForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("/thanks/")
        else:
            form = AddTagsForm()

    return render(request, "mailing/add-tags.html", {"form": form})
