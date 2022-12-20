from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
import re
import random

from . import util

markdowner = markdown2.Markdown()

#The form for a new entry
class NewEntryForm(forms.Form):
    entry = forms.CharField(label="New Entry")
    
class NewEditingForm(forms.Form):
    body_content = forms.CharField(widget=forms.Textarea(attrs={ "size":30 }), label="", initial="Test")

def index(request):
    '''
    Outputs the home page with all list entries stored
    '''
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "result_type": "All Pages"
    })

def entry_info(request, entry):
    '''
    Get the entry and display it's contents on a page called entry.html
    Does this by converting markdown content using Python library
    '''
    if util.get_entry(entry):
        body = markdowner.convert(util.get_entry(entry))
        return render(request, "encyclopedia/entry.html", {
            "title":entry,
            "body": body
        })
    else:
        return render(request, "encyclopedia/404.html")

def search(request):
    '''
    Loop through all entries and check if search matches an entry
    If yes, deliver the entry page and not a search results page
    Else, return results page with all entries that cotain query as substring.
    '''
    current_query = request.GET.get('q')
    all_entries = util.list_entries()
    result_entries = []
    
    for entry in all_entries:
        if current_query.lower() == entry.lower():
            return entry_info(request, entry)
        elif re.search(current_query.lower(), entry.lower()):
            result_entries.append(entry)
        else: pass
        
    return render(request, "encyclopedia/index.html", {
        "entries": result_entries,
        "result_type": f"Search results for '{current_query}'"
    })
    
def add(request):
    '''
    Take request from add.html
    If it's a first load with no post request, send standard add.html page
    If it's a post method, take the content
        If entry already exists within database, return a add.html with an error
        that it already exists in the database
        
        Else, add it to the database with content of 'No content inserted yet'
        and redirect the user to the home page
    '''
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
    
def edit(request, entry):
    if request.method == "POST":
        form = NewEditingForm(request.POST)
        if form.is_valid():
            body_form = form.cleaned_data["body_content"]
            util.save_entry(entry, body_form)
            return entry_info(request, entry)
            
    
    elif util.get_entry(entry):
        form = NewEditingForm()
        form.fields['body_content'].initial = util.get_entry(entry)
        return render(request, "encyclopedia/edit.html", {
            "title":entry,
            "body":form
        })
    else:
        return render(request, "encyclopedia/404.html")
    
def random_entry(request):
    all_entries = util.list_entries()
    winner = random.choice(all_entries)
    return entry_info(request, winner)