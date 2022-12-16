from django.shortcuts import render
from django.http import HttpResponse
import markdown2

from . import util

markdowner = markdown2.Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
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