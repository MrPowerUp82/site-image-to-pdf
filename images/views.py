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


def home(request):
    return render(request,'home.html')

# Create your views here.
def upload(request):
    if request.method == 'POST':
        #forms=CreateImages(request.POST)
        #data=request.POST
        images=request.FILES.getlist('images')
        for f in images:
            imageup=Images.objects.create(image=f)

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        files=[]
        a = os.path.join(BASE_DIR, 'media\\upload')
        now = datetime.datetime.now()
        date= now.strftime('%d-%m-%Y-%H-%M-%S')
        path= os.listdir(a)
        dirs=[]
        pdf=FPDF()
        for file in path:
            if ".jpg" in file or ".jpeg" in file or ".png" in file:
                dirr='{}\{}'.format(a,file)
                files.append(file)
                dirs.append(dirr)

        for d in dirs:
            pdf.add_page()
            pdf.image(d, 0, 0, 210, 297)

        pdf.output("temp-{}.pdf".format(date), "F")
        path=os.listdir(BASE_DIR)
        for p in path:
            if ".pdf" in p:
                file_pdf="media\\upload\\{}".format(p)
                shutil.move(p,a)
        for d in dirs:
            os.remove(d)

        

    return render(request,'Sucess.html',{'file_pdf':file_pdf})


