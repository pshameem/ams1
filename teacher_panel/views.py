from django.shortcuts import render
from admin_panel.models import Batch,Student,Teacher,Subject,Login,Teacher_subject,Attendence
from ams.forms import SnapForm;
import cv2
from django.shortcuts import render,redirect
import numpy as np
import os
from datetime import datetime,timedelta
from django.http import HttpResponse
import json
from django.core import serializers

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def index(request):
    if request.session['user_id'] == None:
        return redirect('/')
    elif request.session['type'] != 'teacher':
        return redirect('/')
    return render(request,'teacher_index.html',{'message':"Message"})

def add_student(request):
    if request.session['user_id'] == None:
        return redirect('/')
    elif request.session['type'] != 'teacher':
        return redirect('/')
    return render(request,'studreg.html')

def manage_student(request):
    if request.session['user_id'] == None:
        return redirect('/')
    elif request.session['type'] != 'teacher':
        return redirect('/')
    return render(request,'mngstd.html')

def view_teacher(request):
    if request.session['user_id'] == None:
        return redirect('/')
    elif request.session['type'] != 'teacher':
        return redirect('/')
    return render(request,'teacher.html')

def snap(request):
    form = SnapForm()
    if request.method == 'POST':
        form = SnapForm(request.POST)
        if form.is_valid():
            batch = form.cleaned_data['batch']
            taken = datetime.now()
            subject = form.cleaned_data['subject']
            attendence = Attendence.objects.filter(taken_on=taken,batch_id=batch.id,subject_id_id=subject.id)
            if len(attendence) > 0  :
                return redirect('/teacher_panel/attendence?bid='+str(batch.id)+'&taken='+taken.strftime('%Y-%m-%d')+'&sid='+str(subject.id))
            faceDetect = cv2.CascadeClassifier(BASE_DIR+'/ml/haarcascade_frontalface_default.xml')

            cam = cv2.VideoCapture(0)
            # creating recognizer
            rec = cv2.face.LBPHFaceRecognizer_create()
            # loading the training data
            rec.read(BASE_DIR+'/ml/recognizer/'+batch.name+'/trainingData.yml')
            getId = 0
            font = cv2.FONT_HERSHEY_SIMPLEX
            userId = 0
            users = []
            while(True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = faceDetect.detectMultiScale(gray, 1.3, 5)
                for(x,y,w,h) in faces:
                    cv2.rectangle(img,(x,y),(x+w,y+h), (0,255,0), 2)

                    getId,conf = rec.predict(gray[y:y+h, x:x+w]) #This will predict the id of the face
                    
                    #print conf;
                    if conf<60:
                        userId = getId
                        student = Student.objects.get(id=userId)
                        if userId not in users:
                            users.insert(len(users)-1,userId)
                        cv2.putText(img, ""+str(student.name),(x,y+h), font, 2, (0,255,0),2)
                    else:
                        cv2.putText(img, "Unknown",(x,y+h), font, 2, (0,0,255),2)
                    # Printing that number below the face
                    # @Prams cam image, id, location,font style, color, stroke

                cv2.imshow("Face",img)
                if(cv2.waitKey(1) == ord('q')):
                    break
            students = Student.objects.filter(fk_batch_id=request.POST.get('batch'))

            for s in students:
                status = 0
                if s.id in users and s.status:
                    status=1
                Attendence.objects.create(
                    status=status,
                    taken_on = datetime.now(),
                    student_id = s,
                    subject_id = Subject.objects.get(id=request.POST.get('subject')),
                    teacher_id = Teacher.objects.get(fk_login_id=request.session['user_id']),
                    batch = batch,
                    updated_on = datetime.now()
                ) 
            cam.release()
            cv2.destroyAllWindows()
            return redirect('/teacher_panel/attendence?bid='+str(batch.id)+'&taken='+taken.strftime('%Y-%m-%d')+'&sid='+str(subject.id))
        # return render(request,'snap.html',{'success':True,'form':form})
    return render(request,'snap.html',{'form':form})

def attendence_today(request):
    if request.session['user_id'] == None:
        return redirect('/')
    elif request.session['type'] != 'teacher':
        return redirect('/')
    taken_on = request.GET.get('taken')
    batch = request.GET.get('bid')
    subject = request.GET.get('sid')
    attendence = Attendence.objects.filter(batch_id=batch,subject_id_id=subject,taken_on=taken_on)
    return render(request,'attendence_today.html',{'attendences':attendence})

def change_attendence(request):
    if request.session['user_id'] == None:
        return redirect('/')
    elif request.session['type'] != 'teacher':
        return redirect('/')
    attendence = Attendence.objects.get(id=request.GET.get('aid'))
    attendence.updated_on = datetime.now()
    attendence.status = not attendence.status
    attendence.save()
    attendences = Attendence.objects.filter(batch_id=attendence.batch_id,subject_id_id=attendence.subject_id_id,taken_on=attendence.taken_on)
    return redirect('/teacher_panel/attendence?bid='+str(attendence.batch_id)+'&taken='+attendence.taken_on.strftime('%Y-%m-%d')+'&sid='+str(attendence.subject_id_id))

def get_subjects_for_teacher(request):
    return_value = []
    teacher = Teacher.objects.get(fk_login_id=request.session['user_id'])
    data =Teacher_subject.objects.filter(teacher=teacher)
    i=0
    for d in data:
        return_value.insert(i,d.subject)
        i = i+1
    return_value = serializers.serialize('json', return_value)
    return HttpResponse(return_value, content_type ="application/json")