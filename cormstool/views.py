from django.shortcuts import render
from django.http import HttpResponse
import cormstool.corms.corms_openstack as corms
from django.core.files.storage import FileSystemStorage

def geeks_view(request):
    # create a dictionary to pass
    # data to the template
    context ={
        "data":"Gfg is the best",
        "list":[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    }
    # return response with template and context
    return render(request, "geeks.html", context)

def upload(request):
    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']
        project = request.POST["projects"]
        platform = request.POST["platform"]
        ls,platform,project = corms.main_controller(upload,project,platform)
        # return HttpResponse(
        # "<h1>CORMSTOOL</h1> <p>results: {0}".format(ls))
        # fss = FileSystemStorage()
        # file = fss.save(upload.name, upload)
        # file_url = fss.url(file)
        return render(request, 'upload.html', {'results': ls,'platform':platform,'project':project})
    return render(request, 'upload.html')

def home(request):
    return render(request, 'home.html')

def demo(request):
    name="prahar"
    ls = corms.main_controller()
    # print("hiii")
    # return HttpResponse()
    return HttpResponse(
        "<h1>CORMSTOOL</h1> <p>results: {0}".format(ls))