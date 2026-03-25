from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import SelectTemplateForm


def select_template(request):
    if request.method == "POST":
        form = SelectTemplateForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("/thanks/")
    else:
        form = SelectTemplateForm()

    return render(request, "mailing/select-template.html", {"form": form})


