from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import markdown2 as mdd
from django.urls import reverse
from django import forms
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title_page(request,title):
    req = util.get_entry(title)
    if req is None:
        return HttpResponse('<h2 align="center">PAGE NOT FOUND</h2>', status=404)
    else:
        htm_cont = mdd.markdown(req)
        return render(request, "encyclopedia/title.html", {"f_cont":htm_cont, "title_of_page":title})
 
def search(request):
    upd_list =[]
    lis = util.list_entries()
    query_param = request.GET.get('q', '')
    for word in lis:
        if query_param == word or query_param == word.lower():
            return HttpResponseRedirect(reverse('title', kwargs={'title':query_param}))
        elif query_param.lower()in word.lower():
            upd_list.append(word)
        #elif any(char in word.lower() for char in query_param.lower()):
           # upd_list.append(word)
        # this above commentened code can even match dased on asingtle alphabet
    
    if len(upd_list) == 0:
        return HttpResponse('<h2 align="center">NO MATCH FOUND </h2>')
    else:
        return render(request,"encyclopedia/search_result.html",{"itb_lis":upd_list})
    



class NewForm(forms.Form):
    name= forms.CharField(label="Name")
    Text = forms.CharField(label="Text",widget=forms.Textarea(attrs={"rows":10, "cols":10, "placeholder":"enter your md text here.."}))



def create_page(request):
   # POST OR GET MUST BE IN UPPERCASE#
   # Getting the name and content#
   if request.method=="GET":
       return render(request,"encyclopedia/create_page.html",{"form":NewForm()})
   if request.method=="POST":
     lis =util.list_entries()
     param1 = request.POST.get('name','')
     cont = request.POST.get('Text','')

# checking if file file already exist or not #
     if param1.lower() in [entery.lower() for entery in lis]:
        return HttpResponse('''<h3>Error!</h3>
        <br>
        <h5> The File with same name already exists </h5>''')
   

    #save the file#
     util.save_entry(param1,cont)

    
    # redirecting
     return HttpResponseRedirect(reverse('title',kwargs={'title':param1})) 


def edit(request, namy):
    if request.method=='GET':
        edit_cont = util.get_entry(namy)
        return render(request,"encyclopedia/edit_page.html",{"form":NewForm(initial={"name": namy,"Text":edit_cont}), "lnk": namy})


    if request.method=='POST':
        form = NewForm(request.POST)
        # request.POST fills form with user submitted data and newform() creates instance so that django can validate
        if form.is_valid():
            context = form.cleaned_data["Text"]
            Name = form.cleaned_data["name"]
            if Name == namy:
              util.save_entry(namy,context)
            else:
              util.del_entry(namy)
              util.save_entry(Name,context)
            return HttpResponseRedirect(reverse('title',kwargs={'title':Name}))
        else:
            return render(request,"encyclopedia/edit_page.html",{"form":form})
        

def random_generator(request):
    ran_lis = util.list_entries()
    my_elem =random.choice(ran_lis)
    return HttpResponseRedirect(reverse('title', kwargs={'title': my_elem}))
   