import markdown2
from django import forms
from django.shortcuts import render,redirect

from . import util

class QueryForm(forms.Form):
    query = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": QueryForm()
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

def search(request):
    entries = util.list_entries()

    if request.method == "POST":
        form = QueryForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            if util.get_entry(query):
                return redirect("entry", title=query)
            results = [entry for entry in entries if query.lower() in entry.lower()]
            return render(request, "encyclopedia/search.html", {
                "query": query,
                "results": results,
                "form": form
            })
        else: 
            print(f"Form error: {form.errors}")
    
    return render(request, "encyclopedia/search.html", {
        "form": QueryForm()
    })