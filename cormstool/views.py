from django.shortcuts import render
from django.http import HttpResponse
import cormstool.corms.corms_controller as corms
import cormstool.corms.feedback as feedback
import os
import mimetypes
from django.conf import settings
import pymongo
import cormstool.corms.projects as projects

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
                ls,platform,project,inrev = corms.main_controller(upload,project,platform)
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
        filepath = BASE_DIR + '/cormstool/corms/files/' + filename
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