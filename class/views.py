import io

import face_recognition
from django.utils import timezone

from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password,check_password
from django.utils.datastructures import MultiValueDictKeyError
from requests import request
from django.urls import path, include
from rest_framework.parsers import JSONParser
from rest_framework.utils import json

from .models import teacher, student, Class, Material, Question, Image, readingReview, Answer
from django.utils.crypto import get_random_string #for random class code generator
from django.contrib import messages
import requests
import smtplib
import os
#for face detection
import os
# import cv2
#for face detection
import numpy as np
from rest_framework.decorators import api_view #for api
from rest_framework.response import Response #for api
from .serializers import postSerializers,studentSerializers,teacherSerializers,classSerializers #for api
from rest_framework.renderers import JSONRenderer
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.
def home(request):
    if request.session.get('email'):
        return redirect("/home")
    else:
        return redirect("/signin")
#for homepage
def homeView(request):
    if request.session.get('email'):
        print("You are ", request.session.get('email'))
        print("You id ", request.session.get('teacher_id'))
        if request.session.get('teacher_id'):
            data=Class.objects.filter(teacherId=request.session.get('teacher_id'))
            data1 = teacher.objects.get(id=request.session.get('teacher_id'))
            return render(request, "home.html", {"detail":data,"profile":data1})
        elif request.session.get('student_id'):
            print("You id ", request.session.get('student_id'))
            studentId = student.objects.get(id=request.session.get('student_id'))
            data=studentId.classJoin.all()

            # com=readingReview.objects.filter(studentId=request.session.get('student_id'))
            incom=readingReview.objects.filter(studentId=request.session.get('student_id'),status='incomplete')
            com = readingReview.objects.filter(studentId=request.session.get('student_id'),status='complete')
            # print(com)
            return render(request, "home.html", {"detail":data,"profile":studentId,"complete":com,"incomplete":incom})
    else:
        return redirect('/signin')
      
# for sign in
def SigninView(request):
    if request.method == "POST":
        print("success")
        email = request.POST.get('Email')
        pass1 = request.POST.get('Password')
        isStudent= request.POST.get('isStudent')
        try:
            if(isStudent=="false"):

                user = teacher.objects.get(Email=email)
            else:
                user = student.objects.get(Email=email)
        except:
            print("incorrect")
            messages.info(request, "User doesn't exist!!!")
            return render(request, "signin.html", {})
        if (user.Email == email):
            print("correct email")
            if(check_password(pass1,user.Password)):
                print("correct password")

                request.session['email']=user.Email
                request.session['name2'] =user.Lname
                if (isStudent == "false"):
                    request.session['teacher_id'] = user.id
                else:
                    request.session['student_id'] = user.id
                return redirect('/home')
            else:
                print("icorrect password")
                messages.info(request, "Incorrect password!!!")
                return redirect('/signin')
        else:
            print("Wrong email address!!!")
            messages.info(request, "Wrong email address!!!")
            return render(request, "signin.html", {})

    if request.session.get('email'):
        return redirect('/home')
    else:
        return render(request,"signin.html",{})
#for signout
def signoutView(request):
    request.session.clear()
    return redirect('/home')
#for signup
def SignupView(request):
    if request.method == "POST":
        Fname = request.POST.get('Fname')
        Lname = request.POST.get('Lname')
        Email = request.POST.get('Email')
        AccountType = request.POST.get('AccountType')
        image = request.FILES['image']
        if (AccountType == "teacher"):
            try:

                user = teacher.objects.get(Email=Email)
                messages.info(request, "Email already exist!!!")
                return render(request, "signup.html", {})
            except:


                Password = make_password(request.POST.get('Password'))
                signup = teacher(Fname=Fname, Lname=Lname, Email=Email, AccountType=AccountType,image=image, Password=Password)
                signup.save()
                print("success input")
                return render(request, "signin.html", {})
        else:
            try:
                user = student.objects.get(Email=Email)
                messages.info(request, "Email already exist!!!")
                return render(request, "signup.html", {})
            except:
                Password = make_password(request.POST.get('Password'))
                signup = student(Fname=Fname, Lname=Lname, Email=Email, AccountType=AccountType,image=image, Password=Password)
                signup.save()
                print("success input")
                return render(request, "signin.html", {})
    elif request.session.get('email'):
        return redirect('/h')
    else:
        return render(request, "signup.html", {})

