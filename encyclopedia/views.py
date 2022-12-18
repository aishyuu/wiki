from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import markdown2
import re

from . import util

markdowner = markdown2.Markdown()

class NewEntryForm(forms.Form):
    entry = forms.CharField(label="New Entry")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "result_type": "All Pages"
    })

def entry_info(request, entry):
    if util.get_entry(entry):
        body = markdowner.convert(util.get_entry(entry))
        return render(request, "encyclopedia/entry.html", {
            "title":entry,
            "body": body
        })
    else:
        return render(request, "encyclopedia/404.html")
    
def search(request):
    current_query = request.GET.get('q')
    all_entries = util.list_entries()
    result_entries = []
    
    for entry in all_entries:
        if re.search(current_query.lower(), entry.lower()):
            result_entries.append(entry)
        else: pass
        
    return render(request, "encyclopedia/index.html", {
        "entries": result_entries,
        "result_type": f"Search results for '{current_query}'"
    })
    
def add(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        current_entries = util.list_entries()
        
        if form.is_valid():
            entry_form = form.cleaned_data["entry"]
            for entry in current_entries:
                if entry.lower() == entry_form.lower():
                    return render(request, "encyclopedia/add.html", {
                        "form":form,
                        "error_message":f"The entry {entry_form} already exists!"
                    })
            util.save_entry(entry_form, 'No content inserted yet...')
            return HttpResponseRedirect(reverse("encyclopedia:index"))
            
    return render(request, "encyclopedia/add.html", {
        "form": NewEntryForm(),
        "error_message":""
    })