import markdown2
import random
from django import forms
from django.shortcuts import render,redirect

from . import util

class QueryForm(forms.Form):
    query = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={'cols': 100, 'rows': 15}))

class EditForm(forms.Form):
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={'cols': 100, 'rows': 15}))

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
    
    return render(request, "encyclopedia/search.html", {
        "form": QueryForm()
    })


def newEntry(request):
    message = "The entry already exists with the provided title"

    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"].capitalize()
            description = form.cleaned_data["description"]

            if title in util.list_entries():
                return render(request, "encyclopedia/error.html",{
                    "form": QueryForm(),
                    "message": message
                })
            else: 
                util.save_entry(title,description)
                return redirect('entry', title=title)

    return render(request, "encyclopedia/newPage.html", {
        "newEntryForm": NewEntryForm(),
        "form": QueryForm()
    })


def editEntry(request,title):
    description = util.get_entry(title)

    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data["description"]
            util.save_entry(title,description)
            return redirect('entry', title=title)

    return render(request, "encyclopedia/editPage.html", {
        "title": title,
        "editForm": EditForm(initial={'description': description}),
        "form": QueryForm()
    })

def randomEntry(request):
    entries = util.list_entries()

    if entries:
        randomEntry = random.choice(entries)
        return redirect('entry', title=randomEntry)
    else:
        return render(request, "encyclopedia/error.html", {
            "form": QueryForm(),
            "message": "No entries available."
        })