#for create class
def create_class(request):
    if request.method == "POST":
        name=request.POST.get("class_name")
        sec = request.POST.get("sec")
        sub = request.POST.get("sub")
        room = request.POST.get("room")
        code= get_random_string(length=8)
        user = teacher.objects.get(id=request.session.get('teacher_id'))
        create = Class(name=name,section=sec,subject=sub,room=room,class_code=code,teacherId=user)
        create.save()
        messages.info(request, "Class create successfully")
        return redirect('/home')
#for join class
def join_class(request):
    if request.method == "POST":
        code=request.POST.get("class_code")
        studentId = student.objects.get(id=request.session.get('student_id'))
        try:
            croom = Class.objects.get(class_code=code)
            print("student id ", studentId)
            print(croom)
            studentId.classJoin.add(croom)
            print(studentId.classJoin.all())
            messages.info(request,"Class join successfully")
            return redirect('/home')
        except:
            messages.info(request,"No class found")
            return redirect('/home')


#for class view
def classView(request,cid):
    if "class_code" in request.POST:
        Email = request.POST.get('email')
        code = request.POST.get('class_code')
        sub = request.POST.get('subject_name')
        sec = request.POST.get('section')
        subject = 'Class Invitation'
        message = f'Dear Students, This is your class Code for joining {sub}.{sec} is {code} See you all in the class. Thanks'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [Email, ]
        send_mail(subject, message, email_from, recipient_list)
        print("email send")
    if 'post_title' in request.POST:
        Title = request.POST.get('post_title')
        desc = request.POST.get('post_desc')
        Due_time=request.POST.get('due_time')
        try:
            file1 = request.FILES['file']
            classId=Class.objects.get(id=cid)
            document = Material.objects.create(title=Title,description=desc,file=file1,classId=classId,dueTime=Due_time)
        except MultiValueDictKeyError:
            classId = Class.objects.get(id=cid)
            document = Material.objects.create(title=Title,description=desc,classId=classId,dueTime=Due_time)


        document.save()
        data1 = Class.objects.get(id=cid)
        students = student.objects.filter(classJoin=data1)
        for stu in students:
            data2=student.objects.get(id=stu.id)
            r=readingReview.objects.create(materialId=document,studentId=data2)
            r.save()
    if request.session.get('email'):
        data1=Class.objects.get(id=cid)

        data2=teacher.objects.get(id=data1.teacherId.id)
        material=Material.objects.filter(classId=cid).order_by('-id')
        students=student.objects.filter(classJoin=data1)
        studentcount = student.objects.filter(classJoin=data1).count()
        print(studentcount)
        if request.session.get('teacher_id'):
            data3=teacher.objects.get(id=request.session.get('teacher_id'))
            print("teacher class")
        else:
            data3 = student.objects.get(id=request.session.get('student_id'))
        return render(request, "class.html", {"detail": data1,"material":material,"teacher":data2,"profile":data3,"students":students,"total":studentcount})

    else:
        return redirect('/home')
def materialview(request,Mid):
    if request.session.get('email'):
        print("material id:",Mid)

        time = 0
        if request.session.get('teacher_id'):
            work=""
            data3 = teacher.objects.get(id=request.session.get('teacher_id'))
        else:
            data3 = student.objects.get(id=request.session.get('student_id'))
            print(data3.id)
            work=readingReview.objects.get(materialId=Mid,studentId=data3.id)
            images=Image.objects.filter(reviewId=work.id,status=True)

            for image in images:
                time=time+1
                print("1 minute")


        data = Material.objects.get(id=Mid)  # get material information
        return render(request, "material.html", {"profile":data3,"material": data,"work":work,"readingtime":time})
    else:
        return redirect('/home')
