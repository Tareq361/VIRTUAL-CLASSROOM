from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.hashers import make_password,check_password
from django.utils.datastructures import MultiValueDictKeyError
from requests import request
from .models import teacher,student,Class,Material,TextQuestion,audioQuestion
from django.utils.crypto import get_random_string #for random class code generator
from django.contrib import messages
import requests
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
        if request.session.get('teacher_id'):
            data=Class.objects.filter(teacherId=request.session.get('teacher_id'))
            data1 = teacher.objects.get(id=request.session.get('teacher_id'))
            return render(request, "home.html", {"detail":data,"profile":data1})
        elif request.session.get('student_id'):
            studentId = student.objects.get(id=request.session.get('student_id'))
            data=studentId.classJoin.all()
            return render(request, "home.html", {"detail":data,"profile":studentId})
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
                return redirect('/signin')
        else:
            print("incorrect pass")
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
            Password = make_password(request.POST.get('Password'))
            signup = teacher(Fname=Fname, Lname=Lname, Email=Email, AccountType=AccountType,image=image, Password=Password)
            signup.save()
            print("success input")
            return render(request, "signin.html", {})
        else:
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


#for invite student
def InviteStudent(request):
    if "class_code" in request.POST:
        Email = request.POST.get('email')
        code = request.POST.get('class_code')
        sub = request.POST.get('subject_name')
        sec = request.POST.get('section')
        subject = 'Class Invitation'
        message = f'Dear Students, This is your class Code for joining {sub}.{sec}is {code} See you all in the class. Thanks'
        print(Email)
        return HttpResponse("Invite student successfully")
#for class view
def classView(request,cid):
    if request.method == "POST":
        Title = request.POST.get('post_title')
        desc = request.POST.get('post_desc')
        try:
            file1 = request.FILES['file']
            classId=Class.objects.get(id=cid)
            document = Material.objects.create(title=Title,description=desc,file=file1,classId=classId)
        except MultiValueDictKeyError:
            document = Material.objects.create(title=Title,description=desc)


        document.save()
        return HttpResponse("Your post submitted")
    if request.session.get('email'):
        data1=Class.objects.get(id=cid)

        data2=teacher.objects.get(id=data1.teacherId.id)
        material=Material.objects.filter(classId=cid).order_by('-id')
        if request.session.get('teacher_id'):
            data3=teacher.objects.get(id=request.session.get('teacher_id'))
        else:
            data3 = student.objects.get(id=request.session.get('student_id'))
        return render(request, "class.html", {"detail": data1,"material":material,"teacher":data2,"profile":data3})

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
            s=student.objects.get(id=request.session.get('student_id'))#get student information
            material=Material.objects.get(id=Mid)#get material information
            q=TextQuestion.objects.create(question=q,student_id=s,page_no=pno,width=request.POST.get('width'),top=request.POST.get('top'),left=request.POST.get('left'),material_id=material)#new text question
            q.save()

        else:

            audio = request.FILES["audio_data"]
            pno = request.POST.get('pageno')
            print(audio)
            print(pno)
            request.session['pageno'] = pno  # set page no
            s = student.objects.get(id=request.session.get('student_id'))  # get student information
            material = Material.objects.get(id=Mid)  # get material information
            q = TextQuestion.objects.create(AudioQuestion=audio, student_id=s, page_no=pno,
                                            material_id=material)  # new text question
            q.save()
    data=Material.objects.get(id=Mid) #get material information
    qdata=TextQuestion.objects.filter(material_id=Mid) #get all question under the material

    return render(request,"pdfview.html",{"material":data,"data":qdata})

def Audio(request):
    if request.method == "POST":
        a = request.FILES["audio_data"]
        p=request.POST.get('pageno')
        q=audioQuestion(file=a)
        q.save()
        print(a)
        print(p)
        return HttpResponse("recived")
