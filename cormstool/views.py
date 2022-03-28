from django.shortcuts import render
from django.http import HttpResponse
def demo(request):
    name="prahar"
    return HttpResponse(
        "<h1>CORMSTOOL</h1> <p>Created By: {0}".format(name))