def pdfview(request,Mid):
    request.session['pageno'] =1 #set page no default
    if request.method=="POST":
        if "question" in request.POST:
            print(request.POST.get('question'))
            print(request.POST.get('pageno'))
            print(request.POST.get('width'))
            print(request.POST.get('top'))
            print(request.POST.get('left'))
            q=request.POST.get('question')
            pno=request.POST.get('pageno')
            request.session['pageno'] = pno #set page no
            #s=student.objects.get(id=request.session.get('student_id'))#get student information
            material=Material.objects.get(id=Mid)#get material information
            q=Question.objects.create(question=q,page_no=pno,width=request.POST.get('width'),top=request.POST.get('top'),left=request.POST.get('left'),material_id=material)#new text question
            q.save()
        elif "qanswer" in request.POST:
            print(request.POST.get('qid'))
            print(request.POST.get('qanswer'))
            print(request.session['pageno'])
            print(request.session['student_id'])
            qid=Question.objects.get(id=request.POST.get('qid'));
            sid=student.objects.get(id=request.session['student_id'])

            if Answer.objects.filter(questionId=qid,studentId=sid).exists():

                return HttpResponse("found")
            else:
                newAns=Answer.objects.create(questionId=qid,studentId=sid,page_no=request.session['pageno'],
                                         answer=request.POST.get('qanswer'))
                newAns.save()

        elif "PAGENO." in request.POST:
            print(request.POST.get('PAGENO.'))
            image1 = request.FILES["image_data"]
            print(image1)
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            # print(BASE_DIR)
            MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
            data3 = student.objects.get(id=request.session.get('student_id'))
            # print(MEDIA_ROOT,loc)
            b = """\\"""
            u = str(data3.image)
            u.replace(u[0], """\\""")
            loc = (str(MEDIA_ROOT) + b + u)
            # photoRecognize(loc, data3.id,data3.Fname,Mid,request.POST.get('PAGENO.'))
            # print(loc)
            print("recognizing started")
            face_1_image = face_recognition.load_image_file(loc)
            face_1_face_encoding = face_recognition.face_encodings(face_1_image)[0]
            face_2_image = face_recognition.load_image_file(image1)
            face_2_face_encoding = face_recognition.face_encodings(face_2_image)[0]

            check = face_recognition.compare_faces([face_1_face_encoding], face_2_face_encoding)
            print(check)
            M = Material.objects.get(id=Mid)
            if (readingReview.objects.filter(studentId=data3, materialId=M, status='incomplete')):
                print("find incomplete review")
                readingReview.objects.filter(studentId=data3, materialId=M, status='incomplete').update(
                    comTime=timezone.now(), status='complete')
                r = readingReview.objects.get(studentId=data3, materialId=M)
                if check[0]:

                    p = Image.objects.create(image=image1, pageNo=request.POST.get('PAGENO.'), status=True, reviewId=r)
                else:
                    p = Image.objects.create(image=image1, pageNo=request.POST.get('PAGENO.'), reviewId=r)
                p.save()
            else:
                print('complete')
                material = Material.objects.get(id=Mid)
                r = readingReview.objects.get(studentId=data3, materialId=material)
                if check[0]:

                    p = Image.objects.create(image=image1, pageNo=request.POST.get('PAGENO.'), status=True, reviewId=r)
                else:
                    p = Image.objects.create(image=image1, pageNo=request.POST.get('PAGENO.'), reviewId=r)
                p.save()

            print('image saved successful')
        else:
            try:
                audio = request.FILES["audio_data"]
            except:
                audio = request.POST.get("audio_data")
            pno = request.POST.get('pageno')
            print(audio)
            print(pno)
            request.session['pageno'] = pno  # set page no
            # s = student.objects.get(id=request.session.get('student_id'))  # get student information
            material = Material.objects.get(id=Mid)  # get material information
            q = Question.objects.create(AudioQuestion=audio, page_no=pno,
                                            material_id=material)  # new text question
            q.save()
    data=Material.objects.get(id=Mid) #get material information
    qdata=Question.objects.filter(material_id=Mid) #get all question under the material

    return render(request,"pdfview.html",{"material":data,"data":qdata})

def invite(request):
    return render(request, 'email.html')

def sendanmail(request):
    if request.method=="POST":
      emailid = request.POST.get('toemail')
      content=request.POST.get('content')

      subject = 'Class Invitation'
      message = f'Dear Student, Hello. The Class Code for PHI 104.6 is hxktigc See you all in the class. Thanks. -PHI104.6 (MNT) (MNTPHI104 - 6 -NSU).'
      email_from = settings.EMAIL_HOST_USER
      recipient_list = [emailid, ]
      send_mail(subject, message, email_from, recipient_list)

      return render(request,"invitation_send.html")


def review(request,mid):
    if request.session.get('email'):

        m=Material.objects.get(id=mid)
        com=readingReview.objects.filter(materialId=mid,status="complete").count();

        rincom=readingReview.objects.filter(materialId=mid,status="incomplete")
        rcom = readingReview.objects.filter(materialId=mid, status="complete")
        icom=readingReview.objects.filter(materialId=mid,status="incomplete").count();


        m=Material.objects.get(id=mid)
        if request.session.get('teacher_id'):
            data3 = teacher.objects.get(id=request.session.get('teacher_id'))

        return render(request, "review.html", {"profile": data3,"comlist":rcom,"incomlist":rincom,"material":m,"complete":com,"incomplete":icom})

    else:
        return redirect('/home')
