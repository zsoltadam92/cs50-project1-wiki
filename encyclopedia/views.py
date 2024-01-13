import markdown2
from django import forms
from django.shortcuts import render

from . import util

class QueryForm(forms.Form):
    query = forms.CharField(label="")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def getEntry(request,title):
    content = util.get_entry(title)
    form = QueryForm()
    message = "The page doesn't exist."

    if content:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdown2.markdown(content) ,
            "form": form,
        })
    else:
        return render(request, "encyclopedia/error.html",{
            "form": form,
            "message": message
        })
