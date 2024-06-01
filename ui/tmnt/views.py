from django.shortcuts import render
from .forms import UploadDFDFileForm
from .scripts.img_test import *
import io
import os
import subprocess

# base editor view
def test(request):
    # generate() # generate random color cat picture
    return render(request, "tmnt/test.html")

# view for uploading file
def upload_file(request):
    # checks to see if request method is POST which means form is submitted
    if request.method == 'POST':
        # request.POST has form data, request.FILE has file data
        fileform = UploadDFDFileForm(request.POST, request.FILES)

        # first, check that the user actually submitted something
        if fileform.is_valid():
            tm_file = None

            # if yes...
            # did they submit a file?
            if 'inputFile' in request.FILES.keys():
                # then get the file
                print("DEBUG >>>> using FILE")
                tm_file = request.FILES['inputFile'].file

            # # or did they submit via the textbox?
            else:
                # then get the text and treat it like a file
                print("DEBUG >>>> using TEXT")
                tm_file = io.BytesIO((request.POST['inputText']).replace('\r', '').encode('ascii'))

            # now save whatever they gave us to our own local file...
            DIR = os.path.dirname(__file__)
            with open(os.path.join(DIR, 'scripts', 'tm.py'), "wb") as f:
                f.write(tm_file.read())

            # ...and run pytm on it to generate a threat model image
            # run /mnt/c/Users/miraj/Desktop/study/capstone/ntmt_github/pytm_web/scripts/tm.py --dfd | dot -Tpng -o sample.png
            ps = subprocess.Popen((os.path.join(DIR, 'scripts', 'tm.py'), '--dfd'), stdout=subprocess.PIPE)
            _  = subprocess.check_output(('dot', '-Tpng', '-o', os.path.join(DIR, 'static', 'out.png')), stdin=ps.stdout)

            # os.remove(os.path.join(DIR, 'static', 'out.png'))

            # then render the new page
            return render(request, 'tmnt/dfd_viewer.html', {'fileform': fileform})

    else:
            # if request method is not POST, make an empty form
        fileform = UploadDFDFileForm()
            # renders template upload.html, passing in the form
            # NEED TO IMPLEMENT upload.html TEMPLATE
    return render(request, 'tmnt/dfd_viewer.html', {'fileform': fileform})

def asset_viewer(request):
    return render(request, "tmnt/asset_viewer.html")

################################################################################

# helper to convert a BytesIO to a TM object
# def process_tm_file(file, model_name="Threat Model"):
#     tm = TM(model_name)

#     return tm
