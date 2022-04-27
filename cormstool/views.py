from django.shortcuts import render
from django.http import HttpResponse
import cormstool.corms.corms_controller as corms
import cormstool.corms.feedback as feedback
import os
import mimetypes
from django.conf import settings
import pymongo
import cormstool.corms.projects as pros
from django.http import HttpResponseRedirect

def add_project(request):
    return render(request, 'template_addproject.html') 

def projects(request):
    client = pymongo.MongoClient(settings.DB_NAME)
    db = client['CORMS']
    proj_collection = db["Projects"]
    proj_s = proj_collection.find({"status":1})
    proj_r = proj_collection.find({"status":0})
    context = {"project_supported":proj_s,"project_requested":proj_r}
    proj = request.POST.get('project', False)
    if proj:
        project = request.POST['project']
        url = request.POST['url']
        platform = request.POST['platform']
        desc = request.POST['desc']
        if(pros.add_project(proj_collection,project,url,platform,desc)==True):
            notification = "New project request for " + project+ " is submitted successfully!"
            status = True
        else:
            notification = "Some error occured! Please try again later."
            status = False
        context = {"project_supported":proj_s,"project_requested":proj_r,"notification":notification,"status":status}
        return render(request, 'template_projects.html', context)
    return render(request, 'template_projects.html', context)    

def index(request):
    client = pymongo.MongoClient(settings.DB_NAME)
    db = client['CORMS']
    feed_collection = db["Feedback"]
    score,total,accuracy = feedback.check(feed_collection)
    feed = request.POST.get('feedback', False)
    if feed:
        ans = request.POST['feedback']
        project = request.POST['project']
        try:
            accuracy = feedback.update(ans,score,total,feed_collection,project)
            notification = "Thanks for giving us your valuable feedback!"
            status=True
            context = {'status':status,'feedback': feedback,"score":accuracy,'notification':notification}
        except:
            notification = "Some error occured! Please try again later."
            status=False
            context = {'status':status,'notification':notification,'feedback': feedback}
        return render(request, 'index.html', context)
    return render(request, 'index.html', {"score":accuracy})

def step1(request):
    return render(request, 'step1.html')

def step2(request):
    client = pymongo.MongoClient(settings.DB_NAME)
    db = client['CORMS']
    proj_collection = db["Projects"]
    if request.method == 'POST':
        platform = request.POST["platform"]
        proj_details = proj_collection.find({"platform":platform,"status":1})
        context = {"proj_details":proj_details,"platform":platform}
        return render(request, 'step2.html', context)
    return HttpResponseRedirect('/step/1/')

def step3(request):
    if request.method == 'POST':
        platform = request.POST["platform"]
        project = request.POST["project"]
        context = {"project":project,"platform":platform}
        return render(request, 'step3.html', context)
    return HttpResponseRedirect('/step/1/')

def results(request):
    client = pymongo.MongoClient(settings.DB_NAME)
    db = client['CORMS']
    if request.method == 'POST': 
        upload = request.FILES.get('upload', False)
        if upload:
            upload = request.FILES['upload']
            project = request.POST["project"]
            platform = request.POST["platform"]
            try:
                results,inrev = corms.main_controller(upload,project,platform,db)
                notification = "CORMS has successfully predicted reviewers for your new review request! CHECK RESULTS NOW!"
                status=True
                context = {
                    'status':status,'results': results,'platform':platform,'project':project,'inactive':inrev,'notification':notification                
                }
            except:
                status=False
                notification = "Some error occured! Please try again later."
                context = {'notification':notification,"status":status}
            return render(request, 'template_results.html', context)
    return render(request, 'template_results.html')

def upload(request):
    client = pymongo.MongoClient(settings.DB_NAME)
    db = client['CORMS']
    feed_collection = db["Feedback"]
    score,total,accuracy = feedback.check(feed_collection)
    if request.method == 'POST': 
        upload = request.FILES.get('upload', False)
        if upload:
            upload = request.FILES['upload']
            project = request.POST["projects"]
            platform = request.POST["platform"]
            try:
                ls,platform,project,inrev = corms.main_controller(upload,project,platform,db)
                notification = "CORMS has successfully predicted reviewers for your new review request! CHECK RESULTS NOW!"
                status=True
                context = {
                    'status':status,'score':accuracy,'results': ls,'platform':platform,'project':project,'inactive':inrev,'notification':notification                
                }
            except:
                status=False
                notification = "Some error occured! Please try again later."
                context = {'notification':notification,"status":status}
            return render(request, 'upload.html', context)
        else:
            feed = request.POST.get('feedback', False)
            if feed:
                ans = request.POST['feedback']
                project = request.POST['project']
                try:
                    accuracy = feedback.update(ans,score,total,feed_collection,project)
                    notification = "Thanks for giving us your valuable feedback!"
                    status=True
                    context = {'status':status,'feedback': feedback,"score":accuracy,'notification':notification}
                except:
                    notification = "Some error occured! Please try again later."
                    status=False
                    context = {'status':status,'notification':notification,'feedback': feedback}
                return render(request, 'upload.html', context)
            else:
                project = request.POST['project']
                url = request.POST['url']
                platform = request.POST['platform']
                proj_collection = db["Projects"]
                if(projects.add_project(proj_collection,project,url,platform)):
                    notification = "New project request for " + project+ " is submitted successfully!"
                    status = True
                else:
                    notification = "Some error occured! Please try again later."
                    status = False
                context = {'notification':notification,"status":status}
                return render(request, 'upload.html', context)
    return render(request, 'upload.html', {"score":accuracy})

def download_file(request,filename=''):
    if filename != '':
        # Define Django project base directory
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Define the full file path
        filepath = BASE_DIR + '/data/' + filename
        # Open the file for reading content
        path = open(filepath, 'rb')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        # Return the response value
        return response
    else:
        return render(request, 'upload.html')