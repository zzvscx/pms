from django.shortcuts import render

def index(request):
    return render(request,'pms/index.html')

def about(request):
    return render(request,'pms/about.html')