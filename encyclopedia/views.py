from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import markdown2
import re

from . import util

markdowner = markdown2.Markdown()

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
        entry_check = request.POST.get("new_entry")
        current_entries = util.list_entries()
        
        for entry in current_entries:
            if entry_check.lower() == entry.lower():
                return HttpResponse("This already exists")
        util.save_entry(entry_check, 'No content inserted yet...')
        return render(request, "encyclopedia/index.html")
            
    return render(request, "encyclopedia/add.html")