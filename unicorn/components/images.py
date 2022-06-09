from django_unicorn.components import UnicornView, PollUpdate
from images.models import Images
from django.conf import settings
import datetime
from fpdf import FPDF
import os
from PIL import Image
import shutil
from django.shortcuts import redirect, render
from uuid import uuid4
from django.utils.timezone import now


class ImagesView(UnicornView):
    path = ''
    msg = ''
    current_time = now()

    
    def __init__(self,*args,**kwargs):
        super().__init__(**kwargs)
        self.path = ''
        self.msg = ''
        if self.request.FILES.getlist('images') != []:
            images=self.request.FILES.getlist('images')
            uuid = str(uuid4())
            for f in images:
                imageup=Images.objects.create(image=f, uuid=uuid)
                if not imageup.image.height:
                    os.remove(imageup.image.path)
                    imageup.delete()

            
            BASE_DIR = settings.BASE_DIR
            files=[]
            a = os.path.join(BASE_DIR, r'media/upload')
            now = datetime.datetime.now()
            date= now.strftime('%d-%m-%Y-%H-%M-%S')
            path= os.listdir(a)
            dirs=[]
            pdf=FPDF()
            files = Images.objects.filter(uuid=uuid)

            # for file in path:
            #     if ".jpg" in file or ".jpeg" in file or ".png" in file:
            #         dirr=r'{}/{}'.format(a,file)
            #         files.append(file)
            #         dirs.append(dirr)

            for file in files:
                dirs.append(file.image.path)

            if not files.exists():
                self.msg = 'Formato Inválido!'
                return

            for d in dirs:
                im = Image.open(d)
                width, height = im.size
                if height > width:
                    pdf.add_page('P')
                    pdf.image(d, 0, 0, 210, 297)
                else:
                    pdf.add_page('L')
                    pdf.image(d, 0, 0, 297, 210)
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

            self.path = '/'+file_pdf