from django.shortcuts import render
from django.http import HttpResponse
import cormstool.corms.corms_openstack as corms
import cormstool.corms.feedback as feedback
import os
import mimetypes

def upload(request):
    df,accuracy = feedback.check()
    if request.method == 'POST': 
        upload = request.FILES.get('upload', False)
        if upload:
            upload = request.FILES['upload']
            project = request.POST["projects"]
            platform = request.POST["platform"]
            ls,platform,project,inrev = corms.main_controller(upload,project,platform)
            context = {
                'score':accuracy,'results': ls,'platform':platform,'project':project,'inactive':inrev
            }
            return render(request, 'upload.html', context)
        else:
            ans = request.POST['feedback']
            accuracy = feedback.update(ans,df)
            context = {'feedback': feedback,"score":accuracy}
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