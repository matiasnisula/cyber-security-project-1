from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import connection
from datetime import datetime
from .models import Publication


@login_required
def front_page_view(request):
    publications = Publication.objects.all()
    return render(request, "messageFrontPage.html", {"publications": publications})

#CSRF
#remove line below for csrf fix
@csrf_exempt
@login_required
def add_publication_view(request):
    if request.method == "POST":
        content = request.POST.get("content")
        #safe db insert below
        #Publication.objects.create(publisher=request.user, content=content)
        
        #sql injection
        sql = f"INSERT INTO messageapp_publication (published, publisher_id, content) VALUES ('{datetime.now()}', {request.user.id}, '{content}');"
        print("sql:", sql)
        cursor = connection.cursor()
        cursor.executescript(sql)
    
    return redirect("/messages")

#Broken access control
#@login_required
def delete_publication(request, id):
    publication = Publication.objects.get(id=id)

    publication.delete()
    #if (request.user == publication.publisher):
        #publication.delete()
        
    return redirect("/messages")