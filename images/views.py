from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse
from .models import Images
from django.template import RequestContext
from .forms import CreateImages
import os
from os import walk
from fpdf import FPDF
import datetime
import shutil
from PIL import Image
from django.conf import settings


def home(request):
    files = []
    context = {}
    if request.method == 'POST':
        #forms=CreateImages(request.POST)
        #data=request.POST
        images=request.FILES.getlist('images')
        for f in images:
            files.append(str(f))
            
    context['files'] = files
    return render(request,'home.html', context)


