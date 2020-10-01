from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
import secrets

from django import forms

from . import util

class PageForm(forms.Form):
    title = forms.CharField(label = "Title")
    body = forms.CharField(label = "Page", widget=forms.Textarea)



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,title):
    content = util.get_entry(title)


    if  content is not None:
        return render(request,"encyclopedia/entry.html",{
            "title" : title ,
            "content" : markdown2.markdown(content)
            })
    return render(request,"encyclopedia/error.html",{
    "error" : "The page your are trying to access does not exisit "
    })

def search(request):
    if request.method == 'POST':

        entries = list(filter(lambda x : request.POST["q"].lower() in x.lower(),util.list_entries()))

        if len(entries) ==1 and entries[0].lower()== request.POST["q"].lower() :
            return entry(request,entries[0])

        return render(request, "encyclopedia/search.html", {
            "entries": entries
            })

def newpage(request):
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["title"] in util.list_entries():
                return render(request,"encyclopedia/error.html",{
                "error" : "The page you are trying to create already exisits "
                })
            else:
                util.save_entry(form.cleaned_data["title"],form.cleaned_data["body"])
                return entry(request,form.cleaned_data["title"])
        else:
            return render(request,"encyclopedia/newpage.html",{
            "form" : form
            })

    return render(request, "encyclopedia/newpage.html",{
    "form" : PageForm()
    })


def editpage(request,title):

    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            util.save_entry(form.cleaned_data["title"],form.cleaned_data["body"])

            return entry(request,title)
        else:
            return render(request,"encyclopedia/editpage.html",{
            "form" : form
            })
    return render(request, "encyclopedia/editpage.html",{
    "form" : PageForm({"title":title,"body":util.get_entry(title)})
    })


def random(request):

    return entry(request,secrets.choice(util.list_entries()))