def reviewstudent(request,rid):
    if request.session.get('email'):
        d=readingReview.objects.get(id=rid)
        photo=Image.objects.filter(reviewId=rid)
        images = Image.objects.filter(reviewId=rid, status=True)
        time=0;
        for image in images:
            time = time + 1;
        if request.session.get('teacher_id'):
            data3 = teacher.objects.get(id=request.session.get('teacher_id'))

        return render(request, "reviewStudent.html",{"profile": data3,"details":d,"photo":photo,"readingTime":time})

    else:
        return redirect('/home')
#for api using rest framework
@api_view(['GET'])
def apiView(request):
    api_urls = {
        'Sign in': 'api/signIn/',
        'Register': 'api/register/',
        'Join class': 'api/join/',
        'Create class': 'api/createClass/',
        'Class list':'api/classList/',
        'Material-list':'api/material-list/',
        'Material-post': 'api/material-post/'
    }
    return Response(api_urls)
@api_view(['POST'])
def materiallist(request):
    if request.method =='POST':
        print(request.body)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        cid = body['id']
        material=Material.objects.filter(classId=cid).order_by('-id')
        serializer= postSerializers(material,many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')

@api_view(['POST'])
def materialpost(request):
    if request.method =='POST':
        print(request.body)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        title = body['title']
        description=body['description']
        Id=body['cid']
        classid = Class.objects.get(id=Id)
        print(classid)
        post=Material.objects.create(title=title,description=description,classId=classid)
        post.save()
        js = {"msg": "post material successfully"}
        json_data = JSONRenderer().render(js)
        return HttpResponse(json_data, content_type='application/json')

@api_view(['GET'])
def studentlist(request,pk):
    posts= student.objects.get(id=pk)
    serializer= studentSerializers(posts,many=False)

    return JsonResponse(serializer.data)
@api_view(['POST'])
def signinInfo(request):
    if request.method =='POST':
        print(request.body)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        email = body['Email']
        password=body['Password']
        print(email)

        try:
            pythondata=student.objects.get(Email=email)
            if (check_password(password, pythondata.Password)):

                print(pythondata)
                serializer = studentSerializers(pythondata,many=False)
                json_data=JSONRenderer().render(serializer.data)
                return HttpResponse(json_data, content_type='application/json')
        except:
            pythondata = teacher.objects.get(Email=email)
            if (check_password(password, pythondata.Password)):
                print(pythondata)
                print("correct password")
                serializer = teacherSerializers(pythondata, many=False)
                json_data = JSONRenderer().render(serializer.data)
                return HttpResponse(json_data, content_type='application/json')

@api_view(['POST'])
def register(request):
    if request.method =='POST':
        print(request.body)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        type=body['AccountType']
        rdata = JSONParser().parse(request)
        if type=="Student":

            serializer=studentSerializers(data=rdata)
            if serializer.is_valid():
                serializer.save()
                js = {"msg": "student register successfully"}
                json_data = JSONRenderer().render(js)
                return HttpResponse(json_data, content_type='application/json')
        else:
            serializer = teacherSerializers(data=rdata)
            if serializer.is_valid():
                serializer.save()
                js = {"msg": "teacher register successfully"}
                json_data = JSONRenderer().render(js)
                return HttpResponse(json_data, content_type='application/json')



@api_view(['POST'])
def createClass(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        teacher_id = body['teacher_id']
        name = body["class_name"]
        sec = body["sec"]
        sub = body["sub"]
        room = body["room"]
        code = get_random_string(length=8)
        user = teacher.objects.get(id=teacher_id)
        create = Class(name=name, section=sec, subject=sub, room=room, class_code=code, teacherId=user)
        create.save()
        js = {"msg": "class create successfully"}
        json_data = JSONRenderer().render(js)
        return HttpResponse(json_data, content_type='application/json')

@api_view(['POST'])
def joinClass(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        student_id = body['Student_id']
        code = body['code']
        studentId = student.objects.get(id=student_id)
        try:
            croom = Class.objects.get(class_code=code)
            studentId.classJoin.add(croom)
            js = {"msg": "class join successfully"}
            json_data = JSONRenderer().render(js)
            return HttpResponse(json_data, content_type='application/json')
        except:
            js = {"msg": "no class found"}
            json_data = JSONRenderer().render(js)

@api_view(['POST'])
def Classlist(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        try:

            teacher_id = body['teacher_id']
            data = Class.objects.filter(teacherId=teacher_id)
            data1 = teacher.objects.get(id=teacher_id)
            serializer = classSerializers(data, many=True)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type='application/json')
        except KeyError:
            student_id = body['student_id']
            studentId = student.objects.get(id=student_id)
            data = studentId.classJoin.all()
            serializer = classSerializers(data, many=True)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type='application/json')






