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


def home(request):
    files=[]
    return render(request,'home.html',{'files':files})

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
        a = os.path.join(BASE_DIR, r'media/upload')
        now = datetime.datetime.now()
        date= now.strftime('%d-%m-%Y-%H-%M-%S')
        path= os.listdir(a)
        dirs=[]
        pdf=FPDF()
        for file in path:
            if ".jpg" in file or ".jpeg" in file or ".png" in file:
                dirr=r'{}/{}'.format(a,file)
                files.append(file)
                dirs.append(dirr)

        if files == []:
            return render(request,'Not.html')

        for d in dirs:
            im = Image.open(d)
            width, height = im.size
            pdf.add_page()
            pdf.image(d, 0, 0, 210, 297)
            im.close()

        pdf.output("temp-{}.pdf".format(date), "F")
        path=os.listdir(BASE_DIR)
        for p in path:
            if ".pdf" in p:
                file_pdf=r"media/upload/{}".format(p)
                shutil.move(p,a)

        path=os.listdir(a)

        for p in path:
            if ".pdf" in p:
                continue
            else:
                pasta=r"{}/{}".format(a,p)
                os.remove(pasta)
        

    return render(request,'home.html',{'file_pdf':file_pdf, 'files':files})


