from importlib import import_module

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.test import Client
from django.contrib.sessions.models import Session
from .models import student,teacher,Class,Material,Question,readingReview,Image
# Create your tests here.
class ModelTestAndView(TestCase):
    def setUp(self):
        s = student.objects.create(Fname="tareq",Lname="321",Email="tareq321@gmail,com",Password="tareq321",image="image3535.jpg")
        t = teacher.objects.create(Fname="shimul",Lname="331",Email="shimul331@gmail,com",Password=make_password("shimul331"),image="image3535.jpg")
        new = Class.objects.create(name='cse327', teacherId=t)
        m = Material.objects.create(title="test", classId=new,file="test.pdf")
        r=readingReview.objects.create(materialId=m,studentId=s,)
        i=Image.objects.create(reviewId=r,image="student.jpg")
        q = Question.objects.create(question="what", student_id=s, page_no=1, material_id=m)
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.session = store
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
        response = self.client.post('/signin/',
                                    {'Email': 'shimul331@gmail,com', 'Password': 'shimul331', 'isStudent': 'false'})

        print("Teacher sign in page", response.status_code)
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 302)
    def test_student_model(self):

        new=student.objects.get(Fname="tareq")
        self.assertEqual(str(new),"tareq")

    def test_teacher_model(self):
        new = teacher.objects.get(Fname="shimul")
        self.assertEqual(str(new), "shimul")

    def test_class_model(self):
        new = Class.objects.get(name='cse327')
        self.assertEqual(str(new), "cse327")
        self.assertEqual(new.get_absolute_url(), f'/class/{new.id}')



    def test_material_model(self):
        new = Material.objects.get(title="test")
        self.assertEqual(str(new), "test")
        self.assertEqual(new.get_absolute_url(), f'/pdf/{new.id}')
        self.assertEqual(new.get_absolute_url_material(), f'/material/{new.id}')
        self.assertEqual(new.get_absolute_url_reviewmaterial(), f'/review/{new.id}')

    def test_question_model(self):
        new = Question.objects.get(question="what")
        self.assertEqual(str(new), "what")
    def test_readingReview_model(self):
        s=student.objects.get(Fname="tareq")
        new = readingReview.objects.get(studentId=s)
        self.assertEqual(str(new.studentId.Fname), "tareq")
        self.assertEqual(new.get_absolute_url_reviewmaterialstudent(), f'/reviewStudent/{new.id}')
    def test_image_model(self):
        s = student.objects.get(Fname="tareq")
        new = readingReview.objects.get(studentId=s)
        i=Image.objects.get(reviewId=new)
        self.assertEqual(str(i.reviewId.studentId.Fname), "tareq")

    def test_signIn(self):
        # Issue a GET request.

        response = self.client.get('/signin/')
        print("sign in page", response.status_code)
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 302)

    def test_home_teacher(self):
        response = self.client.get('/home/')
        print("teacher home response code", response.status_code)
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
    def test_create_class(self):

        response = self.client.post('/create_class/',
                                    {'class_name': 'cse331', 'sec': '1', 'sub': 'database','room':'sac238'})

        print("create class page", response.status_code)
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 302)
    def test_teacher_class_view(self):
        new = Class.objects.get(name="cse327")
        response = self.client.get(f'/class/{new.id}')
        print("teacher class view response code", response.status_code)
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_post_material(self):
        new = Class.objects.get(name="cse327")
        response = self.client.post(f'/class/{new.id}',
                                    {'post_title': 'test2', 'post_desc': 'test desciption', 'due_time': '2012-09-04 06:00:00.000000'})

        print("post material", response.status_code)
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
    def test_send_invite(self):
        new = Class.objects.get(name="cse327")
        response = self.client.post(f'/class/{new.id}',
                                    {'email': 'abu.tareq@northsouth.edu', 'class_code': 'sufer7eu', 'subject_name': 'cse327','section':'3'})

        print("invite student", response.status_code)
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
    def test_student_view(self):
        new1=student.objects.get(Fname="tareq")
        session = self.session
        session['email'] = new1.Email
        session['student_id'] = new1.id
        session.save()
        new = Class.objects.get(name="cse327")
        response = self.client.post('/join_class/',
                                    {'class_code': f'{new.class_code}'})

        print("join class", response.status_code)
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 302)
        #asked question
        new2 = Material.objects.get(title="test")
        response2 = self.client.post(f'/pdf/{new.id}',{'question':'test questioj','pageno':'1','width':'200','top':'300','left':'400'})
        print("ask question", response2.status_code)
        # Check that the response is 200 OK.
        self.assertEqual(response2.status_code, 200)
        #askedaudio question
        response3 = self.client.post(f'/pdf/{new.id}',
                                     {'audio':'blob.wav','pageno':'1'})
        print("ask audio question", response3.status_code)
        # Check that the response is 200 OK.
        self.assertEqual(response3.status_code, 200)
    def test_teacher_pdf_view(self):
        new = Material.objects.get(title="test")
        response = self.client.get(f'/pdf/{new.id}')
        print("teacher pdf view response code", response.status_code)
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
    def test_teacher_material_view(self):
        new = Material.objects.get(title="test")
        response = self.client.get(f'/material/{new.id}')
        print("teacher material view response code", response.status_code)
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_teacher_review_view(self):
        new = Material.objects.get(title="test")
        response = self.client.get(f'/review/{new.id}')
        print("teacher review view response code", response.status_code)
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
    def test_teacher_reviewStudent_view(self):
        new = Material.objects.get(title="test")
        new2 = readingReview.objects.get(materialId=new)
        response = self.client.get(f'/reviewStudent/{new2.id}')
        print("teacher student reading review view response code", response.status_code)
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_signOut(self):
        # Issue a GET request.
        response = self.client.get('/signout/')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 302)




